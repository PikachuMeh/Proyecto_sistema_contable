import os
from dotenv import load_dotenv
from typing import Union, List
from pydantic import BaseModel,Field
from fastapi import FastAPI,HTTPException,Depends,File,UploadFile,Form
from fastapi.middleware.cors import CORSMiddleware
from bd.base import Base,SessionLocal
from sqlalchemy.orm import Session,joinedload
import tempfile
import string
import json
import re
from datetime import date, datetime
from bd.models.models import AsientosContables,Bitacora,CuentasContables,CuentasContablesAsientosContables,Empresas,Departamentos,PlanCuentas,RegistrosMovimientos,Reportes,Comprobantes,TipoComprobante,Usuarios,CierreContable,CuentasPrincipales,MovimientosPlan,MovimientosUsuarios
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

# Modelo para la creación de comprobante
class ComprobanteCreateRequest(BaseModel):
    titulo: str
    descripcion: str
    fecha: str
    tipo_comprobante: int

# Modelo para la creación de tipo de comprobante
class TipoComprobanteCreateRequest(BaseModel):
    nombre_comprobante: str

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

class DepartamentoResponse(BaseModel):
    id_departamento: int
    nombre_departamento: str

class EmpresaCreateRequest(BaseModel):
    nombre: str
    fecha_constitucion: str
    rif: str
    fecha_ejercicio_economico: str
    actividad_economica: str
    direccion: str
    correo: str
    departamentos: List[DepartamentoResponse] = []

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index():
    return "hola mundo!"

@app.post("/buscar-empresas", response_model=list[EmpresaSchema])
def buscar_empresas(request: BuscarEmpresaRequest, db: Session = Depends(get_db)):
    empresas = db.query(Empresas).filter(Empresas.rif.ilike(f"%{request.query}%")).all()
    if not empresas:
        raise HTTPException(status_code=404, detail="No companies found")
    return empresas

@app.get("/empresas/{empresa_id}/planes")
def obtener_planes(empresa_id: int, db: Session = Depends(get_db)):
    plan_cuentas = db.query(PlanCuentas).filter(PlanCuentas.id_empresas == empresa_id).all()
    return plan_cuentas

@app.get("/empresas/{empresa_id}/departamentos", response_model=List[DepartamentoResponse])
def obtener_departamentos_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    departamentos = db.query(Departamentos).filter(Departamentos.id_empresa == empresa_id).all()
    if not departamentos:
        raise HTTPException(status_code=404, detail="No se encontraron departamentos para esta empresa.")
    return departamentos

@app.post("/login/")
async def otro(objeto: Item, db: Session = Depends(get_db)):
    correo = objeto.correo
    password = objeto.contrasena

    correox = db.query(Usuarios).where(Usuarios.correo == correo).first()

    if correox is None or password != correox.clave:
        return {"Falso": False}
    else:
        return {"correo": correox}

