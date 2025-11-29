import { Server as SocketIOServer } from "socket.io";
import { Server as HttpServer } from "http";

let io: SocketIOServer;

export const initSocket = (httpServer: HttpServer) => {
  io = new SocketIOServer(httpServer, {
    cors: {
      origin: "*", // En producción esto debe ser la URL del cliente
      methods: ["GET", "POST"],
    },
  });

  io.on("connection", (socket: any) => {
    console.log("Cliente conectado al WebSocket:", socket.id);

    socket.on("disconnect", () => {
      console.log("Cliente desconectado:", socket.id);
    });
  });

  return io;
};

export const getIO = () => {
  if (!io) {
    throw new Error("Socket.io no ha sido inicializado!");
  }
  return io;
};
