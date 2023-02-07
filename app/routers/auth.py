from fastapi import APIRouter,Depends, status 
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas import Loging
from app.repository import auth
from fastapi.security import OAuth2PasswordRequestForm

router =  APIRouter(
    prefix = "/login",
    tags=["Login"]
)

@router.post('/',status_code=200)
def obtener_usuarios(usuario:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    auth_token = auth.auth_user(usuario,db)
    return auth_token 