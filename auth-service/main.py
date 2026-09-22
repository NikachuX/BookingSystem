from fastapi import FastAPI, Depends

from schemas import User
from auth import create_jwt_token
from db.database import get_session
from db.crud import create_user, get_user_by_email


app = FastAPI()

@app.post("/register")
async def register(user: User, session = Depends(get_session)):
    res = await create_user(session,
                            email=user.email,
                            password_hash=user.password_hash,
                            full_name=user.full_name)
    return res

@app.get("/user")
async def get_user(email: str, session = Depends(get_session)):
    res = await get_user_by_email(session, email)
    return res


@app.post("/login")
async def login(user: User):
    pass