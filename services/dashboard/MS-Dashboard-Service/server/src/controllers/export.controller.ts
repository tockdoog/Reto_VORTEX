import { Request, Response } from "express";

export class ExportController {
  // Endpoint: GET /api/dashboard/export
  async exportReport(req: Request, res: Response) {
    try {
      // En un caso real, aquí generaríamos un PDF o CSV con datos reales
      // Para el hackathon, devolvemos un CSV simple generado al vuelo

      const csvContent = `TicketID,Prioridad,Sentimiento,RiesgoChurn
TKT-123,ALTA,NEGATIVO,ALTO
TKT-124,MEDIA,NEUTRO,MEDIO
TKT-125,BAJA,POSITIVO,BAJO`;

      res.setHeader("Content-Type", "text/csv");
      res.setHeader("Content-Disposition", 'attachment; filename="reporte_dashboard.csv"');
      res.status(200).send(csvContent);
    } catch (error) {
      res.status(500).json({ error: "Error al exportar reporte" });
    }
  }
}
