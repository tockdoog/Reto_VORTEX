import mongoose from 'mongoose';

const ticketSchema = new mongoose.Schema({
  ticketId: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  cliente: {
    type: String,
    required: true,
    trim: true
  },
  proyecto: {
    type: String,
    required: true,
    trim: true
  },
  fecha: {
    type: String,
    required: true
  },
  contacto: {
    nombre: {
      type: String,
      required: true,
      trim: true
    },
    email: {
      type: String,
      required: true,
      trim: true,
      lowercase: true
    }
  },
  telefono: {
    type: String,
    required: true,
    trim: true
  },
  asunto: {
    type: String,
    required: true,
    trim: true
  },
  descripcion: {
    type: String,
    required: true
  },
  estado: {
    type: String,
    enum: ['abierto', 'en_proceso', 'resuelto', 'cerrado'],
    default: 'abierto'
  },
  prioridad: {
    type: String,
    enum: ['baja', 'media', 'alta', 'critica'],
    default: 'media'
  },
  categoria: {
    type: String,
    enum: ['soporte_tecnico', 'facturacion', 'funcionalidad', 'mejora', 'otro'],
    default: 'soporte_tecnico'
  },
  fechaCreacion: {
    type: Date,
    default: Date.now
  },
  fechaActualizacion: {
    type: Date,
    default: Date.now
  },
  metadata: {
    fuente: {
      type: String,
      enum: ['web', 'api', 'chatbot', 'email'],
      default: 'web'
    },
    usuarioCreacion: {
      type: String,
      default: 'sistema'
    }
  }
});

// Middleware para actualizar fecha de modificación
ticketSchema.pre('save', function() {
  this.fechaActualizacion = Date.now();
});

// Método estático para buscar por ticketId
ticketSchema.statics.findByTicketId = function(ticketId) {
  return this.findOne({ ticketId });
};

// Método estático para obtener analytics
ticketSchema.statics.getAnalytics = function() {
  return this.aggregate([
    {
      $facet: {
        // Conteo por estado
        porEstado: [
          {
            $group: {
              _id: '$estado',
              count: { $sum: 1 }
            }
          }
        ],
        // Conteo por prioridad
        porPrioridad: [
          {
            $group: {
              _id: '$prioridad',
              count: { $sum: 1 }
            }
          }
        ],
        // Conteo por categoría
        porCategoria: [
          {
            $group: {
              _id: '$categoria',
              count: { $sum: 1 }
            }
          }
        ],
        // Tickets por mes
        porMes: [
          {
            $group: {
              _id: {
                year: { $year: '$fechaCreacion' },
                month: { $month: '$fechaCreacion' }
              },
              count: { $sum: 1 }
            }
          },
          {
            $sort: { '_id.year': 1, '_id.month': 1 }
          }
        ],
        // Estadísticas generales
        general: [
          {
            $group: {
              _id: null,
              totalTickets: { $sum: 1 },
              ticketsAbiertos: {
                $sum: { $cond: [{ $eq: ['$estado', 'abierto'] }, 1, 0] }
              },
              ticketsResueltos: {
                $sum: { $cond: [{ $eq: ['$estado', 'resuelto'] }, 1, 0] }
              },
              promedioTiempoResolucion: {
                $avg: {
                  $cond: [
                    { $eq: ['$estado', 'resuelto'] },
                    { $subtract: ['$fechaActualizacion', '$fechaCreacion'] },
                    null
                  ]
                }
              }
            }
          }
        ]
      }
    }
  ]);
};

export default mongoose.model('Ticket', ticketSchema);