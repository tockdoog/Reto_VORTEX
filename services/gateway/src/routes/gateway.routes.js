import { Router } from "express";
import { verifyToken } from "../middleware/auth.middleware.js";
import { callInternalService } from "../utils/internal-call.js"
import { recibirTicket } from "../controllers/ticket.controller.js";
import dotenv from "dotenv";
dotenv.config();

const routerGateway = Router();

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.get("/security", verifyToken, async (req, res) => {
  try {
    
    const response = await callInternalService(
      process.env.SECURITY_SERVICE_HOST,
      "GET"
    );

    res.json({
      gateway: "OK",
      fromMicroservice: response.data
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al microservicio",
      details: error.response?.data || error.message
    });
  }
});

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.post("/insertarticket", verifyToken, async (req, res) => {
  try {
    // Captura el body del cliente
    const data = req.body;

    const response = await callInternalService(
      process.env.DATA_SERVICE_HOST + "/api/data/tickets",
      "POST",
      data
    );

    res.json({
      gateway: "OK",
      fromMicroservice: response.data
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al microservicio",
      details: error.response?.data || error.message
    });
  }
});

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.get("/consultarticket/:id", verifyToken, async (req, res) => {
  try {
    const { id } = req.params; // <-- obtener ID

    const response = await callInternalService(
      `${process.env.DATA_SERVICE_HOST}/api/data/tickets/${id}`,
      "GET"
    );

    res.json({
      gateway: "OK",
      fromMicroservice: response.data
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al microservicio",
      details: error.response?.data || error.message
    });
  }
});

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.get("/analisis", verifyToken, async (req, res) => {
  try {

    const response = await callInternalService(
      `${process.env.DATA_SERVICE_HOST}/api/data/analytics`,
      "GET"
    );

    res.json({
      gateway: "OK",
      fromMicroservice: response.data
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al microservicio",
      details: error.response?.data || error.message
    });
  }
});

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.post("/generarrecomendacion", verifyToken, async (req, res) => {
  try {
    const { tipo, sentimiento, churn, insights } = req.body;

    if (!tipo || sentimiento === undefined || churn === undefined) {
      return res.status(400).json({
        error: "Faltan datos obligatorios: tipo, sentimiento, churn"
      });
    }

    // Llamar al microservicio Recommendations
    const response = await callInternalService(
      `${process.env.RECOMMENDATION_SERVICE_HOST}/api/recommendations/generate`,
      "POST",
      {
        tipo,
        sentimiento,
        churn,
        insights
      }
    );

    res.json({
      gateway: "OK",
      recomendaciones: response.data.recomendaciones,
      plantilla: response.data.plantilla
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al MS-Recommendation-Service",
      details: error.response?.data || error.message
    });
  }
});

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.get("/templates", verifyToken, async (req, res) => {
  try {

    const response = await callInternalService(
      `${process.env.RECOMMENDATION_SERVICE_HOST}/api/recommendations/templates`,
      "GET"
    );

    res.json({
      gateway: "OK",
      fromMicroservice: response.data
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al microservicio",
      details: error.response?.data || error.message
    });
  }
});

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.post("/evaluate", verifyToken, async (req, res) => {
  try {
    const { recommendationId, efectividad, comentario, usuario } = req.body;

    // Validación básica
    if (!recommendationId || !efectividad) {
      return res.status(400).json({
        success: false,
        message: "Faltan campos requeridos: recommendationId y efectividad."
      });
    }

    // Llamar al microservicio Recommendations
    const response = await callInternalService(
      `${process.env.RECOMMENDATION_SERVICE_HOST}/api/recommendations/evaluate`,
      "POST",
      {
        recommendationId,
        efectividad,
        comentario,
        usuario
      }
    );

    // Datos de evaluación procesados
    const evaluacion = {
      
    };

    res.json({
      gateway: "OK",
      recomendaciones: response.data.recomendaciones,
      plantilla: response.data.plantilla
    });

  } catch (error) {
    res.status(500).json({
      error: "Error al llamar al MS-Recommendation-Service",
      details: error.response?.data || error.message
    });
  }
});


// Ruta pública para probar (SIN llamar microservicio todavía)
routerGateway.post("/tickets/ingresar", verifyToken, recibirTicket);
 
export default routerGateway;