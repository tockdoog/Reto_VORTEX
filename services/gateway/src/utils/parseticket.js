export const parseTicket = (text) => {
  const lines = text.split("\n").map(l => l.trim());

  const getValue = (prefix) => {
    const line = lines.find(l => l.startsWith(prefix));
    return line ? line.replace(prefix, "").trim() : "";
  };

  const id = getValue("ID del Ticket:");
  const cliente = getValue("Cliente:");
  const proyecto = getValue("Proyecto:");
  const fecha = getValue("Fecha:");
  const contacto = getValue("Contacto:");
  const telefono = getValue("Teléfono:");

  // Extraer Asunto (líneas posteriores al label)
  const asuntoIndex = lines.findIndex(l => l.startsWith("Asunto"));
  let asunto = "";
  if (asuntoIndex !== -1) {
    asunto = lines[asuntoIndex + 1]?.trim();
  }

  // Extraer descripción: desde "Descripción del problema" hasta final
  const descIdx = lines.findIndex(l => l.startsWith("Descripción"));
  const descripcion = descIdx !== -1
    ? lines.slice(descIdx + 1).join("\n").trim()
    : "";

  return {
    id,
    cliente,
    proyecto,
    fecha,
    contacto,
    telefono,
    asunto,
    descripcion
  };
};
