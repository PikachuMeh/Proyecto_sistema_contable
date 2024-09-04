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
from datetime import date, datetime, timedelta
from bd.models.models import AsientosContables,Bitacora,PeriodosContables,CuentasContables,CuentasContablesAsientosContables,Empresas,Departamentos,PlanCuentas,RegistrosMovimientos,Reportes,Comprobantes,TipoComprobante,Usuarios,CierreContable,CuentasPrincipales,MovimientosPlan,MovimientosUsuarios
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

def procesar_reporte(asientos_cerrados):
    reporte = []
    for asiento in asientos_cerrados:
        info_asiento = {
            "num_asiento": asiento.num_asiento,
            "fecha_apertura": asiento.cierre.fecha_contable_apertura,
            "fecha_cierre": asiento.cierre.fecha_contable_cierre,
            "cuentas": []
        }

        # Asegúrate de usar el nombre correcto de la relación
        for cuenta_asiento in asiento.cuentas:  # Aquí cambio "cuentas_contables_asientos" a "cuentas"
            info_asiento["cuentas"].append({
                "descripcion_cuenta": cuenta_asiento.cuenta_contable.nombre_cuenta,
                "debe": cuenta_asiento.saldo if cuenta_asiento.tipo_saldo == 'debe' else 0,
                "haber": cuenta_asiento.saldo if cuenta_asiento.tipo_saldo == 'haber' else 0,
            })

        reporte.append(info_asiento)
    return reporte



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
    
# Modelos Pydantic
class CuentaAsientoRequest(BaseModel):
    cuentaId: int
    tipo_saldo: str
    saldo: float

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
    nombre_departamento: str
    id_departamento: int

    
class DepartamentoCrear(BaseModel):
    nombre_departamento: str


class EmpresaCreateRequest(BaseModel):
    nombre: str
    fecha_constitucion: str
    rif: str
    fecha_ejercicio_economico: str
    actividad_economica: str
    direccion: str
    correo: str
    departamentos: List[DepartamentoCrear] = []

class CuentaAsientoRequest(BaseModel):
    cuentaId: int
    tipo_saldo: str
    saldo: float



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

@app.get("/empresas", response_model=List[EmpresaSchema])
def obtener_empresas(db: Session = Depends(get_db)):
    """
    Endpoint para obtener todas las empresas.
    """
    try:
        empresas = db.query(Empresas).all()
        if not empresas:
            raise HTTPException(status_code=404, detail="No se encontraron empresas")
        return empresas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las empresas: {str(e)}")


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
    try:
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

    except HTTPException as e:
        db.rollback()
        print(f"HTTPException: {e.detail}")  # Agrega este print para depurar
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error al crear la empresa: {e}")  # Agrega este print para depurar
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@app.get("/tipo_comprobante")
def get_tipos_comprobante(db: Session = Depends(get_db)):
    return db.query(TipoComprobante).all()

