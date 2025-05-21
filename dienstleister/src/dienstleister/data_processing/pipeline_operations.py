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

    :param target: List of columns to drop
    :type target: list

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

        :param x: The Dataframe to transform
        :type x: pd.DataFrame

        :return: The transformed Dataframe
        :rtype: pd.DataFrame

        """
        return x.drop(self.target, axis=1)

class ColumnTypeSetter(BaseEstimator, TransformerMixin):
    """
    Set the specified columns to type float in the DataFrame.

    :param target: List of columns to set
    :type target: list

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

        :param x: The Dataframe to transform
        :type x: pd.DataFrame

        :return: The transformed Dataframe
        :rtype: pd.DataFrame

        """
        x[self.target] = x[self.target].astype(float)
        return x

class OneHotEncodePd(BaseEstimator, TransformerMixin):
    """
    One-hot encode the specified column.

    :param target: The column to one-hot encode.
    :type target: list

    :param prefix: The prefix to use for the one-hot encoded columns.
    :type prefix: str

    :param sep: The separator to use for the one-hot encoded columns.
    :type sep: str

    :param required_columns: A list of columns that should be present in the DataFrame after one-hot encoding.
    :type required_columns: list

    """

    def __init__(self, target: str, prefix: str, sep: str, required_columns=None):
        """
        Initialize the OneHotEncodePd object.

        """

        if required_columns is None:
            required_columns = []
        self.target = target
        self.prefix = prefix
        self.sep = sep
        self.required_columns = required_columns

    def fit(self, target):
        """
        Return self.
        """
        return self

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        """
        One-hot encode the specified column.

        :param x: The Dataframe to transform
        :type x: pd.DataFrame

        :return: The transformed Dataframe
        :rtype: pd.DataFrame

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
    One-hot encode the specified column into multiple categorical values.

    :param target: The column to one-hot encode.
    :type target: list

    :param prefix: The prefix to use for the one-hot encoded columns.
    :type prefix: str

    :param sep: The separator to use for the one-hot encoded columns.
    :type sep: str

    :param required_columns: A list of columns that should be present in the DataFrame after one-hot encoding.
    :type required_columns: list

    """

    def __init__(self, target: str, prefix: str, sep: str, required_columns=None):
        """
        Initialize the MultiOneHotEncodePd object.

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

        :param x: The Dataframe to transform
        :type x: pd.DataFrame

        :return: The transformed Dataframe
        :rtype: pd.DataFrame

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

    :param target: The column to normalize.
    :type target: str

    :param feature_range: The desired range of the transformed data.
    :type feature_range: tuple

    :param column_range: The actual range of the column data.
    :type column_range: tuple

    """

    def __init__(self, target: str, feature_range: tuple, column_range: tuple):
        """
        Initialize the CustomNormalizeCols object.

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

        :param x: The Dataframe to transform
        :type x: pd.DataFrame

        :return: The transformed Dataframe
        :rtype: pd.DataFrame

        """
        df = x.copy()  # don't modify original df
        col_min, col_max = self.column_range
        feature_min, feature_max = self.feature_range

        df[self.target] = df[self.target].apply(
            lambda x: feature_min + (x - col_min) * (feature_max - feature_min) / (col_max - col_min)
            if not pd.isna(x) else pd.NA
        )
        return df

