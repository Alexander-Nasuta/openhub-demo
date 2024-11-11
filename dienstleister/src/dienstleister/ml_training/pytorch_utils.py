import pandas as pd

import torch
from torch import nn, optim
from torch.utils.data import Dataset


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
