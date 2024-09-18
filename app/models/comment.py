# models/comment.py

from pydantic import BaseModel
from datetime import datetime

class Comment(BaseModel):
    book_id: str
    text: str
    created_at: datetime
