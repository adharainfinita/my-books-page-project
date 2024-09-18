# routes/comments.py

from fastapi import APIRouter, HTTPException
from database import get_db
from models.comment import Comment
from datetime import datetime
from bson import ObjectId

router = APIRouter()


@router.post("/comments/")
async def create_comment(comment: Comment):
    db = get_db()
    result = db.comments.insert_one(comment.dict())
    return {"id": str(result.inserted_id)}

@router.get("/comments/{book_id}")
async def get_comments(book_id: str):
    db = get_db()
    comments = list(db.comments.find({"book_id": book_id}))
    return comments
