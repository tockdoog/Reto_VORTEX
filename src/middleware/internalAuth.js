import jwt from "jsonwebtoken";

export const verifyInternalToken = (req, res, next) => {
  const auth = req.headers["authorization"];

  if (!auth)
    return res.status(401).json({ error: "Token interno faltante" });

  const token = auth.split(" ")[1];

  try {
    const decoded = jwt.verify(token, process.env.INTERNAL_SECRET);

    if (decoded.from !== "gateway")
      return res.status(403).json({ error: "Acceso denegado" });

    next();
  } catch (error) {
    return res.status(403).json({ error: "Token interno inválido" });
  }
};
