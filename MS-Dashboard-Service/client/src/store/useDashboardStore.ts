import { create } from "zustand";

interface DashboardState {
  // Estado de Análisis
  isAnalyzing: boolean;
  analysisProgress: number;
  analysisMessage: string;
  analysisResult: any | null;

  // Acciones
  setAnalyzing: (isAnalyzing: boolean) => void;
  setProgress: (progress: number, message: string) => void;
  setResult: (result: any) => void;
  resetAnalysis: () => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  isAnalyzing: false,
  analysisProgress: 0,
  analysisMessage: "",
  analysisResult: null,

  setAnalyzing: (isAnalyzing) => set({ isAnalyzing }),
  setProgress: (progress, message) => set({ analysisProgress: progress, analysisMessage: message }),
  setResult: (result) => set({ analysisResult: result }),
  resetAnalysis: () => set({ isAnalyzing: false, analysisProgress: 0, analysisMessage: "", analysisResult: null }),
}));
