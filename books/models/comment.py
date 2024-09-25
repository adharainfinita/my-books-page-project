# models/comment.py

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class Comment(BaseModel):
    book_id: str
    text: str
    created_at: Optional[datetime] = None

    @field_validator('text')
    def validator_text_limit(text_value):
        max_words = 1500
        text_length = len(text_value)
        if text_length > max_words:
            raise ValueError(f'The comment has be exceed the max limit of character. {text_length} characters.')
        return text_value

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.now()

class CommentUpdate(Comment):
    book_id: Optional[str] = None
    text: Optional[str] = None
    created_at: Optional[datetime] = None