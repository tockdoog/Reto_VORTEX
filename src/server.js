import express from "express";
import cors from "cors";
import { Router } from "express";
import dotenv from "dotenv";
import { verifyInternalToken } from "./middleware/internalAuth.js"
import routes from "./routes/index.js";

dotenv.config();
const ruta = Router();

const app = express();
const PORT = process.env.PORT || 4000;

app.use(express.json());
app.use(cors());

// app.use(verifyInternalToken);

// Rutas del microservicio
app.use("/", routes);

// 404
app.use((req, res) => {
  res.status(404).json({ error: "Ruta no encontrada" });
});

// Iniciar
app.listen(PORT, () => {
  console.log(`API Gateway escuchando en http://localhost:${PORT}`);
});
