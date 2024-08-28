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
from datetime import date
from bd.models.models import AsientosContables,Bitacora,CuentasContables,Empresas,Departamentos,PlanCuentas,RegistrosMovimientos,Reportes,Usuarios,CierreContable,CuentasPrincipales,MovimientosPlan,MovimientosUsuarios
from email.message import EmailMessage
import openpyxl
import random

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

# Función para generar un código aleatorio de hasta 20 caracteres
def generar_codigo_aleatorio(longitud=20):
    caracteres = string.ascii_letters + string.digits
    codigo_aleatorio = ''.join(random.choices(caracteres, k=longitud))
    return codigo_aleatorio

def validar_secuencia(codigos):
    nivel_anterior = []

    for codigo in codigos:
        niveles = [int(n) for n in codigo.split(".")]

        if not nivel_anterior:
            nivel_anterior = niveles
            continue

        for i in range(len(niveles)):
            if i < len(nivel_anterior):
                if niveles[i] < nivel_anterior[i]:
                    raise HTTPException(status_code=400, detail=f"Secuencia inválida: {codigo} no puede seguir a {'.'.join(map(str, nivel_anterior))}")
                elif niveles[i] > nivel_anterior[i]:
                    break  # Avanzó a un nuevo nivel, no necesita más comprobaciones
            else:
                break

        nivel_anterior = niveles

    return True


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
    
def determinar_nivel_tipo(codigo: str) -> str:
    # Determinar el tipo de cuenta según el primer dígito del código
    if codigo.startswith("1"):
        return "Activos"
    elif codigo.startswith("2"):
        return "Pasivos"
    elif codigo.startswith("3"):
        return "Capital/Patrimonio"
    elif codigo.startswith("4"):
        return "Ingresos"
    elif codigo.startswith("5"):
        return "CMV"
    elif codigo.startswith("6"):
        return "Egresos"
    else:
        return "Desconocido"

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

class ActualizarPrincipalRequest(BaseModel):
    es_principal: bool

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

class CuentaNueva(BaseModel):
    codigo: str
    descripcion: str
    saldo: float
class EmpresaCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=1)
    fecha_constitucion: date = Field(...)
    rif: str = Field(..., min_length=1, max_length=10)
    fecha_ejercicio_economico: date = Field(...)
    fecha_contable: date = Field(...)
    actividad_economica: str = Field(..., min_length=1)
    direccion: str = Field(..., min_length=1)
    correo: str = Field(..., min_length=1)

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


        return {"message": "Plan de cuentas y asientos contables creados con éxito."}

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

@app.get("/empresas/{empresa_id}/planes")
def obtener_planes(empresa_id: int):
    plan_cuentas = session.query(PlanCuentas).filter(PlanCuentas.id_empresas == empresa_id).all()
    return plan_cuentas


@app.post("/login/")
async def otro(objeto: Item):
    correo = objeto.correo
    password = objeto.contrasena

    correox = session.query(Usuarios).where(Usuarios.correo == correo).first()

    if correox is None or password != correox.clave:
        return {"Falso": False}
    else:
        return {"correo": correox}

