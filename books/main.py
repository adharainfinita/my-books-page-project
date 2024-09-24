# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from routes.books import router as books_router
from routes.comments import router as comments_router
from database import get_db
import firebase_admin
from firebase_admin import credentials, storage

app = FastAPI()
 # Incluimos las rutas de los libros

app.include_router(books_router, prefix="/api")
app.include_router(comments_router, prefix="/api")



cred = credentials.Certificate("./config/my-books-pages-proyect-firebase-adminsdk-7mv1a-10132a0524.json")
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


@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        # Nombre del bucket de Firebase
        bucket = storage.bucket()

        # Crear un blob con el nombre del archivo
        blob = bucket.blob(file.filename)

        # Subir el archivo al bucket de Firebase
        blob.upload_from_file(file.file)

        # Hacer que el archivo sea accesible públicamente
        blob.make_public()

        # Devolver la URL pública del archivo
        return {"url": blob.public_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")