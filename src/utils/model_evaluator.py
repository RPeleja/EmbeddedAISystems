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
import pandas as pd

class ModelEvaluator:
    def evaluate_models(self, models, X_test, y_test):
        results = {}
        for name, model in models.items():
            y_pred = model.predict(X_test)
            y_pred = np.maximum(0, y_pred)  # Ensure non-negative
            
            results[name] = {
                'score': model.score(X_test, y_test),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred),
                'predictions': y_pred
            }
        return results

    def plot_results(self, results, y_test):
        # Helps visualize how well the model predicts the target.
        plt.figure(figsize=(10, 6))
        for name, result in results.items():
            plt.scatter(y_test, result['predictions'], label=name, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--')
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.legend()
        plt.title("Actual vs Predicted")
        plt.grid(True)
        plt.savefig(f"data/predictions.png")
        
        plt.figure(figsize=(10, 6))
        residuals_data = [
            pd.DataFrame({'Model': name, 'Error': y_test - result['predictions']})
            for name, result in results.items()
        ]
        all_residuals = pd.concat(residuals_data)
        sns.boxplot(data=all_residuals, x='Model', y='Error')
        plt.title("Error Distribution per Model")
        plt.axhline(0, color='k', linestyle='--')
        plt.grid(True)
        plt.savefig(f"data/boxplot.png")

        
    def plot_feature_importance(self, data_path, trained_models, tree_models, feature_columns):
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
