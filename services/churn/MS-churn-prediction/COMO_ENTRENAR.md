# 🎯 Guía Rápida: Entrenar el Modelo de ML

## Pasos para entrenar el modelo:

### 1. Asegúrate de tener el CSV

Verifica que tienes el archivo:

```
data/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

### 2. Ejecuta el script de entrenamiento

```powershell
python train_model.py
```

**Lo que hace este script:**

- Lee el CSV
- Prepara los datos (limpia, convierte texto a números)
- Entrena un modelo Random Forest
- Guarda el modelo en `data/churn_model.pkl`
- Muestra la precisión del modelo (accuracy)

**Tiempo estimado:** 30 segundos a 2 minutos

### 3. ¿Cómo saber si funcionó?

Al finalizar deberías ver:

```
✅ Modelo guardado en: data/churn_model.pkl
✅ Información guardada en: data/model_info.pkl
✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE
```

### 4. Reinicia el servidor

```powershell
python -m app.main
```

**Deberías ver:**

```
✅ MLService inicializado con MODELO ENTRENADO (versión: v2.0_random_forest)
```

---

## ❓ ¿Qué cambia con el modelo entrenado?

### ANTES (Reglas simples):

```python
if tenure < 6:
    churn_score += 0.4
```

### DESPUÉS (Modelo ML):

```python
churn_probability = model.predict_proba(features)
```

El modelo **aprendió patrones** del CSV de Kaggle y hace predicciones **más precisas**.

---

## 📊 Ejemplo de uso

### Request al endpoint:

```json
POST /api/churn/predict
{
  "user_id": "USER_123",
  "features": {
    "tenure": 5,
    "MonthlyCharges": 85.0,
    "TotalCharges": 425.0,
    "Contract": "Month-to-month"
  }
}
```

### Response (con modelo entrenado):

```json
{
  "user_id": "USER_123",
  "churn_probability": 0.87,
  "risk_level": "HIGH",
  "risk_factors": ["Cliente nuevo (menos de 6 meses)", "Contrato mes a mes (sin compromiso)", "Cargo mensual elevado"]
}
```

---

## 🔄 ¿Y si no entreno el modelo?

**No problem!** El servicio funciona igual con reglas simples.

- El servidor detecta automáticamente si hay modelo entrenado
- Si NO hay, usa las reglas simples
- Si SÍ hay, usa el modelo Random Forest

---

## 🛠️ Troubleshooting

### Error: "No se encontró el archivo CSV"

- Verifica que el CSV esté en `data/` y se llame exactamente:
  `WA_Fn-UseC_-Telco-Customer-Churn.csv`

### Error al ejecutar train_model.py

- Asegúrate de estar en el directorio del proyecto
- Verifica que el entorno virtual esté activado

### El servidor no carga el modelo

- Verifica que existan los archivos:
  - `data/churn_model.pkl`
  - `data/model_info.pkl`
