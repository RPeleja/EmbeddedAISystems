"""
    Handles model evaluation and visualization of results.
    
    Methods:
        evaluate_models(models, X_test, y_test):
            Evaluates all models and computes performance metrics
            Returns: Dictionary containing for each model:
                - Predictions
                - Probabilities
                - Confusion Matrix
                - Classification Report
                - ROC AUC Score
            
        plot_results(results, y_test):
            Creates visualization of model performance
            - ROC curves for all models
            - Confusion matrices
            - Performance comparison plots
    
    Usage:
        evaluator = ModelEvaluator()
        results = evaluator.evaluate_models(trained_models, X_test, y_test)
        evaluator.plot_results(results, y_test)
"""

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np

class ModelEvaluator:
    def evaluate_models(self, models, X_test, y_test):
        results = {}
        for name, model in models.items():
            y_pred = model.predict(X_test)
            y_pred = np.maximum(0, y_pred)  # Ensure non-negative
            
            results[name] = {
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred),
                'predictions': y_pred
            }
        return results

    def plot_results(self, results, y_test):
        # Residual Plot
        plt.figure(figsize=(10, 6))
        for name, result in results.items():
            residuals = y_test - result['predictions']
            sns.histplot(residuals, kde=True, label=name)
        plt.legend()
        plt.title("Residual Distribution")
        plt.show()