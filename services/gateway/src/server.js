import express from "express";
import cors from "cors";
import routes from "./routes/index.js";
import { generalLimiter } from "../config/rateLimit.js";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(cors());

//  Aplicar limitador a TODAS las rutas del gateway
app.use(generalLimiter);

// Rutas
app.use("/", routes);

// 404
app.use((req, res) => {
  res.status(404).json({ error: "Ruta no encontrada" });
});

// Iniciar
app.listen(PORT, () => {
  console.log(`API Gateway escuchando en http://localhost:${PORT}`);
});
