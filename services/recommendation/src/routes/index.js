import { Router } from "express";
import rutaRecomendacion from "./recommendation.routes.js";

const ruta = Router();

// Rutas del gateway (protegidas opcionalmente)
ruta.use("/api/recommendations", rutaRecomendacion);

export default ruta;
