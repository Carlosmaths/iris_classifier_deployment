from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Crear la aplicación FastAPI
app = FastAPI(title="Iris Classifier API")

# Cargar el modelo entrenado
model = joblib.load('iris_model.pkl')

# Nombres de las clases
class_names = ['setosa', 'versicolor', 'virginica']


# Definir el formato de entrada usando Pydantic
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Ruta raíz
@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de clasificación de flores Iris",
        "endpoints": {
            "/predict": "POST - Hacer una predicción",
            "/docs": "GET - Documentación interactiva"
        }
    }


# Ruta para hacer predicciones
@app.post("/predict")
def predict(features: IrisFeatures):
    # Convertir los datos de entrada a un array numpy
    data = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]])

    # Hacer la predicción
    prediction = model.predict(data)
    prediction_proba = model.predict_proba(data)

    # Preparar la respuesta
    return {
        "prediction": class_names[prediction[0]],
        "prediction_class": int(prediction[0]),
        "probabilities": {
            "setosa": float(prediction_proba[0][0]),
            "versicolor": float(prediction_proba[0][1]),
            "virginica": float(prediction_proba[0][2])
        }
    }