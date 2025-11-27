import { generateToken } from "../utils/token.util.js";

// Usuarios de ejemplo (puedes sustituir con DB real)
const mockUsers = [
  { id: 1, username: "admin", password: "123456", role: "admin" },
  { id: 2, username: "luis", password: "abc123", role: "user" }
];

export const login = (req, res) => {
  const { username, password } = req.body;

  if (!username || !password)
    return res.status(400).json({ error: "Usuario y contraseña requeridos" });

  const user = mockUsers.find(
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
