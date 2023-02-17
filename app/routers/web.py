from fastapi import Request, APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
import aiohttp
from starlette.responses import RedirectResponse, Response
from app.token import verify_token
from app.schemas import TokenData



router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")

url = "http://127.0.0.1:8000"

def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    else:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        return verify_token(token, credentials_exception,TokenData)

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html",{"request":request})

@router.get("/registrer")
def registration(request: Request):
    msj = ""
    return templates.TemplateResponse("create_user.html",{"request":request, "msj":msj })

@router.post("/registrer")
async def registration(request: Request):
    form = await request.form()
    usuario = {
        "username":form.get('username'),
        "password":form.get('password'),
        "nombre":form.get('nombre'),
        "apellido":form.get('apellido'),
        "direccion":form.get('direccion'),
        "correo":form.get('correo'),
        "telefono":form.get('telefono')
    }
    url_post= f"{url}/user/"
    async with aiohttp.ClientSession() as session:
        response = await session.request(method="POST",url=url_post, json=usuario)
        response_json = await response.json()
        print("final-->",response_json)
        if "Respuesta" in response_json:
            msj = "Usuario creado correctamente."
            type_alert ="primary"
        else: 
            msj = "Usuario no creado."
            type_alert ="danger"
        return templates.TemplateResponse("create_user.html",{"request":request, "msj":msj, "type_alert":type_alert })

@router.get("/logout")
def logout(response: Response ,request: Request):
    msj = ""
    response = RedirectResponse("/",status_code=302)
    response.delete_cookie("access_token")
    return response

@router.get("/login_web")
def login_web(request: Request):
    msj = ""
    return templates.TemplateResponse("login.html",{"request":request, "msj":msj })

@router.post("/login_web")
async def login_web(response: Response , request: Request):
    form = await request.form()
    usuario = {
        "username":form.get('username'),
        "password":form.get('password'),
    }
    url_post= f"{url}/login/"
    async with aiohttp.ClientSession() as session:
        response = await session.request(method="POST",url=url_post, data=usuario)
        response_json = await response.json()
        print("final-->",response_json)
        if "access_token" in response_json:
            msj = "Acceso correcto."
            type_alert ="primary"
            response = RedirectResponse("/",status_code=302)
            response.set_cookie(key="access_token",value=response_json["access_token"])
            return response
        else: 
            msj = "Datos incorrctos."
            type_alert ="danger"
        return templates.TemplateResponse("login.html",{"request":request, "msj":msj, "type_alert":type_alert })

@router.get("/mostrar_usuarios")
def mostrar_usuarios(request: Request, current_user= Depends(get_current_user)):
    msj = ""
    if current_user:
        return templates.TemplateResponse("mostrar_usuarios.html",{"request":request, "msj":msj })
    ###return templates.TemplateResponse("login.html",{"request":request, "msj":"Usuario no autenticado, favor de iniciar sesión" })
    response = RedirectResponse("/",status_code=302)
    return response 

