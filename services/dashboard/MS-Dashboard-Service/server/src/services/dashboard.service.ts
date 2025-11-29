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

      // Paso 1: Llamar a MS-Text-Analysis para seguridad (detección de phishing)
      const securityRes = await httpClient.post(`${envs.MS_SECURITY_URL}/api/security/detect-phishing`, {
        text: ticketText,
        ticket_id: ticketId,
      });
      const security = securityRes.data;

      // Notificar progreso
      io.emit("analysis:progress", { ticketId, step: 2, message: "Analizando texto y clasificación..." });
      console.log("2. Paralelizando análisis de texto y clasificación...");

      // Paso 2: Llamar a Text (sentiment) y Classification en paralelo
      const [textRes, classRes] = await Promise.all([
        httpClient.post(`${envs.MS_TEXT_URL}/api/text/sentiment`, { text: security.anonymizedText, ticket_id: ticketId }),
        httpClient.post(`${envs.MS_CLASSIFICATION_URL}/api/classification/predict`, { text: security.anonymizedText, ticket_id: ticketId })
      ]);
      const sentiment = textRes.data;
      const classification = {
        type: classRes.data.prediction,
        confidence: classRes.data.confidence,
      } as any;

      // Notificar progreso
      io.emit("analysis:progress", { ticketId, step: 3, message: "Calculando riesgo de Churn..." });
      console.log("3. Prediciendo Churn...");

      // Paso 3: Churn (con fallback si el MS no responde)
      let churnRisk: any = { score: 0, level: "BAJO" };
      try {
        const churnRes = await httpClient.post(`${envs.MS_CHURN_URL}/api/churn/predict`, {
          user_id: ticketId,
          features: {
            sentiment_score: sentiment.sentiment,
            num_tickets: 1,
          },
        });
        const churnData = churnRes.data;
        churnRisk = {
          score: Math.round(churnData.churn_probability * 100),
          level: churnData.risk_level === "HIGH" ? "ALTO" : churnData.risk_level === "MEDIUM" ? "MEDIO" : "BAJO",
        } as any;
      } catch (err) {
        const s = sentiment.sentiment ?? sentiment.score ?? 0;
        const approx = Math.max(0, Math.min(100, Math.round(((-s + 1) / 2) * 80)));
        churnRisk = {
          score: approx,
          level: approx > 66 ? "ALTO" : approx > 33 ? "MEDIO" : "BAJO",
          fallback: true,
        } as any;
        console.warn("Churn MS no disponible, usando fallback", err?.message || err);
      }

      // Notificar progreso
      io.emit("analysis:progress", { ticketId, step: 4, message: "Generando recomendaciones..." });
      console.log("4. Generando recomendaciones...");

      // Paso 4: Recomendaciones (placeholder basado en riesgo/sentimiento)
      const recommendationsMock = churnRisk.level === "ALTO"
        ? ["Activar gestor de cuenta", "Ofrecer incentivo de retención"]
        : sentiment.label === "negativo"
          ? ["Escalar a soporte senior", "Agendar sesión de seguimiento"]
          : ["Agradecer feedback", "Explorar upsell"];

      // Notificar finalización
      io.emit("analysis:complete", { ticketId, message: "Análisis completado" });

      // Armamos la respuesta final unificada
      return {
        ticketId,
        security,
        classification,
        sentiment,
        churnRisk,
        recommendations: recommendationsMock,
      };
    } catch (error) {
      console.error("Error en el servicio de dashboard:", error);
      getIO().emit("analysis:error", { message: "Falló el análisis del ticket" });
      throw new Error("Falló el análisis del ticket");
    }
  }

  async getOverview() {
    try {
      const insightsRes = await httpClient.get(`${envs.MS_ANALYTICS_URL}/api/analytics/insights`);
      const insights = insightsRes.data;
      return {
        totalTickets: 150,
        avgSentiment: 0.65,
        alerts: 3,
        topFactor: insights.top_factor,
        insights: insights.insights,
      };
    } catch (e) {
      return {
        totalTickets: 150,
        avgSentiment: 0.65,
        alerts: 3,
      };
    }
  }
}
