"""
    Central configuration management for the "irrigation" project.

    Attributes:
        RANDOM_STATE (int): Seed for reproducibility (42)
        TEST_SIZE (float): Proportion of data used for testing (0.2)
        MODEL_PATH (str): Directory for saving trained models
        DATA_PATH (str): Directory for input data files
"""
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from xgboost import XGBRegressor

class Config:
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    MODEL_PATH = '/models/'
    DATA_PATH = '/data/'
    MODELS = {
        'linear_regression': LinearRegression(),
        'random_forest': RandomForestRegressor(
            n_estimators=100,
            random_state=RANDOM_STATE
        ),
        'xgboost': XGBRegressor(
            n_estimators=10,
            max_depth=3,
            learning_rate=0.1
        ),
        'decision_tree': DecisionTreeRegressor(
            max_depth=3,
            min_samples_leaf=3,
            max_leaf_nodes=10,
            random_state=RANDOM_STATE
        )
    }
    MODELS_NAMES = {
        'random_forest': 'RandomForestRegressor',
        'xgboost': 'XGBRegressor',
        'decision_tree': 'DecisionTreeRegressor',
        'linear_regression': 'LinearRegression'
    }