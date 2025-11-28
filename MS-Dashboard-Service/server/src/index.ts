import express from "express";
import { createServer } from "http";
import { config } from "dotenv";
import cors from "cors";
import dashboardRoutes from "./routes/dashboard.routes";
import { initSocket } from "./websocket/socket";

config(); // Cargar variables de entorno

const app = express();
const httpServer = createServer(app); // Creamos servidor HTTP nativo para soportar WS
const PORT = process.env.PORT || 3001;

// Inicializar WebSockets
initSocket(httpServer);

// Middleware
app.use(cors());
app.use(express.json());

// Rutas
app.use("/api/dashboard", dashboardRoutes);

app.get("/api/health", (req, res) => {
  res.status(200).json({ message: "server working" });
});

// Usamos httpServer.listen en lugar de app.listen
httpServer.listen(PORT, () => console.log(`Server running on port ${PORT}`));
