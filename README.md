MS-Classification-Service

📋 Descripción
Microservicio responsable de clasificar tickets de soporte en categorías de mantenimiento (Correctivo vs Evolutivo) utilizando técnicas de Machine Learning. Este servicio forma parte del ecosistema RETO_VORTEX para la gestión inteligente de tickets.

🎯 Responsabilidades
Clasificación binaria de tickets (Correctivo/Evolutivo)
Entrenamiento y fine-tuning de modelos de ML
Almacenamiento de historial de predicciones
Monitoreo del performance del modelo
API REST para integración con otros microservicios

🏗️ Arquitectura
Tecnologías Principales
Python FastAPI - Framework web asíncrono
Scikit-learn - Machine Learning (MLPClassifier)
MongoDB - Almacenamiento de predicciones
Joblib - Serialización de modelos
Pydantic - Validación de datos

📊 Endpoints Principales
🔍 Clasificación
POST /api/classification/predict

🤖 Información del Modelo
GET /api/classification/model-info

🎓 Entrenamiento
POST /api/classification/train

🩺 Health Check
GET /health

Estructura de Proyecto
MS-Classification-Service/
├── app/
│   ├── services/
│   │   ├── classification_model.py  # Lógica del modelo ML
│   │   └── data_processor.py        # Procesamiento de datos
│   ├── config.py                    # Configuración
│   ├── database.py                  # Conexión MongoDB
│   ├── main.py                      # App FastAPI
│   └── models.py                    # Modelos Pydantic
├── models/                          # Modelos serializados
├── data/                           # Datos de entrenamiento
├── requirements.txt
├── run_uvicorn.py                  # Script de ejecución
└── test_api.py                     # Pruebas


🚀 Instalación y Ejecución
1. Clonar y Configurar
git clone <repository>
cd MS-Classification-Service
python -m venv env
source env/bin/activate  # Linux/Mac
# o
.\env\Scripts\activate  # Windows

2. Instalar Dependencias
pip install -r requirements.txt

4. Ejecutar Servicio
# Desarrollo
python run_uvicorn.py

# Producción
uvicorn app.main:app --host 0.0.0.0 --port 4002 --workers 4

Documentación Interactiva
Swagger UI: http://localhost:4002/docs
ReDoc: http://localhost:4002/redoc