@app.post("/empresas/{empresa_id}/crear-plan")
async def crear_plan(empresa_id: int, departamento_id: int = Form(...), archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    if not archivo.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un archivo Excel con extensión .xlsx")

    try:
        # Guardar el archivo subido en el sistema de archivos
        carpeta = "uploads"
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        ruta_archivo = os.path.join(carpeta, archivo.filename)
        with open(ruta_archivo, "wb") as buffer:
            buffer.write(await archivo.read())

        # Procesar el archivo Excel
        workbook = openpyxl.load_workbook(ruta_archivo)
        hoja = workbook.active

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
        db.add(nuevo_plan)
        db.commit()
        db.refresh(nuevo_plan)

        # Crear un nuevo registro de movimiento
        nuevo_movimiento = RegistrosMovimientos(
            fecha_movimiento=date.today(),
            id_empresas=empresa_id,
            nro_control=generar_codigo_aleatorio(),
            nro_documentos=ruta_archivo,
            id_departamentos=departamento_id  # Asociar el departamento
        )
        db.add(nuevo_movimiento)
        db.commit()
        db.refresh(nuevo_movimiento)

        nuevo_movimiento_plan = MovimientosPlan(
            id_plan_cuentas=nuevo_plan.id_plan_cuentas,
            id_registro=nuevo_movimiento.id_registros_movimientos
        )
        db.add(nuevo_movimiento_plan)
        db.commit()
        db.refresh(nuevo_movimiento_plan)

        # Insertar cada cuenta contable en la base de datos
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
            db.add(nueva_cuenta)

        db.commit()

        return {"resultados": resultados}

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

@app.post("/cuentas/{cuenta_id}/actualizar-principal")
def actualizar_cuenta_principal(cuenta_id: int, request: ActualizarPrincipalRequest, db: Session = Depends(get_db)):
    cuenta = db.query(CuentasContables).filter_by(id_cuenta_contable=cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada.")
    
    if request.es_principal:
        cuenta_principal = CuentasPrincipales(
            codigo=cuenta.codigo,
            nombre_cuenta=cuenta.nombre_cuenta,
            nivel_cuenta=cuenta.nivel_cuenta,
            tipo_cuenta=cuenta.tipo_cuenta,
            id_cuenta_contable=cuenta.id_cuenta_contable
        )
        db.add(cuenta_principal)
    else:
        db.query(CuentasPrincipales).filter_by(id_cuenta_contable=cuenta_id).delete()

    db.commit()

    return {"mensaje": "Actualización exitosa"}

@app.get("/empresas/{empresa_id}/planes/{plan_id}/cuentas")
def obtener_cuentas_del_plan(empresa_id: int, plan_id: int, db: Session = Depends(get_db)):
    print(f"Recibido empresa_id: {empresa_id}, plan_id: {plan_id}")
    
    plan_cuentas = db.query(PlanCuentas).filter_by(id_plan_cuentas=plan_id, id_empresas=empresa_id).first()
    
    if not plan_cuentas:
        print(f"No se encontró un plan de cuentas para empresa_id={empresa_id}, plan_id={plan_id}")
        raise HTTPException(status_code=404, detail="El plan de cuentas no fue encontrado para esta empresa.")
    
    print(f"Plan de cuentas encontrado: {plan_cuentas.descripcion_cuenta}")
    
    cuentas = db.query(CuentasContables).filter_by(id_plan_cuenta=plan_id).all()

    resultado = []
    for cuenta in cuentas:
        es_principal = db.query(CuentasPrincipales).filter_by(id_cuenta_contable=cuenta.id_cuenta_contable).first() is not None
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
def agregar_cuenta(empresa_id: int, plan_id: int, cuenta: CuentaNueva, db: Session = Depends(get_db)):
    plan_cuentas = db.query(PlanCuentas).filter_by(id_plan_cuentas=plan_id, id_empresas=empresa_id).first()
    
    if not plan_cuentas:
        raise HTTPException(status_code=404, detail="El plan de cuentas no fue encontrado para esta empresa.")
    
    existe_cuenta = db.query(CuentasContables).filter_by(id_plan_cuenta=plan_id, codigo=cuenta.codigo).first()
    if existe_cuenta:
        raise HTTPException(status_code=400, detail="El código de cuenta ya existe en este plan de cuentas.")
    
    nivel_cuenta = cuenta.codigo.count('.') + 1
    tipo_cuenta = determinar_nivel_tipo(cuenta.codigo)
    
    nueva_cuenta = CuentasContables(
        codigo=cuenta.codigo,
        nombre_cuenta=cuenta.descripcion,
        nivel_cuenta=nivel_cuenta,
        tipo_cuenta=tipo_cuenta,
        saldo_normal=cuenta.saldo,
        estado_cuenta="Activo",
        id_plan_cuenta=plan_id
    )
    db.add(nueva_cuenta)
    db.commit()
    
    return {"mensaje": "Cuenta agregada con éxito."}

@app.post("/empresas/crear")
def crear_empresa(empresa: EmpresaCreateRequest, db: Session = Depends(get_db)):
    existe_empresa = db.query(Empresas).filter_by(rif=empresa.rif).first()
    if existe_empresa:
        raise HTTPException(status_code=400, detail="Ya existe una empresa con este RIF.")

    nueva_empresa = Empresas(
        nombre=empresa.nombre,
        fecha_constitucion=empresa.fecha_constitucion,
        rif=empresa.rif,
        fecha_ejercicio_economico=empresa.fecha_ejercicio_economico,
        actividad_economica=empresa.actividad_economica,
        direccion=empresa.direccion,
        correo=empresa.correo
    )
    db.add(nueva_empresa)
    db.commit()
    db.refresh(nueva_empresa)

    for depto in empresa.departamentos:
        nuevo_departamento = Departamentos(
            nombre_departamento=depto.nombre_departamento,
            id_empresa=nueva_empresa.id_empresas
        )
        db.add(nuevo_departamento)

    db.commit()

    return {"mensaje": "Empresa y departamentos creados con éxito.", "empresa_id": nueva_empresa.id_empresas}

@app.get("/tipo_comprobante")
def get_tipos_comprobante(db: Session = Depends(get_db)):
    return db.query(TipoComprobante).all()

@app.get("/asientos")
def get_asientos(db: Session = Depends(get_db)):
    try:
        print("Obteniendo asientos contables...")
        asientos = db.query(AsientosContables).all()
        print(f"Se encontraron {len(asientos)} asientos contables.")
        return asientos
    except Exception as e:
        print(f"Error al obtener los asientos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.post("/asientos")
def create_asiento(
    num_asiento: int = Form(...),
    tipo_comprobante: int = Form(...),
    fecha: str = Form(...),
    documento_respaldo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        cierre_abierto = db.query(CierreContable).filter_by(estado='Abierto').first()

        if not cierre_abierto:
            cierre_abierto = CierreContable(
                estado='Abierto',
                fecha_contable_apertura=date.today(),
                fecha_contable_cierre='0000-00-00'
            )
            db.add(cierre_abierto)
            db.commit()
            db.refresh(cierre_abierto)

        ruta_archivo = f"uploads/{documento_respaldo.filename}"
        with open(ruta_archivo, "wb") as buffer:
            buffer.write(documento_respaldo.file.read())

        nuevo_asiento = AsientosContables(
            num_asiento=num_asiento,
            tipo_comprobante=tipo_comprobante,
            fecha=fecha,
            documento_respaldo=ruta_archivo,
            cierre_contable=cierre_abierto.id_cierre_contable
        )
        db.add(nuevo_asiento)
        db.commit()
        db.refresh(nuevo_asiento)

        return nuevo_asiento

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/asientos/{asiento_id}")
def get_asiento(asiento_id: int, db: Session = Depends(get_db)):
    asiento = db.query(AsientosContables).filter_by(id_asiento_contable=asiento_id).first()

    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")

    print(f"Asiento encontrado: {asiento}")  # Verifica que el asiento se cargue

    # Intentamos acceder al comprobante
    comprobante = asiento.comprobante
    if comprobante:
        print(f"Comprobante encontrado: {comprobante}")
        if comprobante.tipo:
            print(f"Tipo de comprobante encontrado: {comprobante.tipo.nombre_comprobante}")
        else:
            print("El tipo de comprobante no se encontró.")
    else:
        raise HTTPException(status_code=404, detail="El comprobante no fue encontrado para este asiento")
    
    cuentas_asiento = db.query(CuentasContablesAsientosContables).filter_by(id_asiento_contable=asiento_id).all()
    cuentas = [
        {
            "nombre_cuenta": cuenta.cuenta_contable.nombre_cuenta,
            "debe_haber": cuenta.debe_haber,
            "monto": cuenta.monto
        }
        for cuenta in cuentas_asiento
    ]
    
    return {
        "num_asiento": asiento.num_asiento,
        "tipo_comprobante": comprobante.tipo.nombre_comprobante if comprobante and comprobante.tipo else "Desconocido",
        "fecha": asiento.fecha,
        "cuentas": cuentas
    }

@app.put("/asientos/{asiento_id}")
def modificar_asiento(asiento_id: int, nuevo_num_asiento: int, nuevo_tipo_comprobante: int, db: Session = Depends(get_db)):
    asiento = db.query(AsientosContables).filter_by(id_asiento_contable=asiento_id).first()
    
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")
    
    cierre = db.query(CierreContable).filter_by(id_cierre_contable=asiento.cierre_contable).first()
    
    if cierre.estado != 'Abierto':
        raise HTTPException(status_code=400, detail="No se puede modificar un asiento contable en un cierre cerrado.")
    
    asiento.num_asiento = nuevo_num_asiento
    asiento.tipo_comprobante = nuevo_tipo_comprobante
    db.commit()
    
    return {"mensaje": "Asiento contable modificado con éxito."}

@app.post("/cierre-contable/{cierre_id}/cerrar")
def cerrar_cierre_contable(cierre_id: int, db: Session = Depends(get_db)):
    cierre = db.query(CierreContable).filter_by(id_cierre_contable=cierre_id).first()
    
    if not cierre:
        raise HTTPException(status_code=404, detail="Cierre contable no encontrado")
    
    if cierre.estado == 'Cerrado':
        raise HTTPException(status_code=400, detail="El cierre contable ya está cerrado.")
    
    cierre.estado = 'Cerrado'
    cierre.fecha_contable_cierre = date.today()
    db.commit()
    
    return {"mensaje": "Cierre contable cerrado con éxito."}

@app.post("/asientos/{asiento_id}/cuentas")
def add_cuenta_to_asiento(asiento_id: int, cuentaId: int, debe_haber: str, monto: float, db: Session = Depends(get_db)):
    asiento = db.query(AsientosContables).filter(AsientosContables.id_asiento_contable == asiento_id).first()
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")

    cuenta_asiento = CuentasContablesAsientosContables(
        id_asiento_contable=asiento_id,
        id_cuenta_contable=cuentaId,
        debe_haber=debe_haber,
        monto=monto
    )
    db.add(cuenta_asiento)
    db.commit()
    db.refresh(asiento)

    return asiento

@app.post("/tipo_comprobante/crear")
def crear_tipo_comprobante(request: TipoComprobanteCreateRequest, db: Session = Depends(get_db)):
    nuevo_tipo = TipoComprobante(nombre_comprobante=request.nombre_comprobante)
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return {"mensaje": "Tipo de comprobante creado con éxito"}

@app.post("/comprobantes/crear")
def crear_comprobante(titulo: str, descripcion: str, fecha: str, tipo_comprobante: int, archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    ruta_archivo = f"uploads/{archivo.filename}"
    with open(ruta_archivo, "wb") as buffer:
        buffer.write(archivo.file.read())

    nuevo_comprobante = Comprobantes(
        titulo=titulo,
        descripcion=descripcion,
        fecha=fecha,
        archivo=ruta_archivo,
        tipo_comprobante=tipo_comprobante
    )
    db.add(nuevo_comprobante)
    db.commit()
    db.refresh(nuevo_comprobante)
    return {"mensaje": "Comprobante creado con éxito"}