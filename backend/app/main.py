from fastapi import FastAPI
from app.database import db
from app.routers import user, post, message

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(message.router, prefix="/messages", tags=["messages"])

@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()
