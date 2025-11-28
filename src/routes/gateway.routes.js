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

// Ruta pública para probar (SIN llamar microservicio todavía)
routerGateway.post("/tickets/ingresar", verifyToken, recibirTicket);

export default routerGateway;