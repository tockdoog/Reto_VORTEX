import { Router } from "express";
import { generateRecommendations } from "../rules/recommendation.engine.js";
import nunjucks from "nunjucks";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Inicializa plantillas
nunjucks.configure(path.join(__dirname, "../templates"), { autoescape: true });

const router = Router();

router.post("/generate", (req, res) => {
  const { tipo, sentimiento, churn, insights } = req.body;

  const recomendaciones = generateRecommendations({
    tipo,
    sentimiento,
    churn,
    insights
  });

  // Renderizar plantilla
  const mensaje = nunjucks.render("default_template.njk", {
    recomendaciones,
    tipo,
    sentimiento,
    churn
  });

  res.json({
    recomendaciones,
    plantilla: mensaje
  });
});


router.get("/templates", (req, res) => {
  try {
    const templatesPath = path.resolve("src/templates");
    console.log(templatesPath);
    
    // Leer archivos del directorio
    const files = fs.readdirSync(templatesPath);

    // Filtrar solo .njk
    const templates = files
      .filter(file => file.endsWith(".njk"))
      .map(file => {
        const filePath = path.join(templatesPath, file);
        const content = fs.readFileSync(filePath, "utf8");

        return {
          name: file,
          preview: content.substring(0, 200) + "..." // muestra primeros 200 chars
        };
      });

    res.json({ templates });

  } catch (error) {
    res.status(500).json({
      error: "Error al leer las plantillas",
      details: error.message
    });
  }
});


router.post("/evaluate", async (req, res) => {
  try {
    const { recommendationId, efectividad, comentario, usuario } = req.body;

    // Validación básica
    if (!recommendationId || !efectividad) {
      return res.status(400).json({
        success: false,
        message: "Faltan campos requeridos: recommendationId y efectividad."
      });
    }

    if (typeof efectividad !== "number" || efectividad < 1 || efectividad > 5) {
      return res.status(400).json({
        success: false,
        message: "La efectividad debe ser un número entre 1 y 5."
      });
    }

    // Datos de evaluación procesados
    const evaluacion = {
      idEvaluacion: `EV-${Date.now()}`,
      recommendationId,
      efectividad,
      comentario: comentario || "sin comentarios",
      usuario: usuario || "desconocido",
      timestamp: new Date()
    };

    // Aquí luego puedes guardar en MongoDB:
    // await EvaluationModel.create(evaluacion);

    return res.status(201).json({
      success: true,
      message: "Evaluación registrada exitosamente.",
      data: evaluacion
    });

  } catch (error) {
    console.error("Error al registrar evaluación:", error);

    res.status(500).json({
      success: false,
      message: "Error interno del servidor."
    });
  }
});


router.get("/",(req, res)=>{
  console.log("Notas");  
  res.send("adi");
})

export default router;
