"""
    Handles loading dataset.

    Methods:
        load_data(path)
            Loads data and converts timestamps
            Returns: pandas.DataFrame with the data
"""
import pandas as pd
import numpy as np
from datetime import datetime

class DataLoader:
    def __init__(self, config):
        self.config = config

    def load_data(self, path):
        df = pd.read_csv(path, delimiter=';')
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M')
        return df