@app.get("/asientos")
def get_asientos(empresa_id: int = None, asiento_id: int = None, db: Session = Depends(get_db)):
    """
    Endpoint para obtener los asientos contables. 
    - Si se proporciona `asiento_id`, devolverá el asiento específico.
    - Si se proporciona `empresa_id`, devolverá todos los asientos de la empresa.
    """
    try:
        if asiento_id:
            # Obtener un asiento específico
            asiento = db.query(AsientosContables)\
                .filter(AsientosContables.id_asiento_contable == asiento_id)\
                .first()

            if not asiento:
                raise HTTPException(status_code=404, detail="Asiento no encontrado")

            # Verificar el estado del cierre contable
            cierre = db.query(CierreContable).filter_by(id_cierre_contable=asiento.cierre_contable).first()
            estado_asiento = "Cerrado" if cierre and cierre.estado == "Cerrado" else "Abierto"

            # Obtener las cuentas asociadas
            cuentas_asiento = db.query(CuentasContablesAsientosContables)\
                .filter_by(id_asiento_contable=asiento_id)\
                .all()

            cuentas_detalles = [{
                "id": cuenta_asiento.id_cuenta_asiento,
                "nombre_cuenta": cuenta_asiento.cuenta_contable.nombre_cuenta,
                "tipo_saldo": cuenta_asiento.tipo_saldo,
                "saldo": cuenta_asiento.saldo
            } for cuenta_asiento in cuentas_asiento]

            return {
                "num_asiento": asiento.num_asiento,
                "tipo_comprobante": asiento.tipo_comprobante,
                "fecha": asiento.fecha,
                "cuentas": cuentas_detalles,
                "estado": estado_asiento
            }

        elif empresa_id:
            # Obtener todos los asientos de una empresa
            asientos = db.query(AsientosContables)\
                         .filter(AsientosContables.id_empresas == empresa_id)\
                         .all()

            if not asientos:
                raise HTTPException(status_code=404, detail="No se encontraron asientos para esta empresa.")

            resultado = []
            for asiento in asientos:
                # Verificar el estado del cierre contable para cada asiento
                cierre = db.query(CierreContable).filter_by(id_cierre_contable=asiento.cierre_contable).first()
                estado_asiento = "Cerrado" if cierre and cierre.estado == "Cerrado" else "Abierto"

                cuentas_asiento = db.query(CuentasContablesAsientosContables)\
                    .filter_by(id_asiento_contable=asiento.id_asiento_contable)\
                    .all()

                cuentas_detalles = [{
                    "id": cuenta_asiento.id_cuenta_asiento,
                    "nombre_cuenta": cuenta_asiento.cuenta_contable.nombre_cuenta,
                    "tipo_saldo": cuenta_asiento.tipo_saldo,
                    "saldo": cuenta_asiento.saldo
                } for cuenta_asiento in cuentas_asiento]

                resultado.append({
                    "num_asiento": asiento.num_asiento,
                    "tipo_comprobante": asiento.tipo_comprobante,
                    "fecha": asiento.fecha,
                    "cuentas": cuentas_detalles,
                    "estado": estado_asiento
                })

            return resultado

        else:
            raise HTTPException(status_code=400, detail="Debe proporcionar `empresa_id` o `asiento_id`")

    except Exception as e:
        print(f"Error al obtener los asientos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


#Para los asientos en si
@app.get("/asientos/{empresa_id}")
def get_asientos_empresa(empresa_id: int, db: Session = Depends(get_db)):
    asientos = db.query(AsientosContables).filter(AsientosContables.id_empresas == empresa_id).all()
    if not asientos:
        raise HTTPException(status_code=404, detail="No se encontraron asientos para esta empresa.")
    return asientos

@app.post("/asientos")
def create_asiento(
    num_asiento: int = Form(...),
    tipo_comprobante: int = Form(...),
    fecha: str = Form(...),
    documento_respaldo: UploadFile = File(...),
    empresa_id: int = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Verificar si el número de asiento ya existe para la misma empresa
        existing_asiento = db.query(AsientosContables).filter(
            AsientosContables.num_asiento == num_asiento,
            AsientosContables.id_empresas == empresa_id
        ).first()

        if existing_asiento:
            raise HTTPException(status_code=400, detail="El número de asiento ya existe para esta empresa.")

        # Crear un nuevo cierre contable para este asiento
        nuevo_cierre_contable = CierreContable(
            estado='Abierto',
            fecha_contable_apertura=date.today(),
            fecha_contable_cierre="0000-00-00"  # Al estar abierto, le asignamos "0000-00-00"
        )
        db.add(nuevo_cierre_contable)
        db.commit()
        db.refresh(nuevo_cierre_contable)

        # Guardar el archivo de respaldo del asiento
        ruta_archivo = f"uploads/{documento_respaldo.filename}"
        with open(ruta_archivo, "wb") as buffer:
            buffer.write(documento_respaldo.file.read())

        # Crear el nuevo asiento contable vinculado al cierre contable
        nuevo_asiento = AsientosContables(
            num_asiento=num_asiento,
            tipo_comprobante=tipo_comprobante,
            fecha=fecha,
            documento_respaldo="",
            cierre_contable=nuevo_cierre_contable.id_cierre_contable,  # Asignar el id del cierre contable recién creado
            id_empresas=empresa_id
        )
        db.add(nuevo_asiento)
        db.commit()
        db.refresh(nuevo_asiento)

        # Crear el comprobante asociado
        nuevo_comprobante = Comprobantes(
            titulo=f"Comprobante para el asiento contable {nuevo_asiento.num_asiento}",
            descripcion="Descripción del comprobante generado automáticamente.",
            fecha=date.today(),
            archivo=ruta_archivo,
            tipo_comprobante=tipo_comprobante
        )
        db.add(nuevo_comprobante)
        db.commit()
        db.refresh(nuevo_comprobante)

        # Asignar el comprobante al asiento contable
        nuevo_asiento.documento_respaldo = nuevo_comprobante.id_comprobante
        db.commit()

        return {"mensaje": "Asiento creado con éxito", "asiento": nuevo_asiento}

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    
# Obtener todos los asientos de una empresa
@app.get("/asientos/empresa/{empresa_id}")
def get_asientos_por_empresa(empresa_id: int, db: Session = Depends(get_db)):
    asientos = db.query(AsientosContables)\
                 .options(joinedload(AsientosContables.cuentas))\
                 .filter(AsientosContables.id_empresas == empresa_id).all()

    if not asientos:
        raise HTTPException(status_code=404, detail="No se encontraron asientos para esta empresa.")

    resultado = []
    for asiento in asientos:
        # Verificar si el asiento está cerrado
        cierre = db.query(CierreContable).filter(CierreContable.id_cierre_contable == asiento.cierre_contable).first()
        estado_asiento = "Abierto"
        if cierre and cierre.estado == 'Cerrado':
            estado_asiento = "Cerrado"

        # Obtener las cuentas asociadas al asiento desde la tabla intermediaria
        cuentas_asiento = db.query(CuentasContablesAsientosContables).filter_by(id_asiento_contable=asiento.id_asiento_contable).all()

        cuentas_detalles = []
        for cuenta_asiento in cuentas_asiento:
            cuenta_contable = db.query(CuentasContables).filter_by(id_cuenta_contable=cuenta_asiento.id_cuenta_contable).first()
            cuentas_detalles.append({
                "id": cuenta_asiento.id_cuenta_asiento,
                "nombre_cuenta": cuenta_contable.nombre_cuenta,
                "tipo_saldo": cuenta_asiento.tipo_saldo,
                "saldo": cuenta_asiento.saldo
            })

        resultado.append({
            "num_asiento": asiento.num_asiento,
            "tipo_comprobante": asiento.tipo_comprobante,
            "fecha": asiento.fecha,
            "cuentas": cuentas_detalles,
            "estado": estado_asiento
        })

    return resultado


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

# Agregar una cuenta a un asiento contable existente
@app.post("/asientos/{asiento_id}/cuentas")
def add_cuenta_to_asiento(asiento_id: int, cuenta: CuentaAsientoRequest, db: Session = Depends(get_db)):
    asiento = db.query(AsientosContables).filter(AsientosContables.id_asiento_contable == asiento_id).first()
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento no encontrado")

    # Agregar la cuenta al asiento contable
    cuenta_asiento = CuentasContablesAsientosContables(
        id_asiento_contable=asiento_id,
        id_cuenta_contable=cuenta.cuentaId,
        tipo_saldo=cuenta.tipo_saldo,
        saldo=cuenta.saldo
    )
    db.add(cuenta_asiento)
    db.commit()

    return {"mensaje": "Cuenta agregada con éxito al asiento", "cuenta": cuenta_asiento}


@app.get("/empresas/{empresa_id}/cuentas_no_principales")
def obtener_cuentas_no_principales(empresa_id: int, db: Session = Depends(get_db)):
    # Primero, obtén el ID del plan de cuentas asociado con la empresa
    plan_cuentas = db.query(PlanCuentas).filter(PlanCuentas.id_empresas == empresa_id).first()

    if not plan_cuentas:
        raise HTTPException(status_code=404, detail="No se encontró un plan de cuentas para esta empresa.")

    # Obtén las cuentas contables que no son principales
    cuentas_no_principales = db.query(CuentasContables).filter(
        CuentasContables.id_plan_cuenta == plan_cuentas.id_plan_cuentas,
        ~CuentasContables.id_cuenta_contable.in_(
            db.query(CuentasPrincipales.id_cuenta_contable)
        )
    ).all()

    return cuentas_no_principales

@app.post("/tipo_comprobante/crear")
def crear_tipo_comprobante(request: TipoComprobanteCreateRequest, db: Session = Depends(get_db)):
    nuevo_tipo = TipoComprobante(nombre_comprobante=request.nombre_comprobante)
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return {"mensaje": "Tipo de comprobante creado con éxito"}

@app.get("/asientos/verificar/{empresa_id}/{num_asiento}")
def verificar_numero_asiento(empresa_id: int, num_asiento: int, db: Session = Depends(get_db)):
    # Verificar si el número de asiento ya existe para la misma empresa
    existing_asiento = db.query(AsientosContables).filter(
        AsientosContables.num_asiento == num_asiento,
        AsientosContables.id_empresas == empresa_id
    ).first()

    if existing_asiento:
        return {"exists": True}
    else:
        return {"exists": False}

@app.delete("/asientos/{asiento_id}/cuentas/{cuenta_asiento_id}")
def eliminar_cuenta_asiento(asiento_id: int, cuenta_asiento_id: int, db: Session = Depends(get_db)):
    # Obtener la cuenta contable asociada al asiento
    cuenta_asiento = db.query(CuentasContablesAsientosContables).filter_by(id_cuenta_asiento=cuenta_asiento_id, id_asiento_contable=asiento_id).first()

    if not cuenta_asiento:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada o no pertenece al asiento.")

    # Eliminar la cuenta del asiento
    db.delete(cuenta_asiento)
    db.commit()

    return {"mensaje": "Cuenta eliminada del asiento correctamente."}

@app.post("/asientos/{asiento_id}/cerrar")
def cerrar_asiento(asiento_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para cerrar un asiento contable.
    """
    try:
        # Obtener el asiento contable
        asiento = db.query(AsientosContables).filter_by(id_asiento_contable=asiento_id).first()

        if not asiento:
            raise HTTPException(status_code=404, detail="Asiento no encontrado")

        # Obtener el cierre contable relacionado con el asiento
        cierre = db.query(CierreContable).filter_by(id_cierre_contable=asiento.cierre_contable).first()

        if not cierre:
            raise HTTPException(status_code=404, detail="Cierre contable no encontrado")

        if cierre.estado == 'Cerrado':
            raise HTTPException(status_code=400, detail="El asiento ya está cerrado")

        # Validación: Verificar que el asiento contable esté balanceado (Debe = Haber)
        cuentas_asiento = db.query(CuentasContablesAsientosContables).filter_by(id_asiento_contable=asiento_id).all()

        total_debe = 0
        total_haber = 0

        for cuenta in cuentas_asiento:
            if cuenta.tipo_saldo.lower() == "debe":
                total_debe += cuenta.saldo
            elif cuenta.tipo_saldo.lower() == "haber":
                total_haber += cuenta.saldo

        if total_debe != total_haber:
            raise HTTPException(status_code=400, detail=f"El asiento no cuadra: Debe ({total_debe}) y Haber ({total_haber}) no son iguales.")

        # Si el asiento está balanceado, proceder a cerrar
        cierre.estado = 'Cerrado'
        cierre.fecha_contable_cierre = date.today()  # Cambiamos la fecha de cierre al día actual

        db.commit()

        return {"mensaje": "Asiento cerrado con éxito"}

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al cerrar el asiento: {str(e)}")


@app.post("/comprobantes/crear")
def crear_comprobante(asiento_id: int, archivo: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Buscar el asiento contable correspondiente
        asiento = db.query(AsientosContables).filter_by(id_asiento_contable=asiento_id).first()
        if not asiento:
            raise HTTPException(status_code=404, detail="Asiento no encontrado")

        # Asignar un nombre personalizado al archivo
        nuevo_nombre_archivo = f"Comprobante_para_asiento_contable_{asiento.num_asiento}.xlsx"

        # Guardar el archivo con el nuevo nombre
        ruta_archivo = f"uploads/{nuevo_nombre_archivo}"
        with open(ruta_archivo, "wb") as buffer:
            buffer.write(archivo.file.read())

        # Crear el comprobante
        nuevo_comprobante = Comprobantes(
            titulo=f"Comprobante para el asiento contable {asiento.num_asiento}",
            descripcion="Descripción del comprobante generado automáticamente.",
            fecha=date.today(),
            archivo=ruta_archivo,
            tipo_comprobante=asiento.tipo_comprobante
        )
        db.add(nuevo_comprobante)
        db.commit()
        db.refresh(nuevo_comprobante)

        # Asignar el comprobante al asiento
        asiento.documento_respaldo = nuevo_comprobante.id_comprobante
        db.commit()

        return {"mensaje": "Comprobante creado y asignado al asiento con éxito"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el comprobante: {str(e)}")
    
# Añadir un endpoint para iniciar un nuevo periodo contable
@app.post("/empresas/{empresa_id}/iniciar_periodo")
def iniciar_periodo_contable(empresa_id: int, db: Session = Depends(get_db)):
    # Obtener el último periodo contable de la empresa
    ultimo_periodo = db.query(PeriodosContables).filter(
        PeriodosContables.id_empresa == empresa_id
    ).order_by(PeriodosContables.numero_periodo.desc()).first()

    if ultimo_periodo and ultimo_periodo.estado == 'Abierto':
        raise HTTPException(status_code=400, detail="No se puede iniciar un nuevo periodo mientras el anterior está abierto.")

    nuevo_numero_periodo = 1 if not ultimo_periodo else ultimo_periodo.numero_periodo + 1
    fecha_inicio = date.today()
    fecha_fin = fecha_inicio.replace(day=1) + timedelta(days=32)
    fecha_fin = fecha_fin.replace(day=1) - timedelta(days=1)

    nuevo_periodo = PeriodosContables(
        id_empresa=empresa_id,
        numero_periodo=nuevo_numero_periodo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado='Abierto'
    )

    db.add(nuevo_periodo)
    db.commit()
    db.refresh(nuevo_periodo)

    return {"mensaje": "Nuevo periodo contable iniciado con éxito", "periodo": nuevo_periodo}


# Endpoint para cerrar un periodo contable (ya incluido antes)
@app.post("/empresas/{empresa_id}/cerrar_periodo/{numero_periodo}")
def cerrar_periodo_contable(empresa_id: int, numero_periodo: int, db: Session = Depends(get_db)):
    periodo = db.query(PeriodosContables).filter(
        PeriodosContables.id_empresa == empresa_id,
        PeriodosContables.numero_periodo == numero_periodo,
        PeriodosContables.estado == 'Abierto'
    ).first()

    if not periodo:
        raise HTTPException(status_code=404, detail="Periodo contable no encontrado o ya está cerrado")

    # Obtener todos los asientos cerrados del periodo
    asientos_cerrados = db.query(AsientosContables).filter(
        AsientosContables.id_empresas == empresa_id,
        AsientosContables.fecha.between(periodo.fecha_inicio, periodo.fecha_fin),
        AsientosContables.cierre_contable != None
    ).all()

    # Verificar si todos los asientos están cerrados
    if not asientos_cerrados:
        raise HTTPException(status_code=400, detail="No se encontraron asientos cerrados para cerrar el periodo contable")

    periodo.estado = 'Cerrado'
    db.commit()

    return {"mensaje": "Periodo contable cerrado correctamente"}

# Endpoint para generar reportes (ya incluido antes)
@app.post("/reportes/{tipo_reporte}")
def generar_reporte(tipo_reporte: str, request: dict, db: Session = Depends(get_db)):
    fecha_reporte = request.get('fecha')
    empresa_id = request.get('empresa_id')  # Obtener el ID de la empresa seleccionada

    if not fecha_reporte:
        raise HTTPException(status_code=400, detail="Fecha no proporcionada")

    if not empresa_id:
        raise HTTPException(status_code=400, detail="Empresa no proporcionada")

    asientos_cerrados = []
    if tipo_reporte == 'diario':
        asientos_cerrados = db.query(AsientosContables).join(CierreContable).filter(
            CierreContable.estado == 'Cerrado',
            AsientosContables.fecha == fecha_reporte,
            AsientosContables.id_empresas == empresa_id  # Filtrar por empresa
        ).all()

    elif tipo_reporte == 'mensual':
        mes_inicio = f"{fecha_reporte}-01"
        mes_fin = f"{fecha_reporte}-31"

        asientos = db.query(AsientosContables).filter(
            AsientosContables.fecha.between(mes_inicio, mes_fin),
            AsientosContables.id_empresas == empresa_id  # Filtrar por empresa
        ).all()

        for asiento in asientos:
            if asiento.cierre.estado != 'Cerrado':
                raise HTTPException(status_code=400, detail=f"El asiento {asiento.num_asiento} no está cerrado.")
            asientos_cerrados.append(asiento)

    else:
        raise HTTPException(status_code=400, detail="Tipo de reporte inválido")

    if not asientos_cerrados:
        raise HTTPException(status_code=404, detail="No se encontraron asientos cerrados para el periodo seleccionado")

    reporte = procesar_reporte(asientos_cerrados)
    return reporte

@app.post("/reportes/diario")
def generar_reporte_diario(fecha: str, empresa_id: int, db: Session = Depends(get_db)):
    asientos_cerrados = db.query(AsientosContables).join(CierreContable).filter(
        CierreContable.estado == 'Cerrado',
        AsientosContables.fecha == fecha,
        AsientosContables.id_empresas == empresa_id  # Filtrar por empresa
    ).all()

    if not asientos_cerrados:
        raise HTTPException(status_code=404, detail="No se encontraron asientos cerrados para esta fecha.")

    reporte = procesar_reporte(asientos_cerrados)
    return reporte

@app.post("/reportes/mensual")
def generar_reporte_mensual(mes: str, empresa_id: int, db: Session = Depends(get_db)):
    mes_inicio = f"{mes}-01"
    mes_fin = f"{mes}-31"

    asientos = db.query(AsientosContables).filter(
        AsientosContables.fecha.between(mes_inicio, mes_fin),
        AsientosContables.id_empresas == empresa_id  # Filtrar por empresa
    ).all()

    # Verificar que todos los asientos del mes estén cerrados
    for asiento in asientos:
        cierre = db.query(CierreContable).filter(CierreContable.id_cierre_contable == asiento.cierre_contable).first()
        if not cierre or cierre.estado != 'Cerrado':
            raise HTTPException(status_code=400, detail="No se puede generar el reporte mensual porque uno o más asientos no están cerrados.")

    reporte = procesar_reporte(asientos)
    return reporte
