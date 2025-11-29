# =================================================================
# SCRIPT DE ENTRENAMIENTO DEL MODELO DE CHURN
# =================================================================
# Este script ENTRENA un modelo de Machine Learning usando el CSV.
# Solo lo ejecutas UNA VEZ (o cuando quieras re-entrenar).

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("=" * 60)
print("ENTRENAMIENTO DE MODELO DE CHURN PREDICTION")
print("=" * 60)

# ══════════════════════════════════════════════════════════════
# PASO 1: Cargar el CSV
# ══════════════════════════════════════════════════════════════

print("\n📂 Paso 1: Cargando datos...")

# Buscar el archivo CSV en la carpeta data/
csv_path = "data/churn_data.csv"

if not os.path.exists(csv_path):
    print(f"❌ ERROR: No se encontró el archivo {csv_path}")
    print("Por favor verifica que el CSV esté en la carpeta data/ con el nombre 'churn_data.csv'")
    exit(1)

# pd.read_csv() lee un archivo CSV y lo convierte en un DataFrame
# DataFrame es como una tabla de Excel en Python
df = pd.read_csv(csv_path)

print(f"✅ Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
print(f"Primeras 5 filas:")
print(df.head())

# ══════════════════════════════════════════════════════════════
# PASO 2: Preparar los datos (Feature Engineering)
# ══════════════════════════════════════════════════════════════

print("\n🔧 Paso 2: Preparando datos...")

# Eliminar columna customerID (no sirve para predecir)
df = df.drop('customerID', axis=1)

# Convertir TotalCharges a numérico (a veces viene como texto)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Eliminar filas con valores faltantes
df = df.dropna()

# Convertir columnas categóricas a números
# (Machine Learning solo entiende números)
label_encoders = {}

for column in df.columns:
    if df[column].dtype == 'object':  # Si es texto
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

print(f"✅ Datos preparados: {len(df)} filas después de limpieza")

# ══════════════════════════════════════════════════════════════
# PASO 3: Separar Features (X) y Target (y)
# ══════════════════════════════════════════════════════════════

print("\n✂️  Paso 3: Separando variables...")

# X = Features (características del usuario)
# y = Target (lo que queremos predecir: Churn Yes/No)

X = df.drop('Churn', axis=1)  # Todas las columnas excepto Churn
y = df['Churn']  # Solo la columna Churn

print(f"✅ Features (X): {X.shape[1]} columnas")
print(f"✅ Target (y): {y.shape[0]} valores")

# ══════════════════════════════════════════════════════════════
# PASO 4: Dividir en Train y Test
# ══════════════════════════════════════════════════════════════

print("\n🔀 Paso 4: Dividiendo datos en entrenamiento y prueba...")

# train_test_split divide los datos en 2 grupos:
# - 80% para ENTRENAR el modelo
# - 20% para PROBAR qué tan bueno es

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,  # 20% para test
    random_state=42  # Semilla para reproducibilidad
)

print(f"✅ Entrenamiento: {len(X_train)} filas")
print(f"✅ Prueba: {len(X_test)} filas")

# ══════════════════════════════════════════════════════════════
# PASO 5: Entrenar el modelo
# ══════════════════════════════════════════════════════════════

print("\n🧠 Paso 5: Entrenando modelo Random Forest...")

# RandomForestClassifier es un algoritmo de ML muy bueno
# Es como tener muchos "árboles de decisión" votando juntos

model = RandomForestClassifier(
    n_estimators=100,  # Número de árboles en el bosque
    random_state=42,
    max_depth=10,  # Profundidad máxima de cada árbol
    n_jobs=-1  # Usar todos los cores del CPU
)

# .fit() es el método que ENTRENA el modelo
# Le das ejemplos y aprende los patrones
model.fit(X_train, y_train)

print("✅ Modelo entrenado exitosamente")

# ══════════════════════════════════════════════════════════════
# PASO 6: Evaluar el modelo
# ══════════════════════════════════════════════════════════════

print("\n📊 Paso 6: Evaluando precisión del modelo...")

# Hacer predicciones en los datos de prueba
y_pred = model.predict(X_test)

# Calcular precisión (accuracy)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Precisión del modelo: {accuracy * 100:.2f}%")
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# ══════════════════════════════════════════════════════════════
# PASO 7: Guardar el modelo
# ══════════════════════════════════════════════════════════════

print("\n💾 Paso 7: Guardando modelo...")

# Guardar el modelo en un archivo .pkl
model_path = "data/churn_model.pkl"
joblib.dump(model, model_path)

# Guardar también la información de las columnas
columns_info = {
    'feature_names': list(X.columns),
    'label_encoders': label_encoders
}
joblib.dump(columns_info, "data/model_info.pkl")

print(f"✅ Modelo guardado en: {model_path}")
print(f"✅ Información guardada en: data/model_info.pkl")

# ══════════════════════════════════════════════════════════════
# PASO 8: Probar una predicción de ejemplo
# ══════════════════════════════════════════════════════════════

print("\n🧪 Paso 8: Probando predicción de ejemplo...")

# Tomar la primera fila de test
sample = X_test.iloc[0:1]
prediction = model.predict(sample)[0]
probability = model.predict_proba(sample)[0]

print(f"Predicción: {'CHURN' if prediction == 1 else 'NO CHURN'}")
print(f"Probabilidad de Churn: {probability[1] * 100:.2f}%")

print("\n" + "=" * 60)
print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
print("=" * 60)
print("\nAhora puedes:")
print("1. Reiniciar el servidor: python -m app.main")
print("2. El servicio usará automáticamente el modelo entrenado")
