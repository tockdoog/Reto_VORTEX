# Reto_VORTEX
Este espacio se generará con el proceso del reto bajo el área de Talento Tech
🚀 VORTEX – Intelligent Ticket Risk & Support AI

Hackathon Challenge – Microservices Architecture

📌 Descripción General del Proyecto
Este proyecto implementa una arquitectura de microservicios orientada a procesar tickets de soporte de clientes y generar alertas de riesgo proactivas para el Account Manager.
La solución utiliza IA, análisis de texto, clasificación automática, detección de amenazas, predicción de churn y recomendaciones inteligentes, siguiendo las necesidades del reto planteado por Vortex.

🎯 Objetivos Principales del Sistema
1️⃣ Clasificación automática de tickets
Determina si un ticket es correctivo (errores, bugs) o evolutivo (nuevas funciones).
2️⃣ Predicción de riesgo de Churn
Predice si el cliente está en riesgo de no renovar contrato.
3️⃣ Detección de amenazas de ciberseguridad
Identifica phishing, datos sensibles y contenido malicioso.
4️⃣ Análisis de texto avanzado
Tokenización, vectorización, sentimiento y features lingüísticas.
5️⃣ Recomendaciones automáticas para el Account Manager
Sugiere acciones concretas basadas en riesgo, tono, historial y criticidad.
6️⃣ Dashboard interactivo
Muestra insights, métricas, tendencias y alertas inteligentes.

🏛️ Arquitectura General del Sistema
   ┌──────────────────┐
   │   API Gateway     │
   └──────┬───────────┘
          │ Ticket
          ▼
┌───────────────────────────────┐
│    MS-Security-Service        │ ← phishing, anonimización, amenazas
└───────────────┬──────────────┘
                │ texto limpio
                ▼
┌───────────────────────────────┐
│  MS-Text-Analysis-Service     │ ← NLP, TF-IDF, embeddings
└───────────────┬──────────────┘
                │ features NLP
                ▼
┌───────────────────────────────┐
│ MS-Classification-Service     │ ← correctivo/evolutivo
└───────────────┬──────────────┘
                │ riesgo base
                ▼
┌───────────────────────────────┐
│ MS-Churn-Prediction-Service   │ ← churn score
└───────────────┬──────────────┘
                │ analytics data
                ▼
┌───────────────────────────────┐
│   MS-Analytics-Service        │ ← insights, correlaciones
└───────────────┬──────────────┘
                │ alertas
                ▼
┌───────────────────────────────┐
│ MS-Recommendation-Service     │ ← recomendaciones
└───────────────┬──────────────┘
                │ resultados finales
                ▼
┌───────────────────────────────┐
│      MS-Data-Service          │ ← almacenamiento total
└───────────────┬──────────────┘
                ▼
     MS-Dashboard-Service


🔥 Lista Completa de Microservicios
1. 🛡️ MS-Security-Service
Responsabilidad:
Detección de amenazas, anonimización y análisis de seguridad.

2. 🧠 MS-Text-Analysis-Service
Responsabilidad:
Procesamiento de lenguaje natural (NLP).

3. 🧩 MS-Classification-Service
Responsabilidad:
Clasificar tickets en correctivo / evolutivo.

4. 📉 MS-Churn-Prediction-Service
Responsabilidad:
Predicción de riesgo de cancelación de contrato (0–100%).

5. 📊 MS-Analytics-Service
Responsabilidad:
Insights, correlaciones y análisis estadístico.

6. 🤖 MS-Recommendation-Service
Responsabilidad:
Recomendaciones accionables basadas en los análisis.

7. 📈 MS-Dashboard-Service
Responsabilidad:
Visualización final para el usuario.

8. 🕸️ API Gateway
Responsabilidad:
Punto único de entrada al ecosistema.

9. 💾 MS-Data-Service
Responsabilidad:
Almacenamiento unificado de todos los procesos.

🔁 Flujo Completo de Procesamiento
Ticket → Gateway → Security → Text Analysis → Classification → Churn → Analytics → Recommendations → Data → Dashboard
