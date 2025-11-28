import express from "express";
import { verifyInternalToken } from "./middleware/internalAuth.js";
import recommendationRoutes from "./routes/index.js";
import dotenv from "dotenv";

dotenv.config();
const app = express();
const PORT = process.env.PORT || 4005;

app.use(express.json());

// 🔐 Todo el microservicio requiere token interno del Gateway
// app.use(verifyInternalToken);

app.use("/", recommendationRoutes);

app.listen(PORT, () => {
  console.log(`MS-Recommendation-Service escuchando en http://localhost:${PORT}`);
});
