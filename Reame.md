MS-Security-Service
Responsabilidad: Detección de phishing, anonimización de datos, historial de amenazas.

Endpoints:
POST /api/security/detect-phishing
POST /api/security/anonymize-data
GET  /api/security/threats

Seguridad:
– SOLO accesible desde API Gateway con INTERNAL TOKEN

Tecnologías:
Node.js, Express, Regex, Rules Engine, Redis (opcional)