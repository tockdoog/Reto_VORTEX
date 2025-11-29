export const anonymizePII = (text) => {
  return text
    // Emails
    .replace(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/g, "[EMAIL]")
    // Teléfonos
    .replace(/(\+?\d{1,2}\s?\d{3}\s?\d{3}\s?\d{4})/g, "[PHONE]")
    // Claves
    .replace(/(password|clave|key)(:?\s*)(\S+)/gi, "$1: [HIDDEN]")
    // Usuarios
    .replace(/usuario:\s*\w+/gi, "usuario: [USER]");
};
