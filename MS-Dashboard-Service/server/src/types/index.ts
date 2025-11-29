// Definimos la estructura de un Ticket
export interface Ticket {
  id: string;
  text: string;
  priority?: "LOW" | "MEDIUM" | "HIGH";
  category?: string;
  timestamp: string;
}

// Definimos la respuesta que esperamos del análisis completo
export interface AnalysisResult {
  ticketId: string;
  security: {
    isSafe: boolean;
    threatsDetected: string[];
    anonymizedText: string;
  };
  classification: {
    type: "CORRECTIVO" | "EVOLUTIVO";
    confidence: number;
  };
  sentiment: {
    score: number; // -1 a 1
    label: "POSITIVO" | "NEUTRO" | "NEGATIVO";
  };
  churnRisk: {
    score: number; // 0 a 100
    level: "BAJO" | "MEDIO" | "ALTO";
  };
  recommendations: string[];
}
