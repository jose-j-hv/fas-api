from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from main import app
from app.db.models import Base
from app.hashing import Hash
from app.db.database import get_db

db_path = os.path.join(os.path.dirname(__file__),'test.db')
db_uri = "sqlite:///{}".format(db_path)
SQLALCHEMY_DATABASE_URL = db_uri
engine_test = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
TestingSessionLocal = sessionmaker(bind=engine_test,autocommit=False,autoflush=False)
Base.metadata.create_all(bind=engine_test)

cliente = TestClient(app)

def test_insertar_usuario():
    password_hash = Hash.hash_password('pruebax1')
    engine_test.execute(
        f"""
        INSERT INTO usuario(username,password,nombre,apellido,direccion,telefono,correo)
        values
        ('pruebax1','{password_hash}','pru54eba','pru54eba','pru54eba',12235543,'8@gmail')
        """
    )
###test_insertar_usuario()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db 

def test_crear_usuario():
    usuario = {
        "username" : "username201",
        "password" : "password_hash20",
        "nombre" : "nombre20",
        "apellido" : "apellido20",
        "direccion" : "direccioddn201",
        "telefono" : 20,
        "correo" : "co222222222rr@seo20",
        "creacion_user" : "2023-09-10T00:07:49.895643"
    }
    response = cliente.post('/user/',json = usuario)
    assert response.status_code == 401

    usuario_token = {
        "username" : "pruebax1",
        "password" : "pruebax1"
    }

    response_token = cliente.post('/login/',data = usuario_token)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"

    headers = {
        "Authorization" : f"Bearer {response_token.json()['access_token']}"
    }

    response = cliente.post('/user/', json = usuario, headers = headers)
    assert response.status_code == 201
    assert response.json()["Respuesta"] == "Usuario creado correctamente"

def test_obtener_usuario():
    usuario_token = {
        "username" : "pruebax1",
        "password" : "pruebax1"
    }
    response_token = cliente.post('/login/',data = usuario_token)
    assert response_token.status_code == 200
    assert response_token.json()["token_type"] == "bearer"
    headers = {
        "Authorization" : f"Bearer {response_token.json()['access_token']}"
    }
    response = cliente.get('/user/', headers = headers)
    ###print(response.json())
    assert len(response.json()) == 2  ####Solo crea dos usuarios

def test_obtener_usuario():
    response_obtener = cliente.get('/user/1')
    ###print(response_obtener.json())

def test_eliminar_usuario():
    response = cliente.delete('/user/1')
    ##print(response.json())
    response_user = cliente.get('/user/1')
    ##assert response_user.json()["detail"] == "No exsiste el usuario con el id: 1"
    ###print(response_user.json())

########
##def test_actualizar_usuario():
##    usuario = {
##        "username" : "Jose-actualizado",
##    }
##    response = cliente.patch('/user/2',json = usuario)
##    print(response.json())

def test_delete_database():
    db_path = os.path.join(os.path.dirname(__file__),'test.db')
    os.remove(db_path)

