# Carpeta de Datos

## 📁 Estructura

Coloca aquí los archivos CSV para entrenar el modelo:

```
data/
├── churn_data.csv          # Dataset principal de Kaggle
├── README.md               # Este archivo
└── .gitkeep
```

## 📥 Datasets Recomendados de Kaggle

### 1. **Telco Customer Churn** (Más usado)

- **URL**: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- **Tamaño**: ~1MB (7,043 filas)
- **Columnas**: CustomerID, tenure, MonthlyCharges, TotalCharges, Churn (Yes/No)
- **Ideal para**: Empezar rápido, dataset limpio y bien documentado

### 2. **E-Commerce Customer Churn**

- **URL**: https://www.kaggle.com/datasets/ankitverma2010/ecommerce-customer-churn-analysis-and-prediction
- **Tamaño**: ~500KB
- **Ideal para**: Ecommerce/SaaS

### 3. **Bank Customer Churn**

- **URL**: https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction
- **Tamaño**: ~1MB (10,000 filas)
- **Ideal para**: Sector financiero

## 📝 Instrucciones

1. Ve a Kaggle y descarga el dataset
2. Renombra el archivo a `churn_data.csv`
3. Colócalo en esta carpeta: `/data/churn_data.csv`
4. ¡Listo! El código lo leerá automáticamente

## ⚠️ Nota

Los archivos `.csv` NO se suben a Git (están en `.gitignore`) para no ocupar espacio innecesario.
