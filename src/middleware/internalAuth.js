import jwt from "jsonwebtoken";

export const verifyInternalToken = (req, res, next) => {
  const header = req.headers["authorization"];

  if (!header) {
    return res.status(401).json({ error: "Token interno faltante" });
  }

  const token = header.split(" ")[1]; // Formato: Bearer TOKEN

  if (!token) {
    return res.status(401).json({ error: "Formato de token interno inválido" });
  }

  try {
    const decoded = jwt.verify(token, process.env.INTERNAL_SECRET);

    // El gateway agrega "from: 'gateway'" en su JWT interno
    if (decoded.from !== "gateway") {
      return res.status(403).json({ error: "Acceso denegado: origen inválido" });
    }

    // Continúa al endpoint del microservicio
    req.internal = decoded;
    next();

  } catch (error) {
    return res.status(403).json({ error: "Token interno inválido o expirado" });
  }
};