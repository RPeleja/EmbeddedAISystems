"""
    Enhanced data preprocessing with weather data integration.

    Attributes:
        scaler: StandardScaler instance for feature scaling
        imputer: SimpleImputer instance for handling missing values

    Methods:
        preprocess(df):
            Performs initial data cleaning and feature engineering
            - Removes unnecessary columns
            - Extracts time features
            - Creates target variable
            Returns: Preprocessed DataFrame

        prepare_features(df):
            Separates features and target variables
            Returns: (features DataFrame, target Series)

        fit_transform(X_train, X_test):
            Applies scaling and imputation to training and test data
            Returns: (transformed X_train, transformed X_test)
"""

from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')
        self.feature_columns = None  

    def preprocess(self, df):
        # Convert 'data' to datetime if not already
        df['data'] = pd.to_datetime(df['data'])
        
        # Extract basic time features
        df['ano'] = df['data'].dt.year
        df['mes'] = df['data'].dt.month
        df['dia'] = df['data'].dt.day
        df['hora'] = df['data'].dt.hour
        
        # Cyclical encoding for time features
        ''' This tells the model:
            Hour 23 and 0 are close
            Hour 12 is opposite of hour 0 '''
            
        df['mes_sin'] = np.sin(2 * np.pi * df['data'].dt.month / 12)
        df['mes_cos'] = np.cos(2 * np.pi * df['data'].dt.month / 12)
        df['dia_sin'] = np.sin(2 * np.pi * df['data'].dt.day / 31)
        df['dia_cos'] = np.cos(2 * np.pi * df['data'].dt.day / 31)
        df['hora_sin'] = np.sin(2 * np.pi * df['data'].dt.hour / 24)
        df['hora_cos'] = np.cos(2 * np.pi * df['data'].dt.hour / 24)
        
        # Keep original datetime for potential merging
        df['timestamp'] = df['data']
        df = df.drop(columns=['data'])
        
        return df

    def prepare_features(self, df):
       # Define feature columns based on available columns
        basic_features = ["temperatura", "humidade"]
        #time_features = ["ano", "dia_sin", "dia_cos","mes_sin", "mes_cos", "hora_sin", "hora_cos"]
        
        # Combine all available features
        all_features = basic_features #+ time_features
        available_features = [f for f in all_features if f in df.columns]
        
        # Store feature columns for future use
        self.feature_columns = available_features
        
        # Extract features and target variable
        X = df[available_features]
        y = df["rega_necessaria_min"]
        return X, y

    def fit_transform(self, X_train, X_test):
        """
        Fits scaler/imputer on training data and transforms both sets.
        Returns: (X_train_transformed, X_test_transformed)
        """
        # Impute missing values
        X_train_imputed = self.imputer.fit_transform(X_train)
        X_test_imputed = self.imputer.transform(X_test)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train_imputed)
        X_test_scaled = self.scaler.transform(X_test_imputed)
        
        return X_train_scaled, X_test_scaled
    
    def transform_new_data(self, X_new):
        """Transform new data using pre-fitted scaler/imputer."""
        X_imputed = self.imputer.transform(X_new)
        X_scaled = self.scaler.transform(X_imputed)
        return X_scaled