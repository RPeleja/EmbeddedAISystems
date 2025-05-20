import pandas as pd
import joblib  # ou podes usar pickle
from preprocessor import DataPreprocessor

model = joblib.load("models/best_model.pkl")  # caminho para o teu modelo .pkl

dados_novos = pd.DataFrame({
    "data": ["2025-05-16 03:13:00"],
    "temperatura": [13.8],
    "humidade": [64.2]
})

preprocessor = DataPreprocessor()
df_processado = preprocessor.preprocess(dados_novos)

basic_features = ["temperatura", "humidade","ano", "dia_sin", "dia_cos","mes_sin", "mes_cos", "hora_sin", "hora_cos"]

X_novo = df_processado[basic_features]
predicoes = model.predict(X_novo)

print(f" Tempo de rega previsto: {predicoes[0]:.2f} minutos")