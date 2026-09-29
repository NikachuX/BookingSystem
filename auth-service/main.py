from fastapi import FastAPI, Depends, HTTPException

from contextlib import asynccontextmanager
from schemas import UserRegister, UserLogin, UserResponse
from auth import create_jwt_token, get_user_from_token, create_password_hash, verify_password
from db.database import get_session
from db.crud import create_user, get_user_by_email
from db.init_db import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/register")
async def register(user: UserRegister, session = Depends(get_session)):
    usr = await get_user_by_email(session, user.email)
    if usr is not None:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    password_hash = create_password_hash(user.password)
    res = await create_user(session,
                            email=user.email,
                            password_hash=password_hash,
                            full_name=user.full_name)
    return {"Status": "Пользователь зарегистрирован"}

@app.get("/user")
async def get_user(email: str = Depends(get_user_from_token), session = Depends(get_session)):
    res = await get_user_by_email(session, email)

    if res is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user_data = {"id": res.id, "email": res.email, "full_name": res.full_name, "role": res.role.value}
    usr = UserResponse(**user_data)
    return usr

@app.post("/login")
async def login(user: UserLogin, session = Depends(get_session)):
    res = await get_user_by_email(session, user.email)
    if res is None:
        raise HTTPException(status_code=401, detail="Неверный email")
    if not verify_password(res.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")

    token = create_jwt_token({
        "id": res.id,
        "email": res.email
    })

    return {"access_token": token}