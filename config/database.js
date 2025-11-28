// config/database.js
import mongoose from 'mongoose';
import dotenv from "dotenv";
dotenv.config();
export const connectDB = async () => {
  try {
    // Usar IPv4 en lugar de IPv6 para evitar problemas con ::1
    const mongoURI = process.env.MONGODB_URI || 'mongodb://127.0.0.1:27017/ticket_system';
    
    console.log('🔗 Conectando a MongoDB...');
    
    const conn = await mongoose.connect(mongoURI, {
      serverSelectionTimeoutMS: 5000, // Timeout de 5 segundos
    });

    console.log(`✅ MongoDB conectado: ${conn.connection.host}`);
    return conn;
    
  } catch (error) {
    console.error('❌ Error conectando a MongoDB:', error.message);
    
    // En desarrollo, no detener la aplicación
    if (process.env.NODE_ENV === 'development') {
      console.log('⚠️  Continuando sin base de datos (modo desarrollo)');
      return null;
    } else {
      // En producción, detener la aplicación
      throw error;
    }
  }
};
