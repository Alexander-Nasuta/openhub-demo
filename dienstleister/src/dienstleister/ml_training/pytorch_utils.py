import pandas as pd

import torch
from torch import nn, optim
from torch.utils.data import Dataset


class MyDataset(Dataset):
    """
    A custom dataset for the pytorch regression service.

    :param df: The dataframe containing the data.
    :type df: pd.DataFrame

    :param prediction_columns: The columns to be used as prediction targets.
    :type prediction_columns: list

    """

    def __init__(self, df: pd.DataFrame, prediction_columns: list):
        """
        Initialize the dataset.

        """
        self.df = df
        self.prediction_columns = prediction_columns

    def __len__(self):
        """
        Return the length of the dataset.

        :return: The length of the dataset.
        :rtype: int

        """
        return len(self.df)

    def __getitem__(self, idx):
        """
        Get an item from the dataset.

        :param idx: The index of the item to get.
        :type idx: int

        :return: The input and output data.
        :rtype: tuple

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

    :param input_dim: Dimension of the input layer.
    :type input_dim: int

    :param hidden_dim: Dimension of the hidden layers.
    :type hidden_dim: int

    :param output_dim: Dimension of the output layer.
    :type output_dim: int

    :param args: Positional arguments passed to the superclass or internal use.

    :param kwargs: Arbitrary keyword arguments, allowing \
                   for extensibility or forwarding to the\
                    superclass constructor or other components.

    """

    def __init__(self, input_dim, hidden_dim, output_dim, *args, **kwargs):
        """
        Initialize the network.

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

        :param x: The input to the network.

        :return: The output of the network.
        :rtype: torch.Tensor

        """
        x = torch.relu(self.layer_1(x))
        x = torch.relu(self.layer_2(x))
        x = torch.relu(self.layer_3(x))
        x = torch.relu(self.layer_4(x))
        x = self.layer_5(x)
        return x
