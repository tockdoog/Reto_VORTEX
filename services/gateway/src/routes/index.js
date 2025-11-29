import { Router } from "express";
import rutaGateway from "./gateway.routes.js";
import rutaAuth from "./auth.routes.js";

const ruta = Router();

// Ruta de login (sin token)
ruta.use("/auth", rutaAuth);

// Rutas del gateway (protegidas opcionalmente)
ruta.use("/", rutaGateway);

export default ruta;
