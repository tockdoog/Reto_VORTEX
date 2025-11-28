import { Router } from "express";
import { DashboardController } from "../controllers/dashboard.controller";
import { ExportController } from "../controllers/export.controller";

const router = Router();
const controller = new DashboardController();
const exportController = new ExportController();

// Definimos las rutas y las conectamos con el controlador
router.post("/analyze", controller.analyzeTicket.bind(controller));
router.get("/overview", controller.getOverview.bind(controller));
router.get("/export", exportController.exportReport.bind(exportController));

export default router;
