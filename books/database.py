from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de conexión desde las variables de entorno
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

# Crear una instancia del cliente de MongoDB
client = AsyncIOMotorClient(MONGODB_URI)

# Seleccionar la base de datos
db = client[DB_NAME]

# Ejemplo de acceso a una colección llamada 'books'
books_collection = db["books"]
comments_collection = db["comments"]
content_collection = db["contents"]

def get_db():
    """Función para obtener la conexión a la base de datos."""
    return db
