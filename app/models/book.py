# models/book.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema para validar los datos de un libro
class Book(BaseModel):
    title: str
    author: str
    summary: str
    published_date: Optional[datetime] = None
    isbn: str