from database import get_db
from models.book import Book, BookUpdate
from bson import ObjectId
from fastapi import HTTPException

def str_to_objectid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

async def get_all_books():
  db = get_db()
  books_collection = db["books"]
  books = await books_collection.find().to_list(length=None)
 # Convertir ObjectId a string para cada libro
  for book in books:
        book["_id"] = str(book["_id"])
        
  return books
 
async def create_new_book(book: Book):
  db = get_db()
  result = await db.books.insert_one(book.dict(exclude_unset=True))  # Aquí usamos .dict() para convertir el modelo en un diccionario
  return {"id": str(result.inserted_id)}

async def get_book_by_id(book_id:str):
    db = get_db()
    book = await db.books.find_one({"_id": str_to_objectid(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    book["_id"] = str(book["_id"])  # Convertir ObjectId a string
    return book

async def update_book_by_id(book_id: str, book: BookUpdate):
    db = get_db()
    result = await db.books.update_one(
        {"_id": str_to_objectid(book_id)}, 
        {"$set": book.dict(exclude_unset=True)}
     )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "success"}

async def delete_book_by_id(book_id:str):
    db = get_db()
    result = await db.books.delete_one({"_id": str_to_objectid(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book does not exist")
    return {"status": "success"}