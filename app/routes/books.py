# routes/books.py
from fastapi import APIRouter, HTTPException
from models.book import Book
from database import get_db
from datetime import datetime
from bson import ObjectId

router = APIRouter()

def str_to_objectid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")


# Función para convertir ObjectId a string
""" def book_serializer(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "summary": book["summary"],
        "published_date": book["published_date"],
        "isbn": book["isbn"]
    }
 """
# Obtener todos los libros
@router.get("/books")
async def get_books():
    db = get_db()
    books_collection = db["books"]
    books = await books_collection.find().to_list(length=None)

    # Convertir ObjectId a string para cada libro
    for book in books:
        book["_id"] = str(book["_id"])
        
    return books


# Crear un nuevo libro
@router.post("/books")
async def create_book(book: Book):
    db = get_db()
    result = db.books.insert_one(book.dict())  # Aquí usamos .dict() para convertir el modelo en un diccionario
    return {"id": str(result.inserted_id)}

# Obtener un libro por su ID
@router.get("/books/{book_id}")
async def get_book(book_id: str):
    db = get_db()
    book = db.books.find_one({"_id": str_to_objectid(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

# Cambiar datos de los libros
@router.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
    db = get_db()
    result = db.books.update_one({"_id": str_to_objectid(book_id)}, {"$set": book.dict(exclude_unset=True)})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "success"}

# Eliminar un libro
@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    db = get_db()
    result = db.books.delete_one({"_id": str_to_objectid(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return {"status": "success"}
