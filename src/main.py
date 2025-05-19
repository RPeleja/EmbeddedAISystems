import logging
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.config import Config
from utils.preprocessor import DataPreprocessor
from utils.model_trainer import ModelTrainer
from utils.model_evaluator import ModelEvaluator
import joblib
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize components
    config = Config()
    preprocessor = DataPreprocessor()
    trainer = ModelTrainer(config)
    evaluator = ModelEvaluator()

    # Ensure DATA_PATH does not start with a slash
    data_path = config.DATA_PATH.lstrip('/\\')

    # Load irrigation data)
    irrigation_df = pd.read_csv(f"{data_path}dados_arduino.csv")
    logger.info(f"Irrigation data loaded with {len(irrigation_df)} rows")

    df = preprocessor.preprocess(irrigation_df)
    
    # Prepare feature set
    X, y = preprocessor.prepare_features(df)
    logger.info(f"Features prepared: {X.columns.tolist()}")
    
    # Split and transform
    X_train, X_test, y_train, y_test = trainer.split_data(X, y)
    X_train_scaled, X_test_scaled = preprocessor.fit_transform(X_train, X_test)

    # Train and evaluate
    trained_models = trainer.train_models(X_train_scaled, y_train)
    results = evaluator.evaluate_models(trained_models, X_test_scaled, y_test)
    
    # Find best model
    best_model_name = min(results, key=lambda model: results[model]['rmse'])
    best_rmse = results[best_model_name]['rmse']
    logger.info(f"Best model: {best_model_name} with RMSE: {best_rmse:.4f}")
    
    # Compare model performance
    for name, metrics in results.items():
        logger.info(f"{name:20} | RMSE: {metrics['rmse']:.4f} | MAE: {metrics['mae']:.4f} | R²: {metrics['r2']:.4f}")
    
    # # Plot results
    evaluator.plot_results(results, y_test)

    # Feature importance analysis for tree-based models
    tree_models = ['random_forest', 'gradient_boosting']
    feature_columns = X.columns
    # Ensure MODEL_PATH does not start with a slash
    model_path = config.MODEL_PATH.lstrip('/\\')

    for model_name in tree_models:
        if model_name in trained_models:
            model = trained_models[model_name]
            if hasattr(model, 'feature_importances_'):
                plt.figure(figsize=(10, 6))
                importances = model.feature_importances_
                indices = np.argsort(importances)
                plt.title(f'Feature Importance - {model_name}')
                plt.barh(range(len(indices)), importances[indices], color='b', align='center')
                plt.yticks(range(len(indices)), [feature_columns[i] for i in indices])
                plt.xlabel('Relative Importance')
                plt.tight_layout()
                plt.savefig(f"{data_path}{model_name}_feature_importance.png")

    # Save artifacts
    os.makedirs(model_path, exist_ok=True)
    joblib.dump(trained_models[best_model_name], f"{model_path}best_model.pkl")
    joblib.dump(preprocessor.scaler, f"{model_path}scaler.pkl")
    joblib.dump(preprocessor.imputer, f"{model_path}imputer.pkl")

    # Save feature columns list for future inference
    with open(f"{model_path}feature_columns.txt", 'w') as f:
        f.write(','.join(preprocessor.feature_columns))

    logger.info(f"All artifacts saved to {model_path}")


    # Carrega o modelo treinado
    model = joblib.load('models/best_model.pkl')

    # Extrai coeficientes e intercepto
    print("Coeficientes:", model.coef_)
    print("Intercepto:", model.intercept_)


if __name__ == "__main__":
    main()