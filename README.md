# Smart Irrigation System

## Project Overview
This project implements a smart irrigation system that uses machine learning models to predict the optimal irrigation time based on environmental factors like temperature and humidity. The system includes data collection from sensors, model training, evaluation, and deployment to an Arduino microcontroller.

## Directory Structure
```
data/                           # Contains all data files and visualizations
├── dados_arduino_reais.csv     # Real data collected from Arduino sensors
├── dados_Dados_Gerados.csv     # Generated/synthetic data
├── correlation_matrix.png      # Correlation analysis visualization
├── boxplot.png                 # Data distribution visualization
└── *_feature_importance.png    # Feature importance visualizations

models/                         # Stores trained machine learning models
├── best_model.pkl              # Best performing model
├── imputer.pkl                 # Saved imputer for handling missing values
└── scaler.pkl                  # Saved scaler for feature normalization

src/                            # Source code
├── main.py                     # Main application entry point
├── arduino/                    # Arduino-related code
│   ├── Arduino_ExportCSV.ino   # Arduino sketch for data collection
│   ├── Arduino_ExportCSV.py    # Python script to receive and save Arduino data
│   └── modelo_arduino/         # Arduino implementation of ML models
│       ├── Modelo_Arduino.ino  # Main Arduino implementation
│       ├── LinearRegression.h  # Linear regression model in C++
│       ├── RandomForestRegressor.h/cpp # Random forest model in C++
│       ├── DecisionTreeRegressor.h     # Decision tree model in C++
│       └── XGBRegressor.h              # XGBoost model in C++
└── utils/                      # Utility modules
    ├── __init__.py             # Package initialization
    ├── config.py               # Configuration management
    ├── inferencia.py           # Inference utilities
    ├── model_evaluator.py      # Model evaluation utilities
    ├── model_trainer.py        # Model training utilities
    └── preprocessor.py         # Data preprocessing utilities
```

## Key Components

### 1. Data Collection (Arduino_ExportCSV.ino/py)
The system collects temperature and humidity data from an HTU21D sensor connected to an Arduino. The data is sent via serial communication to a Python script that:
- Reads the sensor values
- Calculates recommended irrigation time based on environmental conditions
- Stores the data in CSV files for model training

### 2. Data Preprocessing (preprocessor.py)
The `DataPreprocessor` class handles:
- Temporal feature extraction (year, month, day, hour)
- Cyclical encoding of time features using sine and cosine transformations
- Feature selection and preparation for model training
- Feature scaling and missing value imputation

### 3. Model Training (model_trainer.py)
The system trains multiple regression models to predict irrigation time:
- Linear Regression
- Random Forest Regression
- XGBoost Regression
- Decision Tree Regression

### 4. Model Evaluation (model_evaluator.py)
Models are evaluated using:
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- R² Score
- Feature importance analysis for tree-based models
- Correlation analysis of features

### 5. Model Export to Arduino (main.py)
The best-performing model is exported to Arduino-compatible C++ code:
- For Linear Regression, coefficients and intercepts are explicitly exported
- For other models, m2cgen library is used to convert models to C code

### 6. Arduino Implementation (Modelo_Arduino.ino)
The Arduino implementation:
- Reads sensor data in real-time
- Applies the exported model to predict optimal irrigation time
- Controls irrigation based on predictions

## Usage Instructions

### Training Models
Run the main script to train and evaluate models:
```bash
python src/main.py
```

This will:
1. Load and preprocess data from CSV files
2. Train multiple regression models
3. Evaluate and compare model performances
4. Export the best model to Arduino-compatible code

### Data Collection
To collect new data from Arduino:
1. Upload `Arduino_ExportCSV.ino` to your Arduino board
2. Connect the HTU21D sensor
3. Run the Python collection script:
   ```bash
   python src/arduino/Arduino_ExportCSV.py
   ```

### Deploying to Arduino
1. Upload the best model to Arduino:
   - Copy the appropriate header file (e.g., `LinearRegression.h`) to your Arduino IDE
   - Upload `Modelo_Arduino.ino` to your Arduino board
2. The Arduino will now predict optimal irrigation times based on real-time sensor data

## Model Calculation Logic

The system uses a base calculation for irrigation time:
```python
def calculate_irrigation_time(temperature, humidity):
    # Base irrigation time
    base_time = 1  # minutes
    
    # Temperature adjustment
    temp_factor = 0
    if temperature < 15:
        temp_factor = -2  # Reduce time on cold days
    elif 15 <= temperature < 25:
        temp_factor = 0   # Normal conditions
    elif 25 <= temperature < 30:
        temp_factor = 3   # Increase time on hot days
    elif 30 <= temperature < 35:
        temp_factor = 5   # Increase more on very hot days
    else:
        temp_factor = 8   # Significantly increase on extremely hot days
    
    # Humidity adjustment
    humidity_factor = 0
    if humidity > 80:
        humidity_factor = -3  # Reduce time on very humid days
    elif 60 <= humidity <= 80:
        humidity_factor = -1  # Slightly reduce on humid days
    elif 40 <= humidity < 60:
        humidity_factor = 0   # Normal conditions
    elif 20 <= humidity < 40:
        humidity_factor = 3   # Increase on dry days
    else:
        humidity_factor = 5   # Significantly increase on very dry days
    
    # Final calculation
    irrigation_time = base_time + temp_factor + humidity_factor
    
    # Ensure minimum time is at least 0
    return max(0, irrigation_time)
```

## Configuration (config.py)
The `Config` class manages central configuration:
- `RANDOM_STATE`: Seed for reproducibility (42)
- `TEST_SIZE`: Proportion of data used for testing (0.2)
- `MODEL_PATH`: Directory for saving trained models
- `DATA_PATH`: Directory for input data files
- `MODELS`: Dictionary of regression models with hyperparameters
- `MODELS_NAMES`: Mapping of model identifiers to class names

## Dependencies
- Python: scikit-learn, pandas, numpy, matplotlib, xgboost, m2cgen
- Arduino: Adafruit_HTU21DF library, Wire library
- Hardware: Arduino board, HTU21D temperature and humidity sensor

## Future Improvements
- Add soil moisture sensor for more accurate predictions
- Implement weather API integration for precipitation forecasting
- Add a web interface for system monitoring and control
- Implement IoT connectivity for remote monitoring