@app.post("/empresas/{empresa_id}/crear-plan")
async def crear_plan(empresa_id: int, archivo: UploadFile = File(...)):
    if not archivo.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un archivo Excel con extensión .xlsx")

    try:
        # Crear un archivo permanente en el sistema de archivos
        carpeta = "uploads"  # Cambia esta ruta al directorio deseado
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ruta_archivo = os.path.join(carpeta, archivo.filename)
        
        # Guardar el archivo
        with open(ruta_archivo, "wb") as buffer:
            buffer.write(await archivo.read())

        # Cargar el archivo Excel con openpyxl
        workbook = openpyxl.load_workbook(ruta_archivo)
        hoja = workbook.active

        # Leer las celdas (ajusta el rango según tus datos)
        celdas = hoja['A1':'C325']
        resultados = []
        codigos = []
        ultimo_nivel = 0

        for fila in celdas:
            valor_celda_1 = str(fila[0].value) if fila[0].value is not None else ""
            valor_celda_2 = str(fila[1].value) if fila[1].value is not None else ""
            valor_celda_3 = float(fila[2].value) if fila[2].value is not None else 0.0

            if not valor_celda_1:
                continue

            nivel_actual = valor_celda_1.count('.')
            if nivel_actual > ultimo_nivel + 1:
                raise HTTPException(status_code=400, detail=f"Error en el código {valor_celda_1}: el código no sigue la jerarquía adecuada.")

            ultimo_nivel = nivel_actual
            codigos.append(valor_celda_1)

            tipo_cuenta = determinar_nivel_tipo(valor_celda_1)

            dato = {
                'codigo': valor_celda_1,
                'descripcion': valor_celda_2,
                'saldo_actual': valor_celda_3,
                'tipo_cuenta': tipo_cuenta
            }
            resultados.append(dato)

        validar_secuencia(codigos)

        # Crear el plan de cuentas
        nuevo_plan = PlanCuentas(
            codigo=generar_codigo_aleatorio(),
            descripcion_cuenta="Plan de cuentas para la empresa " + str(empresa_id),
            id_empresas=empresa_id
        )
        session.add(nuevo_plan)
        session.commit()
        session.refresh(nuevo_plan)
        
        # Verificar si el departamento existe
        departamento = session.query(Departamentos).filter_by(id_empresa=empresa_id).first()
        if not departamento:
            raise HTTPException(status_code=404, detail="El departamento especificado no existe.")

        # Crear un nuevo registro de movimiento en registros_movimientos
        nuevo_movimiento = RegistrosMovimientos(
            fecha_movimiento=date.today(),
            id_empresas=empresa_id,
            nro_control=generar_codigo_aleatorio(),
            nro_documentos=ruta_archivo,
            id_departamentos=departamento.id_departamento  # Asegurando que el departamento no sea None
        )
        session.add(nuevo_movimiento)
        session.commit()
        session.refresh(nuevo_movimiento)

        # Crear un nuevo movimiento en movimientos_plan relacionado con el registro de movimiento creado y el plan de cuentas creado
        nuevo_movimiento_plan = MovimientosPlan(
            id_plan_cuentas=nuevo_plan.id_plan_cuentas,
            id_registro=nuevo_movimiento.id_registros_movimientos
        )
        session.add(nuevo_movimiento_plan)
        session.commit()
        session.refresh(nuevo_movimiento_plan)

        # Insertar cada cuenta en la tabla PlanCuentas
        for resultado in resultados:
            nueva_cuenta = CuentasContables(
                codigo=resultado['codigo'],
                nombre_cuenta=resultado['descripcion'],
                nivel_cuenta="Nivel calculado",
                tipo_cuenta=resultado['tipo_cuenta'],
                saldo_normal=resultado['saldo_actual'],
                estado_cuenta="Activo",
                id_plan_cuenta=nuevo_plan.id_plan_cuentas
            )
            session.add(nueva_cuenta)

        session.commit()

        return {"resultados": resultados}

    except HTTPException as he:
        session.rollback()
        raise he
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    finally:
        session.close()

