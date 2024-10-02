from fastapi import APIRouter, Depends
from app.models import Post, Comment
from app.database import db

router = APIRouter()

@router.post("/posts/")
async def create_post(post: Post):
    post_dict = post.dict()
    result = await db["posts"].insert_one(post_dict)
    return {"id": str(result.inserted_id)}

@router.post("/posts/{post_id}/like")
async def like_post(post_id: str, user_id: str):
    post = await db["posts"].find_one({"_id": ObjectId(post_id)})
    if post:
        await db["posts"].update_one({"_id": ObjectId(post_id)}, {"$addToSet": {"likes": user_id}})
        return {"msg": "Post liked"}
    return {"msg": "Post not found"}, 404

@router.post("/posts/{post_id}/comment")
async def comment_on_post(post_id: str, comment: Comment):
    comment_dict = comment.dict()
    comment_dict['post_id'] = post_id
    result = await db["comments"].insert_one(comment_dict)
    return {"id": str(result.inserted_id)}
