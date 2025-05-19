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

        integrate_weather_data(irrigation_df, weather_df):
            Joins irrigation data with weather observations
            - Aligns timestamps and merges datasets
            - Handles duplicate observations
            Returns: Integrated DataFrame with enriched features

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
    
    def integrate_weather_data(self, irrigation_df, weather_df):
        """
        Integrates weather data with irrigation data based on timestamps
        """
        # Prepare weather data
        weather_df['timestamp'] = pd.to_datetime(weather_df['timestamp'])
        
        # Select useful columns from weather data
        weather_features = [
            'timestamp', 'barometricpressure', 'precipitation', 
            'relativehumidity', 'solarradiation', 'temperature',
            'uv_index', 'winddirection', 'windspeed'
        ]
        
        weather_df = weather_df[weather_features].copy()
        
        # Handle missing values in weather data
        for col in weather_features[1:]:
            if weather_df[col].dtype == object:
                # Convert string columns to numeric
                weather_df[col] = pd.to_numeric(weather_df[col], errors='coerce')
        
        # Merge datasets using nearest timestamp match
        # This handles cases where timestamps don't perfectly align
        merged_df = pd.merge_asof(
            irrigation_df.sort_values('timestamp'),
            weather_df.sort_values('timestamp'),
            on='timestamp',
            direction='nearest',
            tolerance=pd.Timedelta('1h')  # Accept matches within 1 hour
        )
        
        # Create weather-based features
        if 'temperature_y' in merged_df.columns:
            # Rename columns to avoid confusion
            merged_df = merged_df.rename(columns={
                'temperature_x': 'temperature_sensor',
                'temperature_y': 'temperature_weather',
                'relativehumidity': 'humidity_weather'
            })
        else:
            # If there's no column collision
            merged_df = merged_df.rename(columns={
                'relativehumidity': 'humidity_weather'
            })
            
        # Create derived features
        if 'temperature_weather' in merged_df.columns and 'precipitation' in merged_df.columns:
            # Evapotranspiration proxy (simplified)
            merged_df['evap_proxy'] = merged_df['temperature_weather'] * 0.5 - merged_df['precipitation'] * 5
            
            # Weather stress indicator
            merged_df['weather_stress'] = (
                (merged_df['temperature_weather'] > 30) * 2 + 
                (merged_df['humidity_weather'] < 30) * 1.5 +
                (merged_df['precipitation'] > 0) * -3
            )
        
        return merged_df

    def prepare_features(self, df):
       # Define feature columns based on available columns
        basic_features = ["temperatura", "humidade"]
        time_features = ["ano", "mes", "dia", "hora", "mes_sin", "mes_cos", "hora_sin", "hora_cos"]
        weather_features = []
        
        # Check for weather columns
        possible_weather_cols = [
            "precipitation", "barometricpressure", "solarradiation", 
            "temperature_weather", "humidity_weather", "windspeed",
            "evap_proxy", "weather_stress"
        ]
        
        for col in possible_weather_cols:
            if col in df.columns:
                weather_features.append(col)
        
        # Combine all available features
        all_features = basic_features + time_features + weather_features
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