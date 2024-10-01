from fastapi import UploadFile, File, HTTPException
from firebase_admin import storage
from models import BookContent, BookUpdate
from services import update_book_by_id

async def upload_file_and_update_book(content: BookContent, book_id: str, file: UploadFile = File(...)): 
    try:
        # Nombre del bucket de Firebase
        bucket = storage.bucket()

        # Crear un blob con el nombre del archivo
        blob = bucket.blob(file.filename)

        # Subir el archivo al bucket de Firebase
        blob.upload_from_file(file.file)

        # Hacer que el archivo sea accesible públicamente
        blob.make_public()

        # Obtener la URL pública del archivo
        url = blob.public_url

        # Crear un nuevo objeto BookContent con la URL del archivo
        book_content = BookContent(content=url, read_by_ai=False, ai_format="text")  # Puedes ajustar ai_format según sea necesario

        # Insertar el contenido en la colección `contents`
        db = get_db()
        content_result = await db.contents.insert_one(book_content.model_dump(exclude_unset=True))

        # Actualizar el libro con el nuevo `content_id`
        update_data = BookUpdate(content_id=str(content_result.inserted_id))  # Crear un objeto BookUpdate con el nuevo content_id

        # Actualizar el libro por su ID
        book_result = await update_book_by_id(book_id, update_data)

        return {
            "book_id": book_id,
            "content_id": str(content_result.inserted_id),
            "file_url": url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")      
