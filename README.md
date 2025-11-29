📝 MS-Text-Analysis-Service
🎯 Descripción
Microservicio especializado en Procesamiento de Lenguaje Natural (NLP) para análisis de texto en español. Este servicio es parte fundamental del sistema de soporte inteligente de Vortex Soluciones.

🚀 Funcionalidades Principales
1. Análisis de Sentimiento
Clasifica texto en: positivo, neutral o negativo
Proporciona scores de confianza (-1 a 1)
Optimizado específicamente para español


2. Tokenización y Limpieza de Texto
Divide texto en tokens (palabras)
Remueve stop words automáticamente
Lematización opcional
Limpieza de caracteres especiales

3. Vectorización de Texto
Convierte texto a vectores numéricos usando HashingVectorizer
Métodos disponibles: TF-IDF y CountVectorizer
Reducción automática de dimensionalidad

4. Análisis Lingüístico Avanzado
Conteo de palabras y oraciones
Diversidad léxica
Score de legibilidad
Métricas de complejidad textual

🛠 Tecnologías Implementadas
FastAPI: Framework web moderno y rápido
NLTK & spaCy: Procesamiento de lenguaje natural
Scikit-learn: Vectorización y modelos ML
HashingVectorizer: Vectorización sin necesidad de entrenamiento
MongoDB: Almacenamiento de logs y análisis
TextBlob: Análisis de sentimiento (fallback)

🎨 Arquitectura del Servicio
Ticket Input → Limpieza → Análisis → Vectorización → Output
     ↓           ↓          ↓           ↓           ↓
   Texto      Tokens    Sentimiento   Vectores   Características

Instalación y Ejecución
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servicio
python run_uvicorn.py

# O directamente con uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 4001 --reload

🎯 ¡Servicio listo para integración en el flujo principal del hackathon!

📚 Documentación interactiva disponible en: http://localhost:4001/docs