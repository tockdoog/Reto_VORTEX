import { useState } from "react";
import { Layout } from "./components/Layout";
import { Overview } from "./pages/Overview";
import { TicketAnalyzer } from "./pages/TicketAnalyzer";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

// Tema personalizado (Opcional, para que se vea más bonito)
const theme = createTheme({
  palette: {
    primary: {
      main: "#2563eb", // Azul moderno
    },
    secondary: {
      main: "#7c3aed", // Violeta
    },
    background: {
      default: "#f8fafc", // Gris muy claro para el fondo
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12, // Bordes redondeados
          boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)", // Sombra suave
        },
      },
    },
  },
});

function App() {
  const [currentView, setCurrentView] = useState<"overview" | "analyzer">("overview");

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Layout currentView={currentView} onViewChange={setCurrentView}>
        {currentView === "overview" ? <Overview /> : <TicketAnalyzer />}
      </Layout>
    </ThemeProvider>
  );
}

export default App;
