# main.py
from fastapi import FastAPI
from routes import books_router, comments_router, book_content_router
from database import get_db
import firebase_admin
from firebase_admin import credentials

app = FastAPI()
 # Incluimos las rutas de los libros

app.include_router(books_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(book_content_router, prefix="/api")



cred = credentials.Certificate("./config/my-books-pages-proyect-firebase-admin.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "my-books-pages-proyect.appspot.com"
})


# Ruta raíz (solo para comprobar que el servidor está funcionando)
@app.get("/")
async def root():
    return {"message": "Bienvenida a tu aplicación literaria!"}


# Probar conexión a la base de datos
db = get_db()
print("Conexión a MongoDB exitosa:", db.name)




    