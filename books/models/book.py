# models/book.py
from pydantic import BaseModel, HttpUrl, EmailStr, field_validator, ConfigDict
from typing import Optional
from datetime import datetime
import re


class ContactInfo(BaseModel):
    name: str
    email: Optional[EmailStr]
    website: Optional[str] = None
    social_media: Optional[dict[str, str]] = None  # Ejemplo: {"twitter": "@autor"}


# Esquema para validar los datos de un libro
class Book(BaseModel):
    title: str
    author: str
    image: HttpUrl
    published_date: Optional[datetime] = None
    summary: str
    banners:Optional[list[str]] = None 
    formats: Optional[list[str]] = None
    isbn: str
    my_book: bool = False
    contact: ContactInfo
    content: Optional[HttpUrl] = None  # Aquí puedes almacenar una ruta al archivo o el contenido en sí
    read_by_ai: Optional[bool] = False
    ai_format: Optional[str] = None  # Define el formato en el que la IA leerá el contenido

    @field_validator('title')
    def title_word_limit(summary_value):
        max_words = 10
        word_count = len(summary_value.split())
        if word_count > max_words:
            raise ValueError(f'The title mus not exceed {max_words}words. Currently has {word_count}words.')
        return summary_value
    
    @field_validator('author')
    def author_word_limit(author_value):
        max_words = 5
        word_count = len(author_value.split())
        if word_count > max_words:
            raise ValueError(f'The title mus not exceed {max_words}words. Currently has {word_count}words.')
        author_value = ' '.join([word.capitalize() for word in author_value.split()])
        return author_value

    @field_validator('image')
    def image_validator(image_value):
        if not re.search(r'\\.(jpg|jpeg|png|webp|tiff|bmp|gif)$', image_value, re.IGNORECASE):
            raise ValueError('Invalid image format. Allowed formats: jpg|jpeg|png|webp|tiff|bmp|gif')
        return image_value


    @field_validator('summary')
    def summary_word_limit(summary_value):
        max_words = 100
        word_count = len(summary_value.split())
        if word_count > max_words:
            raise ValueError(f'summary must not exceed {max_words} words. Currently has {word_count} words.')
        return summary_value

    @field_validator('isbn')
    def isbn_length(isbn_value):
        if len(isbn_value) not in [10, 13]:
            raise ValueError('ISBN must be either 10 or 13 character long.')
        return isbn_value


class BookUpdate(Book):
    title: Optional[str] = None
    author: Optional[str] = None
    image: Optional[HttpUrl] = None
    summary: Optional[str] = None
    published_date: Optional[datetime] = None
    isbn: Optional[str] = None
    my_book: Optional[bool] = None
    banners: Optional[list[str]] = None
    contact: Optional[ContactInfo] = None
    content: Optional[HttpUrl] = None
    read_by_ai: Optional[bool] = None
    ai_format: Optional[str] = None

    class ConfigDict:
        from_attributes = True