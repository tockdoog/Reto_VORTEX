import { io, Socket } from "socket.io-client";

let socket: Socket;

export const initSocket = () => {
  // Conectamos al servidor (puerto 3001)
  socket = io("http://localhost:3001");

  socket.on("connect", () => {
    console.log("Conectado al servidor de WebSockets");
  });

  socket.on("disconnect", () => {
    console.log("Desconectado del servidor");
  });

  return socket;
};

export const getSocket = () => {
  if (!socket) {
    return initSocket();
  }
  return socket;
};
