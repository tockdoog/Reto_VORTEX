import { envs } from "../config/envs";
import { httpClient } from "../utils/httpClient";
import { AnalysisResult, Ticket } from "../types";

import { getIO } from "../websocket/socket";

export class DashboardService {
  // Método principal: Orquesta el análisis completo
  async analyzeTicket(ticketText: string): Promise<AnalysisResult> {
    try {
      const io = getIO();
      const ticketId = `TKT-${Date.now()}`;

      // Notificar inicio
      io.emit("analysis:progress", { ticketId, step: 1, message: "Iniciando análisis de seguridad..." });
      console.log("1. Iniciando análisis de seguridad...");

      // Paso 1: Llamar a MS-Security (Simulado por ahora)
      // const securityRes = await httpClient.post(`${envs.MS_SECURITY_URL}/api/security/detect-phishing`, { text: ticketText });

      // MOCK
      const securityMock = { isSafe: true, threatsDetected: [], anonymizedText: ticketText };

      // Notificar progreso
      io.emit("analysis:progress", { ticketId, step: 2, message: "Analizando texto y clasificación..." });
      console.log("2. Paralelizando análisis de texto y clasificación...");

      // Paso 2: Llamar a Text y Classification en paralelo
      /*
      const [textRes, classRes] = await Promise.all([
        httpClient.post(`${envs.MS_TEXT_URL}/api/text/sentiment`, { text: securityMock.anonymizedText }),
        httpClient.post(`${envs.MS_CLASSIFICATION_URL}/api/classification/predict`, { text: securityMock.anonymizedText })
      ]);
      */

      const textMock = { sentiment: { score: 0.8, label: "POSITIVO" } };
      const classMock = { type: "CORRECTIVO", confidence: 0.95 };

      // Notificar progreso
      io.emit("analysis:progress", { ticketId, step: 3, message: "Calculando riesgo de Churn..." });
      console.log("3. Prediciendo Churn...");

      // Paso 3: Churn
      // const churnRes = await httpClient.post(`${envs.MS_CHURN_URL}/api/churn/predict`, { sentiment: textMock.sentiment.score });
      const churnMock = { score: 12, level: "BAJO" };

      // Notificar progreso
      io.emit("analysis:progress", { ticketId, step: 4, message: "Generando recomendaciones..." });
      console.log("4. Generando recomendaciones...");

      // Paso 4: Recomendaciones
      const recommendationsMock = ["Enviar encuesta de satisfacción", "Ofrecer descuento en renovación"];

      // Notificar finalización
      io.emit("analysis:complete", { ticketId, message: "Análisis completado" });

      // Armamos la respuesta final unificada
      return {
        ticketId,
        security: securityMock,
        classification: classMock as any,
        sentiment: textMock.sentiment as any,
        churnRisk: churnMock as any,
        recommendations: recommendationsMock,
      };
    } catch (error) {
      console.error("Error en el servicio de dashboard:", error);
      getIO().emit("analysis:error", { message: "Falló el análisis del ticket" });
      throw new Error("Falló el análisis del ticket");
    }
  }

  async getOverview() {
    // Aquí llamaríamos a MS-Data o MS-Analytics para obtener métricas generales
    return {
      totalTickets: 150,
      avgSentiment: 0.65,
      alerts: 3,
    };
  }
}
