import Ticket from '../models/ticket.model.js';

// Utilidad para formatear respuesta
const formatResponse = (success, data, message = '') => {
  return {
    success,
    data,
    message,
    timestamp: new Date().toISOString()
  };
};

// Utilidad para extraer nombre y email del contacto
const parseContacto = (contactoString) => {
  const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+)/gi;
  const email = contactoString.match(emailRegex);
  
  let nombre = contactoString;
  if (email) {
    nombre = contactoString.replace(email[0], '').trim();
  }
  
  return {
    nombre: nombre || 'Nombre no proporcionado',
    email: email ? email[0] : 'email@no-proporcionado.com'
  };
};

// Endpoint para almacenar tickets procesados
export const createTicket = async (req, res) => {
  try {
    const {
      id,
      cliente,
      proyecto,
      fecha,
      contacto,
      telefono,
      asunto,
      descripcion
    } = req.body;

    // Validaciones básicas
    if (!id || !cliente || !proyecto || !fecha || !contacto || !asunto || !descripcion) {
      return res.status(400).json(
        formatResponse(false, null, 'Faltan campos obligatorios '+id)
      );
    }

    // Verificar si el ticket ya existe
    const existingTicket = await Ticket.findOne({ ticketId: id });
    if (existingTicket) {
      return res.status(409).json(
        formatResponse(false, null, `El ticket con ID ${id} ya existe`)
      );
    }

    // Parsear información de contacto
    const contactoParseado = parseContacto(contacto);

    // Crear nuevo ticket
    const nuevoTicket = new Ticket({
      ticketId: id,
      cliente,
      proyecto,
      fecha,
      contacto: contactoParseado,
      telefono,
      asunto,
      descripcion,
      prioridad: determinarPrioridad(asunto, descripcion),
      categoria: determinarCategoria(asunto, descripcion),
      metadata: {
        fuente: req.headers['x-fuente'] || 'api',
        usuarioCreacion: req.headers['x-usuario'] || 'sistema'
      }
    });

    // Guardar en la base de datos
    const ticketGuardado = await nuevoTicket.save();

    res.status(201).json(
      formatResponse(true, ticketGuardado, 'Ticket creado exitosamente')
    );

  } catch (error) {
    console.error('Error al crear ticket:', error);
    
    if (error.name === 'ValidationError') {
      return res.status(400).json(
        formatResponse(false, null, 'Error de validación: ' + error.message)
      );
    }
    
    if (error.code === 11000) {
      return res.status(409).json(
        formatResponse(false, null, 'El ID del ticket ya existe')
      );
    }

    res.status(500).json(
      formatResponse(false, null, 'Error interno del servidor')
    );
  }
};

// Endpoint para recuperar ticket específico
export const getTicketById = async (req, res) => {
  try {
    const { id } = req.params;
    
    if (!id) {
      return res.status(400).json(
        formatResponse(false, null, 'ID del ticket es requerido')
      );
    }

    const ticket = await Ticket.findByTicketId(id);

    if (!ticket) {
      return res.status(404).json(
        formatResponse(false, null, `Ticket con ID ${id} no encontrado`)
      );
    }

    res.status(200).json(
      formatResponse(true, ticket, 'Ticket encontrado exitosamente')
    );

  } catch (error) {
    console.error('Error al buscar ticket:', error);
    
    res.status(500).json(
      formatResponse(false, null, 'Error interno del servidor')
    );
  }
};

// Endpoint para datos de análisis agregado
export const getAnalytics = async (req, res) => {
  try {
    const { fechaInicio, fechaFin, agruparPor } = req.query;

    // Pipeline base para analytics
    let pipeline = [];

    // Filtro por fecha si se proporciona
    if (fechaInicio || fechaFin) {
      const fechaFiltro = {};
      if (fechaInicio) fechaFiltro.$gte = new Date(fechaInicio);
      if (fechaFin) fechaFiltro.$lte = new Date(fechaFin);
      
      pipeline.push({
        $match: {
          fechaCreacion: fechaFiltro
        }
      });
    }

    // Agregación según el parámetro agruparPor
    if (agruparPor) {
      pipeline.push({
        $group: {
          _id: `$${agruparPor}`,
          count: { $sum: 1 },
          tickets: {
            $push: {
              ticketId: '$ticketId',
              cliente: '$cliente',
              asunto: '$asunto',
              estado: '$estado',
              fechaCreacion: '$fechaCreacion'
            }
          }
        }
      });
    } else {
      // Analytics completos si no se especifica agrupación
      const analytics = await Ticket.getAnalytics();
      return res.status(200).json(
        formatResponse(true, analytics[0], 'Analytics generados exitosamente')
      );
    }

    const resultado = await Ticket.aggregate(pipeline);

    res.status(200).json(
      formatResponse(true, resultado, 'Datos de analytics obtenidos exitosamente')
    );

  } catch (error) {
    console.error('Error al obtener analytics:', error);
    
    res.status(500).json(
      formatResponse(false, null, 'Error interno del servidor')
    );
  }
};

// Función auxiliar para determinar prioridad basada en asunto y descripción
const determinarPrioridad = (asunto, descripcion) => {
  const texto = (asunto + ' ' + descripcion).toLowerCase();
  
  if (texto.includes('crítico') || texto.includes('critico') || 
      texto.includes('error 500') || texto.includes('no funciona') ||
      texto.includes('urgen') || texto.includes('emergencia')) {
    return 'alta';
  }
  
  if (texto.includes('lento') || texto.includes('problema') || 
      texto.includes('error') || texto.includes('bug')) {
    return 'media';
  }
  
  return 'baja';
};

// Función auxiliar para determinar categoría
const determinarCategoria = (asunto, descripcion) => {
  const texto = (asunto + ' ' + descripcion).toLowerCase();
  
  if (texto.includes('factura') || texto.includes('pago') || texto.includes('cobro')) {
    return 'facturacion';
  }
  
  if (texto.includes('mejora') || texto.includes('nueva funcionalidad') || 
      texto.includes('sugerencia')) {
    return 'mejora';
  }
  
  if (texto.includes('error') || texto.includes('bug') || texto.includes('no funciona')) {
    return 'soporte_tecnico';
  }
  
  return 'otro';
};