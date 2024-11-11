import pandas as pd
import mlflow
from mlflow.data.pandas_dataset import PandasDataset
from sklearn.pipeline import Pipeline

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
import torch
from torch import nn, optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader



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

