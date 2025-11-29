export const generateRecommendations = (data) => {
  const { tipo, sentimiento, churn, insights } = data;

  const recomendaciones = [];

  // Regla 1: Sentimiento negativo
  if (sentimiento < -0.3) {
    recomendaciones.push("Contactar al cliente en menos de 24 horas debido al sentimiento negativo.");
  }

  // Regla 2: Alto riesgo de churn
  if (churn > 60) {
    recomendaciones.push("Activar plan de retención y ofrecer beneficios adicionales.");
  }

  // Regla 3: Tipo Correctivo
  if (tipo === "Correctivo") {
    recomendaciones.push("Escalar el incidente al equipo de soporte nivel 2.");
  }

  // Regla 4: Insights detectados
  if (insights?.principalFactor) {
    recomendaciones.push(`Investigar el factor principal identificado: ${insights.principalFactor}`);
  }

  // Regla por defecto
  if (recomendaciones.length === 0) {
    recomendaciones.push("Realizar seguimiento regular y evaluar necesidades del cliente.");
  }

  return recomendaciones;
};
