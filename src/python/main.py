import os
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel,Field
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bd.base import Base,session
import string
import json
import re
from bd.models.models import AsientosContables,Auditoria,CuentasContables,Empresas,Entidad,PlanCuentas,RegistrosMovimientos,RegistroReportes,Reportes,Roles,Token,Usuarios,UsuarioRegistroMovimiento
from email.message import EmailMessage
import ssl
import smtplib
import pyautogui


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las solicitudes de origen. Para mayor seguridad, especifica los dominios permitidos.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    correo: str
    password: str

class registro(BaseModel):
    nombre: str
    correo: str
    clave: str
    telefono: str
    roles_idroles: int
    token_idtoken: int
    recuperacion: str

class recuperar(BaseModel):
    correo: str

class BuscarEmpresaRequest(BaseModel):
    query: str

class EmpresaSchema(BaseModel):
    id_empresas: int
    nombre: str

    class Config:
        orm_mode = True

class PlanCuentasSchema(BaseModel):
    id_plan_cuentas: int
    codigo: int
    descripcion_cuenta: str

    class Config:
        orm_mode = True

class ErrorMessage(BaseModel):
    message: str

class PlanCuentaCreate(BaseModel):
    codigo_cuenta: str
    descripcion_cuenta: str
    nombre_cuenta: str
    nivel_cuenta: int
    tipo_cuenta: str
    saldo_normal: str
    estado: str

@app.get("/")
async def index():
    
    return "hola mundo!"

@app.post("/buscar-empresas", response_model=list[EmpresaSchema])
def buscar_empresas(request: BuscarEmpresaRequest):
    empresas = session.query(Empresas).filter(Empresas.nombre.ilike(f"%{request.query}%")).all()
    if not empresas:
        raise HTTPException(status_code=404, detail="No companies found")
    return empresas


@app.post("/empresas/{empresa_id}/planes", response_model=Union[list[PlanCuentasSchema], ErrorMessage])
def get_planes_de_cuentas(empresa_id: int):
    planes = session.query(PlanCuentas).filter(PlanCuentas.registro_empresas == empresa_id).all()
    if not planes:
        return {"message": "No se encontró plan"}
    return planes

@app.post("/crear-plan-cuenta")
def crear_plan_cuenta(plan_cuenta: PlanCuentaCreate):
    # Aquí se puede agregar la lógica para validar y guardar la nueva cuenta en la base de datos
    # Ejemplo básico:
    nueva_cuenta = PlanCuentas(
        codigo_cuenta=plan_cuenta.codigo_cuenta,
        descripcion_cuenta=plan_cuenta.descripcion_cuenta,
        nombre_cuenta=plan_cuenta.nombre_cuenta,
        nivel_cuenta=plan_cuenta.nivel_cuenta,
        tipo_cuenta=plan_cuenta.tipo_cuenta,
        saldo_normal=plan_cuenta.saldo_normal,
        estado=plan_cuenta.estado
    )
    session.add(nueva_cuenta)
    session.commit()
    return {"message": "Cuenta creada con éxito"}

"""@app.post("/login/")
async def otro(objeto: Item):

    correo = objeto.correo
    password = objeto.password


    correox = session.query(usuarios).where(usuarios.correo == correo).first()


    if(correox == None or password != correox.clave):

        return {"Falso":False}

    else:

        return {"correo":correox}
"""




"""@app.post("/registro")
async def registro(archivo : registro):


    # Aca ira toda la parte donde recopila la informacion
    correox = archivo.correo
    tokenx = archivo.recuperacion
    tokens = archivo.dict()
    del tokens['nombre']
    del tokens['correo']
    del tokens['clave']
    del tokens['roles_idroles']
    del tokens['token_idtoken']


    correo_reg = session.query(usuarios).where(usuarios.correo == correox).first()
    if(correo_reg == None):
        # Generar un correo cada vez que haga un registro
        token_instance = token(**tokens)

        # Add the token instance to the session
        session.add(token_instance)
        session.commit()

        token_bus = session.query(token).where(token.recuperacion == tokenx).first()

        nuevo_usuario = archivo.dict()
        del nuevo_usuario['recuperacion']


        nuevo_usuario['token_idtoken'] = token_bus.id_token

        usuario_instancia = usuarios(**nuevo_usuario)
        session.add(usuario_instancia)
        session.commit()



        load_dotenv()
        password = os.getenv("PASSWORD")
        email_sender = "juanmalave.itjo@gmail.com"  # el que envia el correo

        email_reciver = correox #el que recibe el correo

        subject = "Registro de su cuenta"
        screenshot = pyautogui.screenshot()
        screenshot.save("../src/imagenes/captura_de_pantalla.png")
        screenshot.show()
        body = f"We received a request to recover your account. \n"
        body += f"Toma tu token de recuperacion:"
        body += f"{token_bus.recuperacion} \n"  # Replace with actual password reset link generation
        body += f"\nIf you didn't request a password reset, you can safely ignore this email."

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_reciver
        em["Subject"] = subject
        em.set_content(body)

        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=contexto) as smtp:
              smtp.login(email_sender,password)
              smtp.sendmail(email_sender,email_reciver,em.as_string())

        return {"Registro Completo"}

    else:
        return {"falso": False}
"""
"""@app.post("/recuperacion")
async def recuperacion(archivo:recuperar):


    correo_ver = archivo.correo
    correo_final = session.query(usuarios).where(usuarios.correo == correo_ver).first()

    if(correo_final == None):

        return {"False": False}
    else:
        load_dotenv()
        password = os.getenv("PASSWORD")
        email_sender = "juanmalave.itjo@gmail.com"  # el que envia el correo

        email_reciver = correo_ver  # el que recibe el correo

        subject = "Registro de su cuenta"

        body = f"We received a request to recover your account. \n"
        body += f"Esta es tu clave:"
        body += f"{correo_final.clave} \n"  # Replace with actual password reset link generation
        body += f"\nIf you didn't request a password reset, you can safely ignore this email."

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_reciver
        em["Subject"] = subject
        em.set_content(body)

        contexto = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_reciver, em.as_string())
        return {"data": correo_final}"""