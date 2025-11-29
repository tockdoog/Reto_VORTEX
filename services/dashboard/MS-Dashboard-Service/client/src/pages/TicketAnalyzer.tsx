import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  LinearProgress,
  Box,
  Chip,
  Alert,
  Stack,
} from "@mui/material";
import { Security, Psychology, TrendingDown, Lightbulb } from "@mui/icons-material";
import { useDashboardStore } from "../store/useDashboardStore";
import { api } from "../services/api";
import { getSocket } from "../services/socket";

export const TicketAnalyzer = () => {
  const [text, setText] = useState("");
  const { isAnalyzing, analysisProgress, analysisMessage, analysisResult, setAnalyzing, setProgress, setResult } =
    useDashboardStore();

  useEffect(() => {
    const socket = getSocket();

    socket.on("analysis:progress", (data: { step: number; message: string }) => {
      // Convertimos pasos (1-4) a porcentaje (25-100)
      const percentage = (data.step / 4) * 100;
      setProgress(percentage, data.message);
    });

    socket.on("analysis:complete", () => {
      setAnalyzing(false);
      setProgress(100, "Análisis Completado");
    });

    socket.on("analysis:error", () => {
      setAnalyzing(false);
      setProgress(0, "Error en el análisis");
    });

    return () => {
      socket.off("analysis:progress");
      socket.off("analysis:complete");
      socket.off("analysis:error");
    };
  }, [setAnalyzing, setProgress]);

  const handleAnalyze = async () => {
    if (!text) return;

    setAnalyzing(true);
    setProgress(0, "Iniciando...");
    setResult(null);

    try {
      const response = await api.post("/analyze", { text });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      setAnalyzing(false);
    }
  };

  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: "1400px",
        mx: "auto",
        px: { xs: 2, sm: 3, md: 4 },
      }}
    >
      <Stack spacing={3}>
        {/* Input Area */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Ingresar Ticket
            </Typography>
            <TextField
              fullWidth
              multiline
              rows={4}
              variant="outlined"
              placeholder="Pegue el contenido del correo o ticket aquí..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={isAnalyzing}
            />
            <Box sx={{ mt: 2, display: "flex", alignItems: "center", gap: 2 }}>
              <Button variant="contained" onClick={handleAnalyze} disabled={!text || isAnalyzing}>
                {isAnalyzing ? "Analizando..." : "Analizar Ticket"}
              </Button>
              {isAnalyzing && (
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="body2" color="textSecondary">
                    {analysisMessage}
                  </Typography>
                  <LinearProgress variant="determinate" value={analysisProgress} />
                </Box>
              )}
            </Box>
          </CardContent>
        </Card>

        {/* Results Area */}
        {analysisResult && (
          <Stack spacing={3}>
            <Stack direction={{ xs: "column", md: "row" }} spacing={3}>
              {/* Security */}
              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <Security color="primary" />
                    <Typography variant="h6">Seguridad</Typography>
                  </Box>
                  <Alert severity={analysisResult.security.isSafe ? "success" : "error"}>
                    {analysisResult.security.isSafe ? "Ticket Seguro" : "Amenazas Detectadas"}
                  </Alert>
                  <Typography variant="body2" sx={{ mt: 2, fontStyle: "italic" }}>
                    Texto Anonimizado: "{analysisResult.security.anonymizedText}"
                  </Typography>
                </CardContent>
              </Card>

              {/* Sentiment & Classification */}
              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <Psychology color="secondary" />
                    <Typography variant="h6">Análisis de Texto</Typography>
                  </Box>
                  <Box display="flex" gap={1} mb={2}>
                    <Chip label={`Sentimiento: ${analysisResult.sentiment.label}`} color="primary" variant="outlined" />
                    <Chip label={`Tipo: ${analysisResult.classification.type}`} color="secondary" variant="outlined" />
                  </Box>
                  <Typography>Confianza: {(analysisResult.classification.confidence * 100).toFixed(0)}%</Typography>
                </CardContent>
              </Card>
            </Stack>

            <Stack direction={{ xs: "column", md: "row" }} spacing={3}>
              {/* Churn Risk */}
              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <TrendingDown color="error" />
                    <Typography variant="h6">Riesgo de Fuga (Churn)</Typography>
                  </Box>
                  <Typography variant="h3" color={analysisResult.churnRisk.level === "ALTO" ? "error" : "success.main"}>
                    {analysisResult.churnRisk.score}%
                  </Typography>
                  <Typography variant="subtitle1">Nivel: {analysisResult.churnRisk.level}</Typography>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card sx={{ bgcolor: "#fff3e0", flex: 1 }}>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <Lightbulb color="warning" />
                    <Typography variant="h6">Recomendaciones</Typography>
                  </Box>
                  <ul>
                    {analysisResult.recommendations.map((rec: string, index: number) => (
                      <li key={index}>
                        <Typography variant="body1">{rec}</Typography>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </Stack>
          </Stack>
        )}
      </Stack>
    </Box>
  );
};
