import os
from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel,Field
from fastapi import FastAPI,HTTPException,Depends,File,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from bd.base import Base,session
import tempfile
import string
import json
import re
from bd.models.models import TiposCuentas,AsientosContables,Auditoria,CuentasContables,Empresas,Entidad,PlanCuentas,RegistrosMovimientos,RegistroReportes,Reportes,Roles,Token,Usuarios,UsuarioRegistroMovimiento
from email.message import EmailMessage
import ssl
import smtplib
import pyautogui
import openpyxl


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
    contrasena: str

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


class CuentaContableSchema(BaseModel):
    codigo_cuenta: str
    descripcion_cuenta: str
    nombre_cuenta: str
    nivel_cuenta: str
    tipo_cuenta: str
    saldo_normal: float
    estado: str
    fecha: str
    tipo_asiento: str  # Tipo de asiento relacionado con tipo_cuenta
    documento_respaldo: str  # Documento de respaldo relacionado con tipo_cuenta
    

class BuscarEmpresaRequest(BaseModel):
    query: str

class EmpresaSchema(BaseModel):
    id_empresas: int
    nombre: str

    class Config:
        orm_mode = True


    class Config:
        orm_mode = True

class ErrorMessage(BaseModel):
    message: str
    
class ReporteCreate(BaseModel):
    fecha_inicio: str
    fecha_fin: str
    nivel_detalle: str
    formato: str    
    
class CuentaContableSchema(BaseModel):
    codigo_cuenta: str
    descripcion_cuenta: str
    nombre_cuenta: str
    nivel_cuenta: str
    tipo_cuenta: str
    saldo_normal: float
    fecha: str
    estado: str
    documento_respaldo: str
        
@app.get("/")
async def index():
    
    return "hola mundo!"

@app.post("/buscar-empresas", response_model=list[EmpresaSchema])
def buscar_empresas(request: BuscarEmpresaRequest):
    empresas = session.query(Empresas).filter(Empresas.rif.ilike(f"%{request.query}%")).all()
    if not empresas:
        raise HTTPException(status_code=404, detail="No companies found")
    return empresas


@app.post("/empresas/{empresa_id}/crear-cuentas-y-plan")
def crear_cuentas_y_plan(empresa_id: int, cuentas: list[CuentaContableSchema]):
    try:
        empresa = session.query(Empresas).filter(Empresas.id_empresas == empresa_id).first()
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")

        # Crear plan de cuentas
        nuevo_plan = PlanCuentas(
            codigo="PLAN_" + str(empresa_id),  # Usar un código válido
            descripcion_cuenta="Plan de cuentas para la empresa " + str(empresa_id),
            registro_empresas=empresa_id
        )
        session.add(nuevo_plan)
        session.commit()

        for cuenta in cuentas:
            # Validar la jerarquía de código de cuenta
            codigo_partes = cuenta.codigo_cuenta.split('.')
            if len(codigo_partes) > 1:
                codigo_padre = '.'.join(codigo_partes[:-1])
                cuenta_padre = session.query(CuentasContables).filter(
                    CuentasContables.codigo == codigo_padre,
                    CuentasContables.empresas_id == empresa_id
                ).first()
                if not cuenta_padre:
                    raise HTTPException(status_code=400, detail=f"Debe existir una cuenta padre {codigo_padre} para crear la subcuenta {cuenta.codigo_cuenta}")

            # Crear cuenta contable
            nueva_cuenta = CuentasContables(
                codigo=cuenta.codigo_cuenta,
                descripcion_cuenta=cuenta.descripcion_cuenta,
                nombre_cuenta=cuenta.nombre_cuenta,
                nivel_cuenta=cuenta.nivel_cuenta,
                tipo_cuenta=cuenta.tipo_cuenta,
                saldo_normal=cuenta.saldo_normal,
                estado_cuenta="abierto",
                empresas_id=empresa_id
            )
            session.add(nueva_cuenta)
            session.commit()

            # Crear asiento contable
            nuevo_asiento = AsientosContables(
                cuentas_contables_id=nueva_cuenta.id_cuenta_contable,
                cuentas_contables_empresas_id=empresa_id,
                fecha=cuenta.fecha,
                descripcion_asiento=cuenta.descripcion_cuenta,
                tipo_asiento=cuenta.tipo_cuenta,  # tipo_asiento viene de tipo_cuenta
                documento_respaldo=cuenta.documento_respaldo,
                plan_cuentas_id=nuevo_plan.id_plan_cuentas  # Usar el nuevo plan de cuentas
            )
            session.add(nuevo_asiento)
            session.commit()

        return {"message": "Plan de cuentas y asientos contables creados con éxito."}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

