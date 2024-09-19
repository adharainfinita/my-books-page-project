# models/book.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ContactInfo import ContactInfo



class ContactInfo(BaseModel):
    name: str
    email: str
    website: Optional[str] = None
    social_media: Optional[Dict[str, str]] = None  # Ejemplo: {"twitter": "@autor"}

# Esquema para validar los datos de un libro
class Book(BaseModel):
    title: str
    author: str
    image: str
    published_date: Optional[datetime] = None
    summary: str
    banners: Union[str, list[str]] = None 
    formats: Optional[dict[str, bool]] = None
    isbn: str
    my_book: bool = False
    contact: ContactInfo
    content: Optional[str] = None  # Aquí puedes almacenar una ruta al archivo o el contenido en sí
    read_by_ai: Optional[bool] = False
    ai_format: Optional[str] = None  # Define el formato en el que la IA leerá el contenido
