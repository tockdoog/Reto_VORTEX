🧠 MS-Classification-Service
Microservicio encargado de clasificar tickets de soporte en dos categorías:Correctivo (errores, bugs, fallas)
Correctivo → errores, caídas, fallas
Evolutivo → mejoras, nuevas funciones, cambios solicitados
Este servicio forma parte del ecosistema de microservicios del reto Hackathon Vortex Soluciones 2025.


🚀 Funcionalidad Principal
El servicio expone un endpoint:
POST → /api/classification/predict
Recibe un ticket de soporte y:
Limpia el texto
Tokeniza con el tokenizer entrenado
Usa el modelo TensorFlow (classifier.h5)
Determina si el ticket es:
correctivo
evolutivo
Guarda la predicción en MongoDB
Devuelve la etiqueta y el nivel de confianza
Ejemplo de respuesta:
{
  "label": "correctivo",
  "confidence": 0.8421,
  "input_text": "El sistema no permite iniciar sesión"
}

🧩 🆕 Estructura estándar del Ticket (JSON unificado)
Para estandarizar la entrada de datos, cada ticket debe seguir este formato:
{
  "ticket_id": "TS-2025-01142",
  "cliente": "GlobalTech Solutions",
  "proyecto": "Sistema de Gestión Logística v3.1",
  "fecha": "2025-11-29",
  "contacto_nombre": "María González",
  "contacto_correo": "maria.gonzalez@globaltech.com",
  "contacto_telefono": "+57 301 654 3210",
  "asunto": "Error crítico en módulo de facturación tras última actualización",
  "descripcion": "Texto completo del ticket aquí..."
}

Para el modelo de IA, el campo usado para clasificación es:
descripcion
Pero se pueden usar combinaciones (asunto + descripción) si se quiere mejorar el dataset.

🏗️ Arquitectura del Microservicio
Reto_VORTEX/
│
├── app/
│   ├── api/
│   │   ├── predict.py
│   │   ├── train.py
│   │   └── model_info.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── model_loader.py
│   │   └── mongo.py
│   │
│   ├── ml/
│   │   ├── dataset.csv
│   │   ├── classifier.h5        (se genera después del entrenamiento)
│   │   └── tokenizer.pkl        (se genera después del entrenamiento)
│   │
│   ├── utils/
│   │   └── preprocess.py
│   │
│   └── main.py
│
├── requirements.txt
├── .gitignore
├── README.md
└── venv/                  (NO se sube a Git)




📦 Tecnologías Utilizadas
fastapi
uvicorn
pydantic
pymongo
python-dotenv
pandas
numpy
joblib
tensorflow==2.12.1



🎯 Resumen de Archivos y Carpetas
| Archivo / Carpeta    | Descripción                                  |
| -------------------- | -------------------------------------------- |
| **main.py**          | Arranca FastAPI, registra rutas              |
| **api/**             | Los endpoints (`predict`, `train`, `status`) |
| **core/**            | Config, carga de modelo, conexión a Mongo    |
| **ml/**              | Dataset, entrenamiento, modelo final         |
| **utils/**           | Limpieza y manejo del texto                  |
| **requirements.txt** | Dependencias del microservicio               |
| **Dockerfile**       | Imagen Docker para despliegue                |
| **README.md**        | Este documento                               |


⚙️ Cómo correr el proyecto (entorno virtual)
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

