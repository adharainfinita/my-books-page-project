# routes/comments.py

from fastapi import APIRouter
from models import Comment, CommentUpdate
from services import create_a_new_comment, find_comments_for_book, update_comment_by_id, delete_comment_by_id, find_all_comments

comments_router = APIRouter()

@comments_router.get('/all-comments/')
async def get_all_comments():
  return await find_all_comments()

@comments_router.post("/comments/")
async def create_comment(comment: Comment):
 return await create_a_new_comment(comment)

@comments_router.get("/comments/{book_id}")
async def get_comments(book_id: str):
   return await find_comments_for_book(book_id)

@comments_router.put("/comments/{comment_id}")
async def put_comment(comment_id: str, comment: CommentUpdate):
  return await  update_comment_by_id(comment_id, comment)

@comments_router.delete('/comments/{comment_id}')
async def delete_comment(comment_id):
  return await delete_comment_by_id(comment_id)