from database import get_db
from fastapi import HTTPException
from models.comment import Comment, CommentUpdate
from utils import str_to_objectid


async def create_a_new_comment(comment: Comment):
    db = get_db()
    id_str = str_to_objectid(comment.book_id)
    book_found = await db.books.find_one({"_id": id_str})

    if not book_found:
      raise HTTPException(status_code=404, detail='Book not found')

    result = await db.comments.insert_one(comment.model_dump())
    return {"id": str(result.inserted_id)}

async def find_all_comments():
  db = get_db()
  comments_collections = db["comments"]
  comments = await comments_collections.find().to_list(length=None)
  for comment in comments:
        comment["_id"] = str(comment["_id"])
        
  return comments


async def find_comments_for_book(book_id: str):
    db = get_db()
    comments = await db.comments.find({"book_id":book_id}).to_list(length=None)
    for comment in comments:
        comment["_id"] = str(comment["_id"])
    return comments

async def update_comment_by_id(comment_id: str, comment: CommentUpdate):
    db = get_db()
    update_data = comment.model_dump(exclude_unset=True)
    result_update = await db.comments.update_one(
      {"_id": str_to_objectid(comment_id)},
      {"$set": update_data}
      )
    if result_update.matched_count == 0:
        raise HTTPException(status_code=404, detail="Comment not found")
    if result_update.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made to the comment")

    return {"status": "success"}

async def delete_comment_by_id(comment_id:str):
    db = get_db()
    result_delete = await db.comments.delete_one({"_id": str_to_objectid(comment_id)})
    if result_delete.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comment does not exist")
    return {"status": "success"}
