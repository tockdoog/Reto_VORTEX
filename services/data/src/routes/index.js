import { Router } from "express";
import rutaData from "./data.routes.js";

const ruta = Router();

// Ruta de login (sin token)
ruta.use("/api", rutaData);

export default ruta;
