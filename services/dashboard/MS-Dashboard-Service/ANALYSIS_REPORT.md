# Análisis de Rutas MS-Dashboard-Service

## 1. Ruta `/export`

**Estado:** Se está "usando" (la ruta existe y responde), pero **no es funcionalmente real**.
**Por qué:** Actualmente devuelve un string CSV "hardcodeado" (datos falsos fijos en el código) dentro de `ExportController`.
**Cambios necesarios para integración:**

- **Conexión de Datos:** En lugar de tener el string fijo, el `ExportController` debe llamar a un servicio (ej. `DashboardService`) que a su vez consulte a la base de datos o a otros microservicios (`MS-Data`, `MS-Analytics`) para obtener los datos reales del periodo.
- **Generación Real:** Usar una librería para generar el CSV o PDF dinámicamente basado en esos datos reales.

## 2. Ruta `/overview`

**Estado:** Se está usando, pero también devuelve datos simulados (MOCK).
**Funcionamiento y "Recursividad":**

- **No es recursiva.** La confusión viene de que el controlador llama a una función con el mismo nombre en el servicio.
  _ `DashboardController.getOverview` llama a `DashboardService.getOverview`.
  _ Son dos clases diferentes (`Controller` vs `Service`). El `await` es necesario porque la llamada al servicio es asíncrona (aunque ahora devuelva datos fijos, en el futuro hará peticiones de red/DB).
  **Cambios necesarios para integración:**
- Eliminar el objeto estático en `DashboardService.getOverview`.
- Implementar llamadas HTTP (usando `httpClient`) a los microservicios que tienen la data maestra (probablemente `MS-Tickets` para conteos o `MS-Analytics` para métricas agregadas).

## 3. Rediseño de `/analyze`

**Problema Actual:** Está diseñado para recibir un **texto** manual y analizarlo en tiempo real.
**Nuevo Objetivo:** Traer todos los tickets del Gateway y mostrarlos con sus análisis.

**Idea de Implementación (Pasos a seguir):**

1.  **Cambiar Método HTTP:** Cambiar de `POST` a `GET` (ya que ahora vamos a "obtener" una lista, no a "enviar" un texto para procesar).
2.  **Eliminar Input de Texto:** Ya no necesitas `req.body.text`.
3.  **Flujo en `DashboardService`:**
    - **Paso 1: Obtener Tickets:** Llamar al Gateway (o directamente a `MS-Tickets` si el Gateway solo enruta) para obtener la lista de todos los tickets existentes.
      - `const tickets = await httpClient.get(url_gateway_tickets);`
    - **Paso 2: Enriquecer Datos (Pattern Aggregator):**
      - Iterar sobre la lista de tickets.
      - Para cada ticket, verificar si ya tiene datos de análisis (Churn, Seguridad, Sentimiento).
      - _Opción A (Si los datos ya están guardados):_ El endpoint de tickets ya debería devolver el ticket con sus metadatos de riesgo/churn si están en base de datos.
      - _Opción B (Si hay que calcular al vuelo - No recomendado para "todos"):_ Tendrías que llamar a los microservicios de IA para cada ticket, lo cual sería muy lento.
    - **Recomendación:** El Dashboard debería consultar una vista consolidada. Lo ideal es que cuando un ticket entra, se analiza y se guardan sus resultados. El Dashboard solo hace un `GET` de esos tickets ya enriquecidos.

**Resumen de cambios en código (sin escribir código):**

- En `dashboard.controller.ts`: Cambiar `analyzeTicket` para que no busque `text` y llame a un nuevo método del servicio, ej. `getAllAnalyzedTickets()`.
- En `dashboard.service.ts`: Crear `getAllAnalyzedTickets()` que haga un `fetch` a la API de Tickets/Gateway y retorne esa lista al frontend.
