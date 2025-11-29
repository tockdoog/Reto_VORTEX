# MS-Churn-Prediction-Service 🎯

Microservicio de predicción de abandono (churn) de usuarios utilizando Machine Learning.

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **MongoDB Atlas**: Base de datos en la nube
- **Scikit-learn**: Modelo de Machine Learning
- **Motor**: Driver asíncrono para MongoDB

## Instalación

1. Crea el entorno virtual:

```bash
python -m venv venv
```

2. Activa el entorno:

```bash
.\venv\Scripts\Activate  # Windows PowerShell
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` con:

```
PORT=4003
MONGODB_URL=tu_connection_string_aqui
DATABASE_NAME=churn_prediction_db
```

## Ejecución

```bash
python app/main.py
```

Servidor corriendo en: `http://localhost:4003`

## Endpoints

- `GET /` - Información del servicio
- `GET /health` - Estado del servicio
