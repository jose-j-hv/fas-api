from fastapi import Request, APIRouter
from starlette.templating import Jinja2Templates
import aiohttp

router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")

url = "http://127.0.0.1:8000"

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