"""
    Central configuration management for the "irrigation" project.

    Attributes:
        RANDOM_STATE (int): Seed for reproducibility (42)
        TEST_SIZE (float): Proportion of data used for testing (0.2)
        MODEL_PATH (str): Directory for saving trained models
        DATA_PATH (str): Directory for input data files
"""
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

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
        'gradient_boosting': GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.05,
            max_depth=5,
            random_state=RANDOM_STATE
        ),
        'svr': SVR(
            kernel='rbf',
            C=10.0,
            epsilon=0.1,
            gamma='scale'
        )
    }