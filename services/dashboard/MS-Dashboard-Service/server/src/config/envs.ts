import { config } from "dotenv";

// Cargamos el archivo .env
config();

// Exportamos un objeto con todas las variables limpias
// Esto evita tener process.env por todos lados y nos permite validar si faltan variables
export const envs = {
    PORT: process.env.PORT || 4007,
    MS_SECURITY_URL: process.env.MS_SECURITY_URL || "http://localhost:4000",
    MS_TEXT_URL: process.env.MS_TEXT_URL || "http://localhost:4001",
    MS_CLASSIFICATION_URL: process.env.MS_CLASSIFICATION_URL || "http://localhost:4002",
    MS_CHURN_URL: process.env.MS_CHURN_URL || "http://localhost:4003",
    MS_ANALYTICS_URL: process.env.MS_ANALYTICS_URL || "http://localhost:4004",
    MS_RECOMMENDATION_URL: process.env.MS_RECOMMENDATION_URL || "http://localhost:4005",
    MS_DATA_URL: process.env.MS_DATA_URL || "http://localhost:4006",
};
