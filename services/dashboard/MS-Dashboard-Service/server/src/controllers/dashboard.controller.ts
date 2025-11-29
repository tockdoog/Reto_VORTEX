import { Request, Response } from "express";
import { DashboardService } from "../services/dashboard.service";

const dashboardService = new DashboardService();

export class DashboardController {
  // Endpoint: POST /api/dashboard/analyze
  async analyzeTicket(req: Request, res: Response) {
    try {
      const { text } = req.body;

      if (!text) {
        return res.status(400).json({ error: 'El campo "text" es requerido' });
      }

      const result = await dashboardService.analyzeTicket(text);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: "Error interno del servidor al analizar ticket" });
    }
  }

  // Endpoint: GET /api/dashboard/overview
  async getOverview(req: Request, res: Response) {
    try {
      const data = await dashboardService.getOverview();
      res.json(data);
    } catch (error) {
      res.status(500).json({ error: "Error al obtener resumen" });
    }
  }
}
