from fastapi import APIRouter,Depends, status 
from app.schemas import User,UserID,ShowUser,UpdateUser
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import models
from typing import List
from app.repository import user
from app.oauth import get_current_user

router =  APIRouter(
    prefix = "/user",
    tags=["Users"]
)

usuarios =[]

@router.get('/',status_code=200)#,response_model = List[ShowUser] 
def obtener_usuarios(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    data = user.obtener_usuarios(db)
    return data

@router.post('/',status_code = status.HTTP_201_CREATED)
def crear_usuario(usuario:User, db:Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user.crear_usuario(usuario,db)
    return{"Respuesta":"Usuario creado correctamente"}


@router.post('/obtener_usuario',status_code=status.HTTP_200_OK)
def obtener_usuario_2(user_id:UserID, db:Session =  Depends(get_db) ):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario : 
        return{"Respuesta":"Usuario no encontrado"}

@router.get('//{user_id}',status_code=status.HTTP_200_OK)#response_model = ShowUser
def obtener_usuario(user_id:int, db:Session = Depends(get_db)):
    usuario = user.obtener_usuario(user_id,db)
    return usuario
    
@router.delete('/{user_id}',status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id:int,db:Session = Depends(get_db)):
    res = user.eliminar_usuario(user_id,db)
    return res

@router.patch('/{user_id}',status_code=status.HTTP_200_OK)
def actualizar_usuario(user_id:int, updateUser:UpdateUser, db:Session = Depends(get_db)): 
    res = user.actualizar_user(user_id,UpdateUser,db)
    return res