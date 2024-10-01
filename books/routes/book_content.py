# routes/book_content.py
from fastapi import APIRouter, File, UploadFile
from models import BookContent
from services import upload_file_and_update_book

book_content_router = APIRouter()

@book_content_router.post('/upload{book_id}')
async def upload_file(content: BookContent, file: UploadFile = File(...)):
   return await upload_file_and_update_book(content, book_id, file)    

# Aquí se definirán las rutas de lectura por IA proximamente