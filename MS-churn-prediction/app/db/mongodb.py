# ======================================
# CONEXIÓN A MONGODB ATLAS
# ======================================
# Este archivo maneja la conexión a la base de datos.
#
# Equivalente en Node.js/TypeScript:
# import mongoose from 'mongoose';
# mongoose.connect(MONGO_URL);

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Variable global para guardar la conexión (cuando se conecte)
# Equivalente en TS: let client: MongoClient | null = null;
client: AsyncIOMotorClient = None

async def connect_to_mongo():
    
    global client  # Usamos la variable global definida arriba
    
    print("🔌 Conectando a MongoDB Atlas...")
    
    # Creamos el cliente de MongoDB
    # AsyncIOMotorClient es como el MongoClient de Node.js pero asíncrono
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Probamos la conexión haciendo un ping
    await client.admin.command('ping')
    
    print("✅ Conectado exitosamente a MongoDB Atlas")

async def close_mongo_connection():
    """
    Cierra la conexión a MongoDB.
    
    Esta función se ejecutará cuando el servidor se apague.
    
    Equivalente en Node.js:
    async function closeMongo() {
        await client.close();
    }
    """
    global client
    
    if client:
        print("🔌 Cerrando conexión a MongoDB...")
        client.close()
        print("✅ Conexión cerrada")

def get_database():
    """
    Retorna la base de datos activa.
    
    Esto es como un getter que devuelve la instancia de la BD.
    
    Equivalente en TypeScript:
    function getDatabase(): Db {
        return client.db(DATABASE_NAME);
    }
    
    Returns:
        Database: Instancia de la base de datos
    """
    return client[settings.DATABASE_NAME]
