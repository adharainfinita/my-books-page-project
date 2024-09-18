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

# Obtener todos los libros
@router.get("/books")
async def get_books():
    db = get_db()
    books = db.books_collection
    return books

# Crear un nuevo libro
@router.post("/books")
async def create_book(book: Book):
  db = get_db()
  result = db.books.insert_one(book.dict())
  return {"id": str(result.insert_id)}

# Obtener un libro por su ID
@router.get("/books/{book_id}")
async def get_book(book_id: str):
    db = get_db()
    book = db.books.find_one({"_id": str_to_objectid(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

#Cambiar datos de los libros
@router.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
  db = get_db()
  result = db.books.update_one({"_id:": str_to_objectid(book_id)}, {"$Set": book.__dict__})
  if result.matched_count == 0:
    raise HTTPException(status_code=404, detail="Book not found")
  return {"status": "success"}

#Eliminar un libro
@router.delete("app/books/{book_id}")
async def delete_book(book_id: str):
  db = get_db()
  result = db.books.delete_one({"id": str_to_objectid(book_id)})
  if result.matched_count == 0:
    raise HTTPException(status_code=404, detail="Book dont exist")
  return {"status": "success"}
