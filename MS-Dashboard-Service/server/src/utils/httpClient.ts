import axios from "axios";

// Creamos una instancia base de Axios
// ¿Por qué? Para no repetir configuración en cada llamada
export const httpClient = axios.create({
  timeout: 10000, // Si un microservicio tarda más de 10s, cancelamos (evita que el dashboard se congele)
  headers: {
    "Content-Type": "application/json",
    "X-Source": "MS-Dashboard-Service", // Buena práctica: decir quién llama
  },
});

// Interceptor para manejar errores globalmente (Opcional pero recomendado)
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(`Error en llamada HTTP: ${error.config?.url}`, error.message);
    return Promise.reject(error);
  }
);
