"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import random
import torch
import mlflow
import pandas as pd

from fastiot.core import FastIoTService, Subject, subscribe, loop
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing

from dienstleister.logging.KIOptiPack_banner import KIOptiPack_banner
from dienstleister.logging.wzl_banner import wzl_banner
from dienstleister.ml_lifecycle_utils.edc_endpoints import dataset_edc_endpoint
from dienstleister.ml_lifecycle_utils.ml_lifecycle_broker_facade import request_get_edc_labeled_dataset, request_get_processed_data_points_from_raw_data
from dienstleister.ml_training.pytorch_utils import DemonstratorNeuralNet, MyDataset

from torch import nn, optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from mlflow.data.pandas_dataset import PandasDataset


class MlTrainingService(FastIoTService):

    MLFLOW_TRACKING_URI = "http://127.0.0.1:8080"

    _training_interval = 60 * 15 # 10 minutes


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mlflow.set_tracking_uri(self.MLFLOW_TRACKING_URI)

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("ML Training Service (Dienstleister) started.")

    @loop
    async def produce(self):

        await self.train_model()

        return asyncio.sleep(self._training_interval)

    async def train_model(self, **kwargs):
        self._logger.info("Training model")

        self._logger.info("Fetching labeled dataset from Anlagenbetreiber via EDC")
        labeled_dataset = await request_get_edc_labeled_dataset(fiot_service=self)
        processed_dataset = await request_get_processed_data_points_from_raw_data(fiot_service=self, data=labeled_dataset)
        df = pd.DataFrame(processed_dataset)

        default_params = {
            "learning_rate": 0.001,
            "batch_size": 32,
            "num_epochs": 100,
            "input_dim": 40,
            "output_dim": 3,
            "hidden_dim": 64
        }
        params = {**default_params, **kwargs}

        model = DemonstratorNeuralNet(params["input_dim"], params["hidden_dim"], params["output_dim"])
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=params["learning_rate"])

        # Convert integer columns to float64 to handle missing values
        df = df.astype({col: 'float64' for col in df.select_dtypes(include='int').columns})

        dataset = MyDataset(df, ["Temp", "Zeit", "Druck"])
        dataloader = DataLoader(dataset, batch_size=params["batch_size"], shuffle=True)

        mlflow_dataset: PandasDataset = mlflow.data.from_pandas(df, source=dataset_edc_endpoint)

        DESC = """
        Ausformung
        1	keine Umformung
        2	beginnende Umformung
        3	unvollständige Ausformung
        4	vollständige Ausformung
        5	entlüftungs bohrungen
        6	geschmolzen

        Kaltverformung
        1	Eisschollen
        2	Kaltverformung / Weißfärbung
        3	klar
        """

        with mlflow.start_run() as run:
            # Log parameters
            for key, value in params.items():
                mlflow.log_param(key, value)

            mlflow.log_input(mlflow_dataset, context="training")

            for epoch in range(params["num_epochs"]):
                running_loss = 0.0
                for inputs, targets in dataloader:
                    inputs = inputs.float()
                    targets = targets.float()

                    optimizer.zero_grad()
                    outputs = model(inputs)
                    loss = criterion(outputs, targets)
                    loss.backward()
                    optimizer.step()
                    running_loss += loss.item()

                epoch_loss = running_loss / len(dataloader)
                print(f"Epoch {epoch + 1}/{params['num_epochs']}, Loss: {epoch_loss}")

                # Log metrics
                mlflow.log_metric("loss", epoch_loss, step=epoch)

            # Log model with input example
            input_example = torch.randn(1, params["input_dim"]).float().numpy()
            # get an example input form the dataset
            mlflow.pytorch.log_model(model, "OpenHubDaysModel", input_example=input_example)

            # Log a dictionary as an artifact
            raw_datapoint = {  # FolieVP28
                "ListeKomponenten": ["K000055"],  # id or material name
                "Massenanteile": None,  # unit g/g
                "Flächenanteilmodifiziert": 0,  # unit %
                "Geometrie": "Quader",  # unit: list of types
                "Kopfraumatmosphäre": None,  # unit list of (pa)
                "Masse": None,  # unit g
                "Verpackungstyp": "Folie",  # type
                "CAD": None,  # link to CAD file
                "RauheitRa": 0.729,  # unit µm
                "RauheitRz": 3.33,  # unit µm
                "Trübung": 450.7,  # unit HLog
                "Glanz": 46.9,  # unit GE
                "Dicke": 777,  # unit µm
                "Emodul": 923.5297844703941,  # unit MPa
                "MaximaleZugspannung": 39.27389962516748,  # unit MPa
                "MaximaleLängenänderung": 24.74862718628088,  # unit %
                # Qulaity Labels
                "Ausformung": 1,
                "Kaltverfo": 3,
                # Training Label
                "Temp": 300,
                "Zeit": 8,
                "Druck": 1,
            },

            raw_prediction_payload = {
                "ListeKomponenten": ["K000055"],  # id or material name
                "Massenanteile": None,  # unit g/g
                "Flächenanteilmodifiziert": 0,  # unit %
                "Geometrie": "Quader",  # unit: list of types
                "Kopfraumatmosphäre": None,  # unit list of (pa)
                "Masse": None,  # unit g
                "Verpackungstyp": "Folie",  # type
                "CAD": None,  # link to CAD file
                "RauheitRa": 0.729,  # unit µm
                "RauheitRz": 3.33,  # unit µm
                "Trübung": 450.7,  # unit HLog
                "Glanz": 46.9,  # unit GE
                "Dicke": 777,  # unit µm
                "Emodul": 923.5297844703941,  # unit MPa
                "MaximaleZugspannung": 39.27389962516748,  # unit MPa
                "MaximaleLängenänderung": 24.74862718628088,  # unit %
                # Qulaity Labels
                "Ausformung": 1,
                "Kaltverfo": 3,
            }

            mlflow.log_dict(raw_datapoint, "raw_label_datapoint.json")
            mlflow.log_dict(raw_prediction_payload, "raw_prediction_payload.json")

            model_uri = f"runs:/{run.info.run_id}/OpenHubDaysModel"
            model_details = mlflow.register_model(model_uri=model_uri, name="OpenHubDaysModel")

            # Update model version with additional details
            client = mlflow.tracking.MlflowClient()
            client.update_model_version(
                name="OpenHubDaysModel",
                version=model_details.version,
                description=f"This is a demonstration model for OpenHubDays. Its updated regularly. {DESC}"
            )

            client.set_model_version_tag(
                name="OpenHubDaysModel",
                version=model_details.version,
                key="alias",
                value="v1.0 rolling update"
            )



if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    MlTrainingService.main()
