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

// Ruta pública para probar (SIN llamar microservicio todavía)
routerGateway.post("/tickets/ingresar", verifyToken, recibirTicket);

export default routerGateway;