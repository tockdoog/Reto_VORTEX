import { Router } from "express";
import { verifyToken } from "../middleware/auth.middleware.js";

const routerGateway = Router();

// Ruta libre
routerGateway.get("/", (req, res) => {
  res.json({ respuesta: "API Gateway funcionando" });
});

// Rutas protegidas
routerGateway.get("/servicios", verifyToken, (req, res) => {
  res.json({
    mensaje: "Acceso permitido",
    usuario: req.user
  });
});

export default routerGateway;
