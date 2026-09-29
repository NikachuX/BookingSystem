import jwt
import os

from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
ph = PasswordHasher()

def create_jwt_token(data: Dict) -> str:
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        return email
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный токен")


def create_password_hash(password: str) -> str:
    return ph.hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False