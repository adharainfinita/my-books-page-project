from pydantic import BaseModel, HttpUrl
from typing import Optional

class BookContent(BaseModel):
    content: HttpUrl # Aquí puedes almacenar una ruta al archivo
    read_by_ai: Optional[bool] = False
    ai_format: Optional[str] = None  # Define el formato en el que la IA leerá el contenido