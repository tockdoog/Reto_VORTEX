import { Card, CardContent, Typography, Box, Stack } from "@mui/material";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const data = [
  { name: "Lun", tickets: 40, churn: 24 },
  { name: "Mar", tickets: 30, churn: 13 },
  { name: "Mie", tickets: 20, churn: 58 },
  { name: "Jue", tickets: 27, churn: 39 },
  { name: "Vie", tickets: 18, churn: 48 },
];

export const Overview = () => {
  return (
    <Box
      sx={{
        width: "100%",
        maxWidth: "1400px", // Ancho máximo para pantallas grandes
        mx: "auto", // Centra horizontalmente (margin-left + margin-right: auto)
        px: { xs: 2, sm: 3, md: 4 }, // Padding horizontal adaptativo
      }}
    >
      <Stack spacing={3}>
        {/* Tarjetas de Métricas */}
        <Stack direction={{ xs: "column", sm: "column", md: "row" }} spacing={2} sx={{ width: "100%" }}>
          <Card sx={{ bgcolor: "#e3f2fd", flex: 1, minWidth: { xs: "100%", md: 0 } }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Typography color="textSecondary" gutterBottom sx={{ fontSize: "0.875rem" }}>
                Total Tickets Hoy
              </Typography>
              <Typography
                variant="h3"
                sx={{
                  fontSize: { xs: "1.75rem", md: "2.5rem" },
                  wordBreak: "break-word",
                }}
              >
                150
              </Typography>
            </CardContent>
          </Card>
          <Card sx={{ bgcolor: "#ffebee", flex: 1, minWidth: { xs: "100%", md: 0 } }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Typography color="textSecondary" gutterBottom sx={{ fontSize: "0.875rem" }}>
                Riesgo Promedio Churn
              </Typography>
              <Typography
                variant="h3"
                color="error"
                sx={{
                  fontSize: { xs: "1.75rem", md: "2.5rem" },
                  wordBreak: "break-word",
                }}
              >
                35%
              </Typography>
            </CardContent>
          </Card>
          <Card sx={{ bgcolor: "#e8f5e9", flex: 1, minWidth: { xs: "100%", md: 0 } }}>
            <CardContent sx={{ textAlign: "center", py: 2 }}>
              <Typography color="textSecondary" gutterBottom sx={{ fontSize: "0.875rem" }}>
                Sentimiento Promedio
              </Typography>
              <Typography
                variant="h3"
                color="success.main"
                sx={{
                  fontSize: { xs: "1.75rem", md: "2.2rem" },
                  wordBreak: "break-word",
                  overflow: "visible",
                }}
              >
                Positivo
              </Typography>
            </CardContent>
          </Card>
        </Stack>

        {/* Gráfico */}
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Tendencia Semanal
            </Typography>
            <Box sx={{ height: { xs: 250, sm: 300, md: 350 }, width: "100%" }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" style={{ fontSize: "0.75rem" }} />
                  <YAxis style={{ fontSize: "0.75rem" }} />
                  <Tooltip />
                  <Legend
                    wrapperStyle={{
                      fontSize: "0.875rem",
                      paddingTop: "10px",
                    }}
                    iconSize={10}
                  />
                  <Bar dataKey="tickets" fill="#1976d2" name="Tickets Recibidos" />
                  <Bar dataKey="churn" fill="#d32f2f" name="Riesgo Churn" />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>
      </Stack>
    </Box>
  );
};
