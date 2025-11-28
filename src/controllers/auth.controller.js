import { generateToken } from "../utils/token.util.js";
import users from "../data/users.json" with  { type: "json" };

export const login = (req, res) => {
  const { username, password } = req.body;

  if (!username || !password)
    return res.status(400).json({ error: "Usuario y contraseña requeridos" });

  const user = users.find(
    (u) => u.username === username && u.password === password
  );

  if (!user)
    return res.status(401).json({ error: "Credenciales incorrectas" });

  // Crear token JWT
  const token = generateToken({
    id: user.id,
    username: user.username,
    role: user.role
  });

  return res.json({
    mensaje: "Inicio de sesión exitoso",
    token,
    user: {
      id: user.id,
      username: user.username,
      role: user.role
    }
  });
};
