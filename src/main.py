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
import glob
import m2cgen as m2c

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_model_to_arduino(config, model, best_model_name):
        """
        Export the model to Arduino-compatible C++ code.
        """
        if best_model_name == 'linear_regression':
            # Extract coefficients and intercept
            coef = model.coef_.flatten().tolist()
            intercept = model.intercept_.item() if np.ndim(model.intercept_) == 0 else model.intercept_[0]

            print("Coefficients:", model.coef_)
            print("Intercept:", model.intercept_)

            # Generate the contents of the .h file
            export_name = config.MODELS_NAMES.get(best_model_name)
            export_path = f"src/arduino/modelo_arduino/{export_name}.h"

            with open(export_path, "w") as f:
                f.write("#pragma once\n")
                f.write("namespace Eloquent {\n")
                f.write("    namespace ML {\n")
                f.write("        namespace Port {\n")
                f.write("            class LinearRegression {\n")
                f.write("                public:\n")
                f.write("                    float predict(float *x) {\n")
                f.write("                        return dot(x,\n")
                
                # Write coefficients with line breaks
                for i, c in enumerate(coef):
                    end_char = ",\n" if i < len(coef) - 1 else "\n"
                    f.write(f"                            {c:.8f}{end_char}")
                
                f.write(f"                        ) + {intercept:.8f};\n")
                f.write("                    }\n\n")
                f.write("                protected:\n")
                f.write("                    float dot(float *x, ...) {\n")
                f.write(f"                        va_list w;\n")
                f.write(f"                        va_start(w, {len(coef)});\n")
                f.write("                        float dot = 0.0;\n")
                f.write(f"                        for (uint16_t i = 0; i < {len(coef)}; i++) {{\n")
                f.write("                            const float wi = va_arg(w, double);\n")
                f.write("                            dot += x[i] * wi;\n")
                f.write("                        }\n")
                f.write("                        return dot;\n")
                f.write("                    }\n")
                f.write("            };\n")
                f.write("        }\n")
                f.write("    }\n")
                f.write("}\n")

            logger.info(f"Linear regression model exported to {export_path}")
        else:
            # Dynamically construct export path based on best_model_name
            export_name = config.MODELS_NAMES.get(best_model_name)
            export_path = f"src/arduino/modelo_arduino/{export_name}.c"
            with open(export_path, "w") as f:
                f.write(m2c.export_to_c(model))
            logger.info(f"Model exported to {export_path}")
            
            
            # double score(double input)
            

def main():
    # Initialize components
    config = Config()
    preprocessor = DataPreprocessor()
    trainer = ModelTrainer(config)
    evaluator = ModelEvaluator()

    # Ensure DATA_PATH does not start with a slash
    data_path = config.DATA_PATH.lstrip('/\\')

    # Load irrigation data
    # Load and concatenate all matching files into a single DataFrame
    # Find all CSV files starting with 'dados_' in the directory
    csv_files = glob.glob(f"{data_path}dados_*.csv")
    
    irrigation_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
    logger.info(f"Irrigation data loaded with {len(irrigation_df)} rows from {len(csv_files)} files")
    
    # Preprocess data
    df = preprocessor.preprocess(irrigation_df)
    
    # Correlation analysis
    evaluator.plot_correlation_matrix(data_path, df)
    
    # Prepare feature set
    X, y = preprocessor.prepare_features(df)
    logger.info(f"Features prepared: {X.columns.tolist()}")
    
    # Split and transform
    X_train, X_test, y_train, y_test = trainer.split_data(X, y)
    X_train_scaled, X_test_scaled = preprocessor.fit_transform(X_train, X_test)

    # Train and evaluate
    trained_models = trainer.train_models(X_train_scaled, y_train)
    results = evaluator.evaluate_models(trained_models, X_test_scaled, y_test)
    
    # Find best model with minimum RMSE
    best_model_name = min(results, key=lambda model: results[model]['rmse'])

    # Ensure MODEL_PATH does not start with a slash
    model_path = config.MODEL_PATH.lstrip('/\\')
    
    # Compare model performance
    for name, metrics in results.items():
        logger.info(f"{name:20} | SCORE: {metrics['score']:.4f} | RMSE: {metrics['rmse']:.4f} | MAE: {metrics['mae']:.4f} | R²: {metrics['r2']:.4f}")
    
    if best_model_name in ['random_forest', 'xgboost', 'decision_tree']:
        # Feature importance analysis for tree-based models
        evaluator.plot_feature_importance(data_path, trained_models, [best_model_name], X.columns)
    
    # Plot results
    evaluator.plot_results(results, y_test)

    logger.info(f"Best model: {best_model_name} with SCORE: {results[best_model_name]['score'] * 100:.2f}%")

    # Save artifacts
    os.makedirs(model_path, exist_ok=True)
    joblib.dump(trained_models[best_model_name], f"{model_path}best_model.pkl")
    joblib.dump(preprocessor.scaler, f"{model_path}scaler.pkl")
    joblib.dump(preprocessor.imputer, f"{model_path}imputer.pkl")

    logger.info(f"All artifacts saved to {model_path}")

    # Load the trained model
    model = joblib.load('models/best_model.pkl')
    export_model_to_arduino(config, model, best_model_name)

if __name__ == "__main__":
    main()
