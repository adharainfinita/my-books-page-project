# routes/books.py
from fastapi import APIRouter, HTTPException
from models.book import Book, BookUpdate
from services.books_services import get_all_books, create_new_book, update_book_by_id, delete_book_by_id, get_book_by_id


router = APIRouter()

# Obtener todos los libros
@router.get("/books")
async def get_books():
    return await get_all_books()


# Crear un nuevo libro
@router.post("/books")
async def create_book(book: Book):
    return await create_new_book(book)

# Obtener un libro por su ID
@router.get("/books/{book_id}")
async def get_book(book_id: str):
  return await get_book_by_id(book_id)

# Cambiar datos de los libros
@router.put("/books/{book_id}")
async def update_book(book_id: str, book: BookUpdate):
   return await update_book_by_id(book_id, book)

# Eliminar un libro
@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    return await delete_book_by_id(book_id)