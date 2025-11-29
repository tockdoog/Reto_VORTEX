import { Router } from "express";
import { 
  createTicket, 
  getTicketById, 
  getAnalytics 
} from "../controllers/data.controller.js";

const router = Router();

// Endpoint para Almacenar tickets procesados
router.post("/data/tickets", createTicket);

// Endpoint para Recuperar ticket específico - GET /api/data/tickets/{id}
router.get("/data/tickets/:id", getTicketById);

// Endpoint para Datos para análisis agregado
router.get("/data/analytics", getAnalytics);

export default router;