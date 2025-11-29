# MS-Dashboard-Service 📊

Microservicio de Dashboard para análisis de tickets en tiempo real. Orquesta y unifica las respuestas de múltiples microservicios (Seguridad, Clasificación, Sentiment, Churn) proporcionando una interfaz web interactiva con actualizaciones en tiempo real mediante WebSockets.

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura](#arquitectura)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [WebSockets](#websockets)
- [Frontend](#frontend)
- [Contribuir](#contribuir)

## 🎯 Descripción General

El **MS-Dashboard-Service** es el microservicio central que actúa como orquestador de análisis de tickets. Coordina las siguientes funcionalidades:

### Funcionalidades Principales

1. **Análisis de Seguridad**: Detecta amenazas de phishing y anonimiza datos sensibles
2. **Clasificación de Tickets**: Determina si un ticket es CORRECTIVO o EVOLUTIVO
3. **Análisis de Sentimiento**: Evalúa el sentimiento del cliente (POSITIVO, NEUTRO, NEGATIVO)
4. **Predicción de Churn**: Calcula el riesgo de pérdida del cliente (BAJO, MEDIO, ALTO)
5. **Recomendaciones**: Genera acciones sugeridas basadas en el análisis

### Características

- ✅ **Comunicación en tiempo real** mediante WebSockets (Socket.IO)
- ✅ **Arquitectura modular** con separación de responsabilidades
- ✅ **Dashboard interactivo** con React + Material-UI
- ✅ **TypeScript** en backend y frontend
- ✅ **Orquestación de microservicios** con llamadas paralelas para optimizar rendimiento
- ✅ **Exportación de reportes** en formato JSON/CSV

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Cliente Web (React)                   │
│  - Dashboard Overview                                    │
│  - Analizador de Tickets                                │
│  - Conexión WebSocket                                   │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP (REST API) + WebSocket
                   ▼
┌─────────────────────────────────────────────────────────┐
│           MS-Dashboard-Service (Backend)                │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Controllers                                       │  │
│  │  - DashboardController                            │  │
│  │  - ExportController                               │  │
│  └──────────────┬────────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼────────────────────────────────────┐  │
│  │ Services                                          │  │
│  │  - DashboardService (Orquestador)                 │  │
│  └──────────────┬────────────────────────────────────┘  │
│                 │                                        │
│  ┌──────────────▼────────────────────────────────────┐  │
│  │ WebSocket (Socket.IO)                             │  │
│  │  - Notificaciones de progreso                     │  │
│  │  - Estado de análisis en tiempo real              │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────────┘
                  │
          ┌───────┴────────┬─────────────┬──────────────┐
          ▼                ▼             ▼              ▼
    ┌──────────┐    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ MS-      │    │ MS-Text  │  │ MS-Class │  │ MS-Churn │
    │ Security │    │ Analysis │  │ ification│  │ Predict  │
    └──────────┘    └──────────┘  └──────────┘  └──────────┘
```

### Flujo de Análisis

1. **Cliente envía ticket** → `POST /api/dashboard/analyze`
2. **Backend inicia análisis** → Emite `analysis:progress` vía WebSocket
3. **Paso 1**: Llamada a MS-Security (detección de phishing y anonimización)
4. **Paso 2**: Llamadas paralelas a MS-Text y MS-Classification
5. **Paso 3**: Llamada a MS-Churn con datos del sentimiento
6. **Paso 4**: Generación de recomendaciones
7. **Backend emite resultado** → `analysis:complete` con datos unificados
8. **Cliente actualiza UI** en tiempo real

## 🛠️ Tecnologías Utilizadas

### Backend

- **Node.js** + **TypeScript**
- **Express.js** - Framework web
- **Socket.IO** - WebSockets para comunicación en tiempo real
- **Axios** - Cliente HTTP para llamadas a otros microservicios
- **ts-node-dev** - Desarrollo con hot reload
- **dotenv** - Gestión de variables de entorno

### Frontend

- **React 19** + **TypeScript**
- **Vite** - Build tool y dev server
- **Material-UI (MUI)** - Componentes UI
- **Recharts** - Gráficos y visualizaciones
- **Socket.IO Client** - WebSocket en cliente
- **Zustand** - Gestión de estado global
- **Axios** - Cliente HTTP

## 📁 Estructura del Proyecto

```
MS-Dashboard-Service/
├── server/                          # Backend (Node.js + Express + TypeScript)
│   ├── src/
│   │   ├── config/
│   │   │   └── envs.ts              # Configuración de variables de entorno
│   │   ├── controllers/
│   │   │   ├── dashboard.controller.ts  # Controlador de endpoints de dashboard
│   │   │   └── export.controller.ts     # Controlador de exportación
│   │   ├── routes/
│   │   │   └── dashboard.routes.ts      # Definición de rutas HTTP
│   │   ├── services/
│   │   │   └── dashboard.service.ts     # Lógica de orquestación de análisis
│   │   ├── types/
│   │   │   └── index.ts                 # Tipos TypeScript (Ticket, AnalysisResult)
│   │   ├── utils/
│   │   │   └── httpClient.ts            # Cliente HTTP configurado
│   │   ├── websocket/
│   │   │   └── socket.ts                # Configuración de Socket.IO
│   │   └── index.ts                     # Punto de entrada del servidor
│   ├── .env                         # Variables de entorno (no versionado)
│   ├── .env.example                 # Ejemplo de variables de entorno
│   ├── package.json
│   └── tsconfig.json
│
├── client/                          # Frontend (React + TypeScript + Vite)
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout.tsx           # Layout principal con sidebar
│   │   ├── pages/
│   │   │   ├── Overview.tsx         # Dashboard con métricas generales
│   │   │   └── TicketAnalyzer.tsx   # Analizador de tickets individual
│   │   ├── services/
│   │   │   ├── api.ts               # Cliente Axios configurado
│   │   │   └── socket.ts            # Cliente Socket.IO
│   │   ├── store/
│   │   │   └── useStore.ts          # Estado global con Zustand
│   │   ├── App.tsx                  # Componente raíz
│   │   └── main.tsx                 # Punto de entrada
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── package.json                     # Scripts de desarrollo concurrente
├── .gitignore
└── README.md                        # Este archivo
```

## 🚀 Instalación

### Prerequisitos

- **Node.js** >= 18.x
- **npm** >= 9.x (o yarn/pnpm)

### Pasos

1. **Clonar el repositorio**

   ```bash
   cd Reto_VORTEX/MS-Dashboard-Service
   ```

2. **Instalar dependencias del proyecto raíz**

   ```bash
   npm install
   ```

3. **Instalar dependencias del servidor**

   ```bash
   cd server
   npm install
   cd ..
   ```

4. **Instalar dependencias del cliente**
   ```bash
   cd client
   npm install
   cd ..
   ```

## ⚙️ Configuración

### Variables de Entorno (Backend)

Crear archivo `server/.env` basado en `server/.env.example`:

```env
PORT=3001

# URLs de otros microservicios (descomentar cuando estén disponibles)
# MS_SECURITY_URL=http://localhost:5001
# MS_TEXT_URL=http://localhost:5002
# MS_CLASSIFICATION_URL=http://localhost:5003
# MS_CHURN_URL=http://localhost:5004
```

> **Nota**: Actualmente el servicio funciona con datos mock. Descomentar las URLs cuando los microservicios estén desplegados.

### Configuración del Cliente

La URL del backend se configura en `client/src/services/api.ts`:

```typescript
baseURL: "http://localhost:3001/api/dashboard";
```

## 💻 Uso

### Desarrollo

Ejecutar **servidor y cliente simultáneamente** desde la raíz del proyecto:

```bash
npm run dev
```

Este comando utiliza `concurrently` para lanzar:

- Backend en `http://localhost:3001`
- Frontend en `http://localhost:5173`

### Desarrollo Individual

**Solo Backend:**

```bash
cd server
npm run dev
```

**Solo Frontend:**

```bash
cd client
npm run dev
```

## 📡 API Endpoints

### Health Check

```http
GET /api/health
```

**Respuesta:**

```json
{
  "message": "server working"
}
```

### Analizar Ticket

```http
POST /api/dashboard/analyze
Content-Type: application/json

{
  "text": "Mi internet no funciona desde hace dos días y nadie me responde"
}
```

**Respuesta:**

```json
{
  "ticketId": "TKT-1732766008123",
  "security": {
    "isSafe": true,
    "threatsDetected": [],
    "anonymizedText": "Mi internet no funciona..."
  },
  "classification": {
    "type": "CORRECTIVO",
    "confidence": 0.95
  },
  "sentiment": {
    "score": 0.8,
    "label": "POSITIVO"
  },
  "churnRisk": {
    "score": 12,
    "level": "BAJO"
  },
  "recommendations": ["Enviar encuesta de satisfacción", "Ofrecer descuento en renovación"]
}
```

### Obtener Overview

```http
GET /api/dashboard/overview
```

**Respuesta:**

```json
{
  "totalTickets": 150,
  "avgSentiment": 0.65,
  "alerts": 3
}
```

### Exportar Reporte

```http
GET /api/dashboard/export?format=json
```

Descarga un archivo con el reporte de análisis.

## 🔌 WebSockets

El servidor emite los siguientes eventos via Socket.IO:

### Eventos del Servidor → Cliente

| Evento              | Payload                       | Descripción                            |
| ------------------- | ----------------------------- | -------------------------------------- |
| `analysis:progress` | `{ ticketId, step, message }` | Actualización de progreso del análisis |
| `analysis:complete` | `{ ticketId, message }`       | Análisis completado exitosamente       |
| `analysis:error`    | `{ message }`                 | Error durante el análisis              |

### Ejemplo de Uso en Cliente

```typescript
import { io } from "socket.io-client";

const socket = io("http://localhost:3001");

socket.on("analysis:progress", (data) => {
  console.log(`Paso ${data.step}: ${data.message}`);
});

socket.on("analysis:complete", (data) => {
  console.log("Análisis completado!", data);
});
```

## 🎨 Frontend

### Vistas Principales

#### 1. Overview (Dashboard)

- **Métricas clave**: Total de tickets, sentimiento promedio, alertas
- **Gráficos**: Distribución de sentimientos, evolución temporal
- **Cards informativos**: Resumen visual de KPIs

#### 2. Ticket Analyzer

- **Formulario**: Input de texto para tickets
- **Análisis en tiempo real**: Notificaciones de progreso
- **Resultados**: Visualización detallada de todos los análisis
- **Badges**: Clasificación, sentimiento, riesgo de churn

### Temas y Estilos

Material-UI con tema personalizado:

- **Primary**: `#2563eb` (Azul moderno)
- **Secondary**: `#7c3aed` (Violeta)
- **Background**: `#f8fafc` (Gris claro)
- **Tipografía**: Inter, Roboto

## 🤝 Contribuir

### Guía de Contribución

1. **Fork** del repositorio
2. Crear rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit de cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abrir **Pull Request**

### Convenciones de Código

- **TypeScript** estricto
- **ESLint** para linting
- Nombres de variables en **camelCase**
- Nombres de componentes en **PascalCase**
- Comentarios descriptivos en español

### Roadmap

- [ ] Integración con microservicios reales (actualmente usa mocks)
- [ ] Autenticación y autorización
- [ ] Persistencia de datos históricos
- [ ] Tests unitarios y de integración
- [ ] Dashboard de administración
- [ ] Soporte multi-idioma
- [ ] Exportación a PDF
- [ ] Notificaciones push
