"""
This file has just been created automatically.
This is the file where you can write you own service.
Currently, the is code provides a basic producer and an basic consumer.
In order for your code to work, you must delete the code that you are not using and add your own application logic.
"""

import asyncio
import logging
import random
import mlflow
import torch

import pandas as pd

from fastiot.core import FastIoTService, Subject, subscribe, loop, reply
from fastiot.core.core_uuid import get_uuid
from fastiot.core.time import get_time_now
from fastiot.msg.thing import Thing
from sklearn.pipeline import Pipeline

from hersteller.data_processing.pipeline_operations import OneHotEncodePd, NormalizeCols, MultiOneHotEncodePd, \
    ColumnDropper
from hersteller.logging.KIOptiPack_banner import KIOptiPack_banner
from hersteller.logging.wzl_banner import wzl_banner
from hersteller.ml_lifecycle_utils.ml_lifecycle_broker_facade import error_response_thing, ok_response_thing
from hersteller.ml_lifecycle_utils.ml_lifecycle_subjects_name import ML_SERVING_SUBJECT


class MlServingService(FastIoTService):
    """
    ML Serving Service

    :param args: Positional arguments passed to the superclass or internal use.

    :param kwargs: Arbitrary keyword arguments, allowing \
                   for extensibility or forwarding to the\
                    superclass constructor or other components.
    """
    MLFLOW_TRACKING_URI = "http://127.0.0.1:8080"
    MODEL_URI = "models:/OpenHubDaysModel/4"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mlflow.set_tracking_uri(self.MLFLOW_TRACKING_URI)

    async def _start(self):
        print(wzl_banner)
        print(KIOptiPack_banner)
        self._logger.info("ML Serving Service (Hersteller) started.")

        example_datapoint = {
            "ListeKomponenten": ["K000055", "K000057"],  # id or material name
            "Massenanteile": [0.75, 0.25],  # unit g/g
            "Flächenanteilmodifiziert": 0,  # unit %
            "Geometrie": "Quader",  # unit: list of types
            "Kopfraumatmosphäre": None,  # unit list of (pa)
            "Masse": None,  # unit g
            "Verpackungstyp": "Folie",  # type
            "CAD": None,  # link to CAD file
            "RauheitRa": 0.08966666666666667,  # unit µm
            "RauheitRz": 0.7366666666666667,  # unit µm
            "Trübung": 176.6,  # unit HLog
            "Glanz": 39,  # unit GE
            "Dicke": 769.6666666666666,  # unit µm
            "Emodul": 878.7979886112262,  # unit MPa
            "MaximaleZugspannung": 37.156951742990245,  # unit MPa
            "MaximaleLängenänderung": 19.73276680651324,  # unit %
            # Quality Labels
            "Ausformung": 6,
            "Kaltverfo": 3,
        }


    @reply(ML_SERVING_SUBJECT)
    async def get_prediction(self, _: str, msg: Thing) -> Thing:
        """
        Gets a prediction using :py:func:`perform_prediction` and \
        returns it to the requesting service

        :param _: The topic of the message.
        :type _: str

        :param msg: The data to be used for the prediction
        :type msg: Thing

        :return: The prediction
        :rtype: Thing

        """
        self._logger.info("Received request to get prediction.")

        if not isinstance(msg.value, list):
            self._logger.error(f"Payload (the 'value' field of the msg Thing) must be of type list, "
                               f"but received: {type(msg.value)}")
            e = ValueError("Payload must be a list of processed data points")
            return error_response_thing(exception=e, fiot_service=self)

        try:

            predictions = await self.perform_prediction(data=msg.value)

        except Exception as e:
            self._logger.error(f"Error while fetching labeled data over the edc: {e}")
            return error_response_thing(exception=e, fiot_service=self)

        return ok_response_thing(payload=predictions, fiot_service=self)

    async def perform_prediction(self, data: list[dict]) -> list[dict]:
        """
        Performs a prediction using the model set in the ModelURI

        :param data: The data used for the prediction
        :type data: list[dict]

        :return: The predictions
        :rtype: list[dict]

        """
        self._logger.info("Performing prediction")
        # Load the model

        # Load the model from the MLflow repository
        model = mlflow.pytorch.load_model(self.MODEL_URI)

        # Convert the input data to a DataFrame
        input_df = pd.DataFrame(data)
        # add the cols "Temp", "Zeit", "Druck" if they are not present and initialize them with 0.0
        for col in ["Temp", "Zeit", "Druck", '_id', 'CAD', 'Verpackungstyp', 'Masse', 'Geometrie', 'Massenanteile', 'Kopfraumatmosphäre', 'Flächenanteilmodifiziert', 'ListeKomponenten']:
            if col not in input_df.columns:
                input_df[col] = 0.0

        # Preprocess the input data
        # alternative: build a connection to the service that provides the preprocessed data over the edc
        preprocessed_input = self._preprocessor.transform(input_df)
        # drop the prediction columns
        for col in ["Temp", "Zeit", "Druck"]:
            preprocessed_input.pop(col)

        # Convert the preprocessed input data to a PyTorch tensor
        input_tensor = torch.tensor(preprocessed_input.to_numpy()).float()

        # Perform a forward pass through the model
        with torch.no_grad():
            output_tensor = model(input_tensor)
            # to pandas df with column names Temp, Zeit, Druck
            output_df = pd.DataFrame(output_tensor.numpy(), columns=["Temp", "Zeit", "Druck"])
            print(output_df.head())
            # rescale
            # scale temp by 500
            output_df["Temp"] = output_df["Temp"] * 500
            # scale Zeit by 40
            output_df["Zeit"] = output_df["Zeit"] * 40
            # scale Druck by 6
            output_df["Druck"] = output_df["Druck"] * 6
            print(output_df.head())

        return output_df.to_dict(orient="records")

    _preprocessor = Pipeline(
        verbose=False,
        steps=[
            (
                "Drop irrelevant columns",
                # CAS is always None,
                # Verpackungstyp is always 'Folie'
                # Masse is always None
                # Geometrie is always 'Quader'
                # Kopfraumatmosphäre is always None
                # Flächenanteilmodifiziert is always 0
                # therefore these fields do not provide any information
                ColumnDropper(["CAD", "Verpackungstyp", "Masse", "Geometrie", "Massenanteile", "Kopfraumatmosphäre",
                               "Flächenanteilmodifiziert", "_id"]),
            ), (
                "One-hot encode ListeKomponenten",
                MultiOneHotEncodePd(
                    target="ListeKomponenten",
                    prefix="Komponente",
                    sep="_",
                    required_columns=[
                        "Komponente_K000034",
                        "Komponente_K000035",
                        "Komponente_K000055",
                        "Komponente_K000057",
                        "Komponente_K000141"
                    ]
                )
            ),
            ("Normalise RauheitRa", NormalizeCols(
                target="RauheitRa",
                column_range=(0.05933333333333333, 0.729),
                feature_range=(0, 1)
            )),
            ("Normalise RauheitRz", NormalizeCols(
                target="RauheitRz",
                column_range=(0.39666666666666667, 3.33),
                feature_range=(0, 1)
            )),
            ("Normalise Trübung", NormalizeCols(
                target="Trübung",
                column_range=(63.9, 450.7),
                feature_range=(0, 1))
             ),
            ("Normalise Glanz", NormalizeCols(
                target="Glanz",
                column_range=(27, 67),
                feature_range=(0, 1)
            )),
            ("Normalise Dicke", NormalizeCols(
                target="Dicke",
                column_range=(727.6666666666666, 794.6666666666666),
                feature_range=(0, 1)
            )),
            ("Normalise Emodul", NormalizeCols(
                target="Emodul",
                column_range=(775.2626646454261, 923.5297844703941),
                feature_range=(0, 1)
            )),
            ("Normalise MaximaleZugspannung",
             NormalizeCols(
                 target="MaximaleZugspannung",
                 column_range=(29.682633925969455, 39.27389962516748),
                 feature_range=(0, 1)
             )),
            ("Normalise MaximaleLängenänderung", NormalizeCols(
                target="MaximaleLängenänderung",
                column_range=(12.61880576560562, 75.62994222943517),
                feature_range=(0, 1)
            )),
            ("Normalise Temp", NormalizeCols(
                target="Temp",
                column_range=(0, 500),
                feature_range=(0, 1)
            )),
            ("Normalise Druck", NormalizeCols(
                target="Druck",
                column_range=(0, 6),
                feature_range=(0, 1)
            )),
            ("Normalise Zeit", NormalizeCols(
                target="Zeit",
                column_range=(0, 40),
                feature_range=(0, 1)
            )),
            (
                "One-hot encode Ausformung",
                OneHotEncodePd(
                    target="Ausformung",
                    prefix="Ausformung",
                    sep="_",
                    required_columns=[
                        "Ausformung_1",
                        "Ausformung_1.0",
                        "Ausformung_1.5",
                        "Ausformung_2",
                        "Ausformung_2.0",
                        "Ausformung_2.5",
                        "Ausformung_3",
                        "Ausformung_3.0",
                        "Ausformung_3.5",
                        "Ausformung_4",
                        "Ausformung_4.0",
                        "Ausformung_4.5",
                        "Ausformung_5",
                        "Ausformung_5.0",
                        "Ausformung_5.5",
                        "Ausformung_6",
                        "Ausformung_6.0",
                        "Ausformung_6.5",
                    ]
                )
            ),
            (
                "One-hot encode Kaltverfo",
                OneHotEncodePd(
                    target="Kaltverfo",
                    prefix="Kaltverfo",
                    sep="_",
                    required_columns=[
                        "Kaltverfo_1",
                        "Kaltverfo_1.0",
                        "Kaltverfo_1.5",
                        "Kaltverfo_2",
                        "Kaltverfo_2.0",
                        "Kaltverfo_2.5",
                        "Kaltverfo_3",
                        "Kaltverfo_3.0",
                        "Kaltverfo_3.5",
                    ]
                )
            ),
        ])


if __name__ == '__main__':
    # Change this to reduce verbosity or remove completely to use `FASTIOT_LOG_LEVEL` environment variable to configure
    # logging.
    logging.basicConfig(level=logging.DEBUG)
    MlServingService.main()
