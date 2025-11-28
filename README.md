📌 MS-Classification-Service
Microservicio encargado de clasificar tickets de soporte en:
Correctivo (errores, bugs, fallas)
Evolutivo (mejoras, nuevas funcionalidades)
Forma parte de la arquitectura general del reto Hackathon de Vortex Soluciones.

🚀 Funcionalidad Principal
Este microservicio recibe un texto (ticket) y determina su tipo.
En futuras versiones incorporará un modelo de IA basado en:
TensorFlow / Keras
Embeddings o TF-IDF
Entrenamiento supervisado

🏗️ Tecnologías Utilizadas
Python 3
FastAPI
TensorFlow / Keras
Pandas / NumPy
MongoDB
Joblib
Docker (próxima integración)


🎯 RESUMEN
| Archivo / Carpeta    | Para qué sirve                             |
| -------------------- | ------------------------------------------ |
| **main.py**          | Arranca FastAPI y monta las rutas          |
| **api/**             | Los endpoints (predict, train, model-info) |
| **core/**            | Configuración, MongoDB, cargar modelo      |
| **ml/**              | Modelos, tokenizer y entrenamiento         |
| **utils/**           | Funciones auxiliares (limpieza de texto)   |
| **tests/**           | Pruebas del microservicio                  |
| **requirements.txt** | Librerías necesarias                       |
| **.gitignore**       | Qué no subir a GitHub                      |
| **README.md**        | Documentación del microservicio            |