@app.get("/empresas/{empresa_id}/planes")
def obtener_planes(empresa_id: int):
    planes = session.query(PlanCuentas).filter(PlanCuentas.registro_empresas == empresa_id).all()
    return planes

@app.post("/empresas/{empresa_id}/crear-reporte")
def crear_reporte(empresa_id: int, reporte_data: ReporteCreate):
    # Verificar que la empresa existe
    empresa = session.query(Empresas).filter(Empresas.id_empresas == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    # Crear el reporte
    nuevo_reporte = Reportes(
        tipo_reporte="Libro Diario",
        fecha_inicio=reporte_data.fecha_inicio,
        fecha_fin=reporte_data.fecha_fin,
        nivel_detalle=reporte_data.nivel_detalle,
        formato=reporte_data.formato,
        archivo=""  # Aquí se generaría y guardaría el archivo del reporte
    )
    session.add(nuevo_reporte)
    session.commit()

    # Obtener los registros de movimientos para el reporte
    movimientos = session.query(RegistrosMovimientos).filter(
        RegistrosMovimientos.Empresas_id == empresa_id,
        RegistrosMovimientos.Fecha_movimiento >= reporte_data.fecha_inicio,
        RegistrosMovimientos.Fecha_movimiento <= reporte_data.fecha_fin
    ).all()

    # Aquí iría la lógica para generar el archivo del reporte basado en los movimientos obtenidos

    return {"message": "Reporte creado con éxito", "reporte_id": nuevo_reporte.id_reporte}

@app.post("/login/")
async def otro(objeto: Item):
    correo = objeto.correo
    password = objeto.contrasena

    correox = session.query(Usuarios).where(Usuarios.correo == correo).first()

    if correox is None or password != correox.clave:
        return {"Falso": False}
    else:
        return {"correo": correox}

@app.post("/empresas/crear-plan/")
async def crear_plan(archivo: UploadFile = File(...)):
    if not archivo.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un archivo Excel con extensión .xlsx")

    try:
        # Crear un archivo temporal para guardar el contenido
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
            temp_file.write(await archivo.read())
            temp_file.flush()

            # Cargar el archivo Excel con openpyxl
            workbook = openpyxl.load_workbook(temp_file.name)
            hoja = workbook.active

            # Leer las celdas (ajusta el rango según tus datos)
            celdas = hoja['A1':'C325']
            resultados = []
            arreglo = []
            contador = 0

            for fila in celdas:
                valor_celda_1 = str(fila[0].value)  # Convertir a cadena
                valor_celda_2 = str(fila[1].value)
                valor_celda_3 = str(fila[2].value)

                if contador == 0:
                    arreglo.append(valor_celda_1)  # Agregar valor al arreglo
                
                elif contador == 1:
                    arreglo.append(valor_celda_1)  # Agregar el segundo valor al arreglo
                    bandera = arreglo[1]
                    ultimo_numero = arreglo[1].split(".")[-1]
                        
                    bandera_puntos = re.sub(r'[^.]', '', arreglo[0])
                    bandera_puntos2 = re.sub(r'[^.]', '', arreglo[1])
                        
                    if bandera_puntos < bandera_puntos2 and (int(ultimo_numero) > 1 or int(ultimo_numero) < 0):
                        return {"error": f"Esta mal colocado la cuenta en {arreglo[1]}"}
                        
                elif contador > 2:
                    arreglo[0] = bandera
                    arreglo[1] = valor_celda_1
                    bandera = arreglo[1]
                    ultimo_numero = arreglo[1].split(".")[-1]
                        
                    bandera_puntos = re.sub(r'[^.]', '', arreglo[0])
                    bandera_puntos2 = re.sub(r'[^.]', '', arreglo[1])
                        
                    if bandera_puntos < bandera_puntos2 and int(ultimo_numero) > 1:
                        return {"error": f"El codigo no puede tener un salto en el nivel de detalle, en este caso el codigo: {arreglo[1]}"}
                        
                dato = {
                    'codigo': valor_celda_1,
                    'descripcion': valor_celda_2,
                    'saldo_actual': valor_celda_3
                }
                contador += 1
                resultados.append(dato)
        
        return {"resultados": resultados,"ola":arreglo}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

    finally:
        # Eliminar el archivo temporal
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
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