@app.post("/cuentas/{cuenta_id}/actualizar-principal")
def actualizar_cuenta_principal(cuenta_id: int, request: ActualizarPrincipalRequest):
    # Obtener la cuenta contable
    cuenta = session.query(CuentasContables).filter_by(id_cuenta_contable=cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")
    
    # Actualizar el estado de cuenta principal
    if request.es_principal:
        # Marcar como cuenta principal si no lo es ya
        cuenta_principal = CuentasPrincipales(
            codigo=cuenta.codigo,
            nombre_cuenta=cuenta.nombre_cuenta,
            nivel_cuenta=cuenta.nivel_cuenta,
            tipo_cuenta=cuenta.tipo_cuenta,
            id_cuenta_contable=cuenta.id_cuenta_contable
        )
        session.add(cuenta_principal)
    else:
        # Desmarcar como cuenta principal
        session.query(CuentasPrincipales).filter_by(id_cuenta_contable=cuenta_id).delete()

    session.commit()

    return {"mensaje": "Actualización exitosa"}

@app.get("/empresas/{empresa_id}/planes/{plan_id}/cuentas")
def obtener_cuentas_del_plan(empresa_id: int, plan_id: int):
    print(f"Recibido empresa_id: {empresa_id}, plan_id: {plan_id}")
    
    # Verificar que el plan de cuentas pertenece a la empresa especificada
    plan_cuentas = session.query(PlanCuentas).filter_by(id_plan_cuentas=plan_id, id_empresas=empresa_id).first()
    
    if not plan_cuentas:
        print(f"No se encontró un plan de cuentas para empresa_id={empresa_id}, plan_id={plan_id}")
        raise HTTPException(status_code=404, detail="El plan de cuentas no fue encontrado para esta empresa.")
    
    print(f"Plan de cuentas encontrado: {plan_cuentas.descripcion_cuenta}")
    
    cuentas = session.query(CuentasContables).filter_by(id_plan_cuenta=plan_id).all()

    resultado = []
    for cuenta in cuentas:
        es_principal = session.query(CuentasPrincipales).filter_by(id_cuenta_contable=cuenta.id_cuenta_contable).first() is not None
        resultado.append({
            "id_cuenta_contable": cuenta.id_cuenta_contable,
            "codigo": cuenta.codigo,
            "nombre_cuenta": cuenta.nombre_cuenta,
            "saldo_normal": cuenta.saldo_normal,
            "es_principal": es_principal
        })

    print(f"Se encontraron {len(resultado)} cuentas para el plan_id: {plan_id}")
    return resultado

@app.post("/empresas/{empresa_id}/planes/{plan_id}/cuentas")
def agregar_cuenta(empresa_id: int, plan_id: int, cuenta: CuentaNueva):
    # Verificar que el plan de cuentas pertenece a la empresa especificada
    plan_cuentas = session.query(PlanCuentas).filter_by(id_plan_cuentas=plan_id, id_empresas=empresa_id).first()
    
    if not plan_cuentas:
        raise HTTPException(status_code=404, detail="El plan de cuentas no fue encontrado para esta empresa.")
    
    # Verificar si el código de cuenta ya existe en el plan
    existe_cuenta = session.query(CuentasContables).filter_by(id_plan_cuenta=plan_id, codigo=cuenta.codigo).first()
    if existe_cuenta:
        raise HTTPException(status_code=400, detail="El código de cuenta ya existe en este plan de cuentas.")
    
    # Determinar nivel y tipo de cuenta
    nivel_cuenta = cuenta.codigo.count('.') + 1  # Por ejemplo, '1.1.2' tiene nivel 3
    tipo_cuenta = determinar_nivel_tipo(cuenta.codigo)  # Usa la función para determinar el tipo de cuenta
    
    # Crear la nueva cuenta
    nueva_cuenta = CuentasContables(
        codigo=cuenta.codigo,
        nombre_cuenta=cuenta.descripcion,
        nivel_cuenta=nivel_cuenta,
        tipo_cuenta=tipo_cuenta,
        saldo_normal=cuenta.saldo,
        estado_cuenta="Activo",  # Ajustar según tu lógica de negocio
        id_plan_cuenta=plan_id
    )
    session.add(nueva_cuenta)
    session.commit()
    
    return {"mensaje": "Cuenta agregada con éxito."}


@app.post("/empresas/crear")
def crear_empresa(empresa: EmpresaCreateRequest):
    # Verificar si el RIF ya existe en la base de datos
    existe_empresa = session.query(Empresas).filter_by(rif=empresa.rif).first()
    if existe_empresa:
        raise HTTPException(status_code=400, detail="Ya existe una empresa con este RIF.")

    # Crear la nueva empresa
    nueva_empresa = Empresas(
        nombre=empresa.nombre,
        fecha_constitucion=empresa.fecha_constitucion,
        rif=empresa.rif,
        fecha_ejercicio_economico=empresa.fecha_ejercicio_economico,
        fecha_contable=empresa.fecha_contable,
        actividad_economica=empresa.actividad_economica,
        direccion=empresa.direccion,
        correo=empresa.correo
    )
    session.add(nueva_empresa)
    session.commit()

    return {"mensaje": "Empresa creada con éxito."}
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