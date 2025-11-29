import { parseTicket } from "../utils/parseticket.js";

export const recibirTicket = (req, res) => {
  try {
    const { rawTicket } = req.body;

    if (!rawTicket) {
      return res.status(400).json({ error: "Debe enviar rawTicket en el body" });
    }

    // Convertir texto en JSON estructurado
    const parsedTicket = parseTicket(rawTicket);

    return res.json({
      message: "Ticket recibido correctamente",
      ticketEstructurado: parsedTicket
    });

  } catch (error) {
    res.status(500).json({
      error: "Error procesando ticket",
      details: error.message
    });
  }
};
