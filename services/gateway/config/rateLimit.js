import rateLimit from "express-rate-limit";
import dotenv from "dotenv";
dotenv.config();

// Límite general del sistema
export const generalLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minuto
  max: process.env.RATELIMIT_IP,   // Máx 60 solicitudes/minuto por IP  .ENV
  message: {
    error: "Demasiadas solicitudes, intenta de nuevo más tarde."
  },
  standardHeaders: true,
  legacyHeaders: false
});

// Límite especial para rutas sensibles (login)
export const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 5,                   // Máx 5 intentos de login
  message: {
    error: "Demasiados intentos de inicio de sesión. Espera 15 minutos."
  },
  standardHeaders: true,
  legacyHeaders: false
});
