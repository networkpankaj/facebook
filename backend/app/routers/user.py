from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import UserCreate
from app.auth import get_password_hash, create_access_token, authenticate_user
from app.database import db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    user_dict = user.dict()
    user_dict['hashed_password'] = get_password_hash(user.password)
    await db["users"].insert_one(user_dict)
    return {"msg": "User created"}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/{user_id}/add_friend")
async def add_friend(user_id: str, friend_id: str):
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$addToSet": {"friends": friend_id}})
    return {"msg": "Friend added"}

@router.delete("/{user_id}/remove_friend")
async def remove_friend(user_id: str, friend_id: str):
    await db["users"].update_one({"_id": ObjectId(user_id)}, {"$pull": {"friends": friend_id}})
    return {"msg": "Friend removed"}
