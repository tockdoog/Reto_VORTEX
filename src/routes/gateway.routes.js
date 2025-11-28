import { Router } from "express";
import { verifyToken } from "../middleware/auth.middleware.js";
import { callInternalService } from "../utils/internal-call.js"

const routerGateway = Router();

// Ruta protegida: solo usuarios autenticados pueden invocar microservicios
routerGateway.get("/security", verifyToken, async (req, res) => {
  try {
    
    const response = await callInternalService(
      "http://localhost:4000",
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

export default routerGateway;