import { Router } from "express";
import rutaGateway from "./gateway.routes.js";

const ruta = Router();

ruta.use("/", rutaGateway);

export default ruta;
