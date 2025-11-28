import axios from "axios";

// Instancia de Axios pre-configurada
export const api = axios.create({
  baseURL: "http://localhost:3001/api/dashboard", // URL de backend
  headers: {
    "Content-Type": "application/json",
  },
});
