import pandas as pd
import mlflow
from mlflow.data.pandas_dataset import PandasDataset
from sklearn.pipeline import Pipeline

from data_standalone import raw_data

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
import torch
from torch import nn, optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

MLFLOW_TRACKING_URI = "http://127.0.0.1:8080"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

DESC="""
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
class ColumnDropper(BaseEstimator, TransformerMixin):
    """
    Drop the specified columns from the DataFrame.

    Methods
    -------
    fit(target)
        Return self
    transform(x: pd.DataFrame) -> pd.DataFrame
        Drop the specified columns from the DataFrame.
    """

    def __init__(self, target: list):
        """ Initialize the ColumnDropper object."""
        self.target = target

    def fit(self, target):
        """ Return self."""
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        """
        Drop the specified columns from the DataFrame.

        Parameters
        ----------
        x : pd.DataFrame
            The DataFrame to transform.
        """
        return x.drop(self.target, axis=1)

class ColumnTypeSetter(BaseEstimator, TransformerMixin):
    """
    Set the specified columns to type float in the DataFrame.

    Methods
    -------
    fit(target)
        Return self
    transform(x: pd.DataFrame) -> pd.DataFrame
        Set the specified columns to type float in the DataFrame.
    """

    def __init__(self, target: list):
        """ Initialize the ColumnTypeSetter object."""
        self.target = target

    def fit(self, target):
        """ Return self."""
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        """
        Set the specified columns to type float in the DataFrame.

        Parameters
        ----------
        x : pd.DataFrame
            The DataFrame to transform.
        """
        x[self.target] = x[self.target].astype(float)
        return x
class OneHotEncodePd(BaseEstimator, TransformerMixin):
    """
    One-hot encode the specified column.

    Methods
    -------
    fit(target)
        Return self
    transform(x: pd.DataFrame) -> pd.DataFrame
    """

    def __init__(self, target: str, prefix: str, sep: str, required_columns=None):
        """
        Initialize the OneHotEncodePd object.

        Parameters
        ----------
        target : str
            The column to one-hot encode.
        prefix : str
            The prefix to use for the one-hot encoded columns.
        sep : str
            The separator to use for the one-hot encoded columns.
        required_columns : list
            A list of columns that should be present in the DataFrame after one-hot encoding.
        """

        if required_columns is None:
            required_columns = []
        self.target = target
        self.prefix = prefix
        self.sep = sep
        self.required_columns = required_columns

    def fit(self, target):
        """

        Parameters
        ----------
        target

        Returns
        -------

        """
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        """
        One-hot encode the specified column.

        Parameters
        ----------
        x

        Returns
        -------
        pd.DataFrame
        """
        # Perform in-place one-hot encoding
        df_encoded = pd.get_dummies(x, columns=[self.target], prefix=self.prefix,
                                    prefix_sep=self.sep, dtype=float)

        # Replace the original 'Category' column with the one-hot encoded columns
        x[df_encoded.columns] = df_encoded

        # Drop the original 'Category' column
        x.drop(columns=[self.target], inplace=True)

        # Ensure all required columns are present, adding them with 0s if necessary
        for column in self.required_columns:
            if column not in x.columns:
                x[column] = 0.0

        return x


class MultiOneHotEncodePd(BaseEstimator, TransformerMixin):
    """
    One-hot encode a column containing lists of categorical values.

    Methods
    -------
    fit(target)
        Return self
    transform(x: pd.DataFrame) -> pd.DataFrame
    """

    def __init__(self, target: str, prefix: str, sep: str, required_columns=None):
        """
        Initialize the MultiOneHotEncodePd object.

        Parameters
        ----------
        target : str
            The column to one-hot encode.
        prefix : str
            The prefix to use for the one-hot encoded columns.
        sep : str
            The separator to use for the one-hot encoded columns.
        required_columns : list
            A list of columns that should be present in the DataFrame after one-hot encoding.
        """
        if required_columns is None:
            required_columns = []
        self.target = target
        self.prefix = prefix
        self.sep = sep
        self.required_columns = required_columns

    def fit(self, target):
        """ Return self."""
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        """
        One-hot encode the specified column containing lists of categorical values.

        Parameters
        ----------
        x : pd.DataFrame
            The DataFrame to transform.

        Returns
        -------
        pd.DataFrame
        """
        # Initialize the one-hot encoded columns with 0s
        for column in self.required_columns:
            x[column] = 0.0

        # Iterate over each row and set the corresponding one-hot encoded columns to 1
        for index, row in x.iterrows():
            for value in row[self.target]:
                column_name = f"{self.prefix}{self.sep}{value}"
                if column_name in x.columns:
                    x.at[index, column_name] = 1.0

        # Drop the original target column
        x.drop(columns=[self.target], inplace=True)

        return x


class NormalizeCols(BaseEstimator, TransformerMixin):
    """
    Normalize the specified column to the specified feature range using provided column range.

    Methods
    -------
    fit(target)
        Return self
    transform(x: pd.DataFrame) -> pd.DataFrame
        Normalize the specified column to the specified feature range.
    """

    def __init__(self, target: str, feature_range: tuple, column_range: tuple):
        """
        Initialize the CustomNormalizeCols object.

        Parameters
        ----------
        target : str
            The column to normalize.
        feature_range : tuple
            The desired range of the transformed data.
        column_range : tuple
            The actual range of the column data.
        """
        self.target = target
        self.feature_range = feature_range
        self.column_range = column_range

    def fit(self, target):
        """ Return self."""
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize the specified column to the specified feature range using provided column range.

        Parameters
        ----------
        x : pd.DataFrame
            The DataFrame to transform.

        Returns
        -------
        pd.DataFrame
        """
        df = x.copy()  # don't modify original df
        col_min, col_max = self.column_range
        feature_min, feature_max = self.feature_range

        df[self.target] = df[self.target].apply(
            lambda x: feature_min + (x - col_min) * (feature_max - feature_min) / (col_max - col_min)
            if not pd.isna(x) else pd.NA
        )
        return df


