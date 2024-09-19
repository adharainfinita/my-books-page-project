# main.py
from fastapi import FastAPI
from routes.books import router as books_router
from routes.comments import router as comments_router
from database import get_db

app = FastAPI()
 # Incluimos las rutas de los libros

app.include_router(books_router, prefix="/api")
app.include_router(comments_router, prefix="/api")

# Ruta raíz (solo para comprobar que el servidor está funcionando)
@app.get("/")
async def root():
    return {"message": "Bienvenida a tu aplicación literaria!"}


# Probar conexión a la base de datos
db = get_db()
print("Conexión a MongoDB exitosa:", db.name)
