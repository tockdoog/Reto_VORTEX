import express from "express";
import cors from "cors";
import { Router } from "express";
import dotenv from "dotenv";
import routes from "./routes/index.js";
import { verifyInternalToken } from "./middleware/internalAuth.js";
import { connectDB } from '../config/database.js';
import mongoose from "mongoose"

dotenv.config();
const ruta = Router();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.json());
app.use(cors());

// Middleware para verificar si la BD está conectada
app.use((req, res, next) => {
  if (req.path === '/health') return next(); // Health check siempre disponible
  
  // Verificar conexión a MongoDB
  if (mongoose.connection.readyState !== 1) {
    return res.status(503).json({
      error: "Servicio de base de datos no disponible",
      message: "La base de datos no está conectada"
    });
  }
  next();
});

// Health check
app.get('/health', (req, res) => {
  const mongoose = require('mongoose');
  const dbStatus = mongoose.connection.readyState === 1 ? 'connected' : 'disconnected';
  
  res.json({
    status: 'OK',
    database: dbStatus,
    timestamp: new Date().toISOString()
  });
});

//Solo lo pueden ejecutar el gateway
app.use(verifyInternalToken);

// Rutas
app.use("/", routes);

// 404
app.use((req, res) => {
  res.status(404).json({ error: "Ruta no encontrada" });
});

// Iniciar servidor
const startServer = async () => {
  try {
    console.log('🔗 Conectando a la base de datos...');
    await connectDB();
    
    console.log('✅ Base de datos conectada exitosamente');
    
    app.listen(PORT, () => {
      console.log(`🚀 API Gateway escuchando en http://localhost:${PORT}`);
      console.log(`📊 Ambiente: ${process.env.NODE_ENV || 'development'}`);
      console.log(`❤️  Health check: http://localhost:${PORT}/health`);
    });

  } catch (error) {
    console.error('❌ Error al conectar con la base de datos:', error.message);
    console.log('⚠️  Iniciando servidor sin base de datos...');
    
    // Iniciar servidor incluso sin BD (para desarrollo)
    app.listen(PORT, () => {
      console.log(`🚀 API Gateway escuchando en http://localhost:${PORT} (sin BD)`);
      console.log('⚠️  Modo: Sin base de datos - Algunas funciones no estarán disponibles');
    });
  }
};

startServer();