class MyDataset(Dataset):
    """
    A custom dataset for the pytorch regression service.

    Attributes
    ----------
    df : pd.DataFrame
        The dataframe containing the data.
    prediction_columns : list
        The columns to be used as prediction targets.

    Methods
    -------
    __len__()
        Return the length of the dataset.
    __getitem__(idx)
        Get an item from the dataset.
    """

    def __init__(self, df: pd.DataFrame, prediction_columns: list):
        """
        Initialize the dataset.

        Parameters
        ----------
        df : pd.DataFrame
            The dataframe containing the data.
        prediction_columns : list
            The columns to be used as prediction targets.
        """
        self.df = df
        self.prediction_columns = prediction_columns

    def __len__(self):
        """
        Return the length of the dataset.

        Returns
        -------
        int
            The length of the dataset.
        """
        return len(self.df)

    def __getitem__(self, idx):
        """
        Get an item from the dataset.

        Parameters
        ----------
        idx : int
            The index of the item.

        Returns
        -------
        tuple
            The input and output data.
        """

        temp = self.df.iloc[idx].copy()
        y_data = temp[self.prediction_columns].to_numpy()
        # Remove the prediction columns from the data
        # somehow drop does not work properly on a single datapoint
        for col in self.prediction_columns:
            temp.pop(col)
        x_data = temp.to_numpy()

        return x_data, y_data


class DemonstratorNeuralNet(nn.Module):
    """
    A simple neural network for demonstration purposes.

    Attributes
    ----------
    layer_1 : torch.nn.Linear
        The first linear layer.
    layer_2 : torch.nn.Linear
        The second linear layer.
    layer_3 : torch.nn.Linear
        The third linear layer.

    Methods
    -------
    forward(x)
        Forward pass through the network.
    """

    def __init__(self, input_dim, hidden_dim, output_dim, *args, **kwargs):
        """
        Initialize the network.

        Parameters
        ----------
        input_dim
        hidden_dim
        output_dim
        args
        kwargs
        """
        super().__init__(*args, **kwargs)
        self.layer_1 = nn.Linear(input_dim, hidden_dim)
        self.layer_2 = nn.Linear(hidden_dim, hidden_dim)
        self.layer_3 = nn.Linear(hidden_dim, hidden_dim)
        self.layer_4 = nn.Linear(hidden_dim, hidden_dim)
        self.layer_5 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """
        Forward pass through the network.

        Parameters
        ----------
        x
            The input to the network.

        Returns
        -------
        torch.Tensor
            The output of the network.
        """
        x = torch.relu(self.layer_1(x))
        x = torch.relu(self.layer_2(x))
        x = torch.relu(self.layer_3(x))
        x = torch.relu(self.layer_4(x))
        x = self.layer_5(x)
        return x


def train_model(df, num_epochs=100, batch_size=32, hidden_dim=288, learning_rate=0.001, **kwargs):
    """
    Train a PyTorch model.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the data.
    num_epochs : int, optional
        The number of epochs to train for (default is 25).
    batch_size : int, optional
        The batch size (default is 32).

    Returns
    -------
    None
    """

    input_dim = 40
    output_dim = 3
    hidden_dim = 64

    default_params = {
        "learning_rate": learning_rate,
        "batch_size": batch_size,
        "num_epochs": num_epochs,
        "hidden_dim": hidden_dim
    }
    params = {**default_params, **kwargs}

    model = DemonstratorNeuralNet(input_dim, hidden_dim, output_dim)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=params["learning_rate"])

    # Convert integer columns to float64 to handle missing values
    df = df.astype({col: 'float64' for col in df.select_dtypes(include='int').columns})

    dataset = MyDataset(df, ["Temp", "Zeit", "Druck"])
    dataloader = DataLoader(dataset, batch_size=params["batch_size"], shuffle=True)

    mlflow_dataset: PandasDataset = mlflow.data.from_pandas(df, source="http://localhost:5000/")

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
        input_example = torch.randn(1, input_dim).float().numpy()
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
    df = pd.DataFrame(raw_data)
    print(df.head())

    steps = [
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
                           "Flächenanteilmodifiziert"]),
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
    ]

    preprocessor = Pipeline(steps=steps, verbose=False)

    df = preprocessor.fit_transform(df)


    # Train the model
    train_model(df, num_epochs=100, batch_size=32)

    # Load the model from the MLflow repository
    model_uri = "models:/OpenHubDaysModel/1"
    model = mlflow.pytorch.load_model(model_uri)

    input_data = {
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
        # Training Label
        "Temp": 0, # Note these are included here pass the data through the pipeline and removed afterwards
        "Zeit": 0,
        "Druck": 0,
    }

    # Convert the input data to a DataFrame
    input_df = pd.DataFrame([input_data])
    # Preprocess the input data
    preprocessed_input = preprocessor.transform(input_df)
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
