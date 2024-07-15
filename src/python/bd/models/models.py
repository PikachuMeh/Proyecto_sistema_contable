from ..base import engine,Base
import datetime
from sqlalchemy import (Double, Table, Column, Integer, String, Text, CHAR, Boolean, Date, Time, TIMESTAMP, ForeignKey,Uuid, BigInteger )
from sqlalchemy.dialects.postgresql import BIT


class TiposCuentas(Base):
    __tablename__ = 'tipos_cuentas'
    id_tipo_cuenta = Column(Integer, primary_key=True, index=True)
    nombre_tipo = Column(String, nullable=False)
    codigo_tipo = Column(Integer, nullable=False, unique=True)
    cuenta_padre_id = Column(Integer, nullable=True)

class AsientosContables(Base):
    __tablename__ = 'asientos_contables'
    id_asientos = Column(Integer, primary_key=True, index=True)
    cuentas_contables_id = Column(Integer, ForeignKey('cuentas_contables.id_cuenta_contable'), nullable=False)
    cuentas_contables_empresas_id = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion_asiento = Column(Text, nullable=False)
    tipo_asiento = Column(Text, nullable=False)
    documento_respaldo = Column(Text, nullable=False)
    plan_cuentas_id = Column(Integer, ForeignKey('plan_cuentas.id_plan_cuentas'), nullable=False)

class Auditoria(Base):
    __tablename__ = 'auditoria'
    id_auditoria = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(String(45), nullable=False)
    accion_realizada = Column(String(45), nullable=False)
    usuarios_idusuarios = Column(Integer, ForeignKey('usuarios.idusuarios'))

class CuentasContables(Base):
    __tablename__ = 'cuentas_contables'
    id_cuenta_contable = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, nullable=False)
    descripcion_cuenta = Column(Text, nullable=False)
    nombre_cuenta = Column(Text, nullable=False)
    nivel_cuenta = Column(Text, nullable=False)
    tipo_cuenta = Column(Text, nullable=False)
    saldo_normal = Column(Double, nullable=False)
    estado_cuenta = Column(Text, nullable=False)
    empresas_id = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)

class Empresas(Base):
    __tablename__ = 'empresas'
    id_empresas = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    fecha_constitucion = Column(Date, nullable=False)
    rif = Column(String(12), nullable=False)
    fecha_ejercicio_economico = Column(Date, nullable=False)
    fecha_contable = Column(Date, nullable=False)
    actividad_economica = Column(String(200), nullable=False)
    direccion = Column(String(200), nullable=False)
    correo = Column(String(200), nullable=False)

class Entidad(Base):
    __tablename__ = 'entidad'
    idEntidad = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    rif = Column(String(15), nullable=False)
    direccion = Column(Text, nullable=False)
    correo = Column(String(200), nullable=False)
    telefono_contacto = Column(Integer, nullable=False)
    persona_contacto = Column(String(200), nullable=False)
    Tipo_contribuyente = Column(Text, nullable=False)

class PlanCuentas(Base):
    __tablename__ = 'plan_cuentas'
    id_plan_cuentas = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, nullable=False)
    descripcion_cuenta = Column(Text, nullable=False)
    registro_empresas = Column(Integer, ForeignKey('empresas.id_empresas'))

class RegistrosMovimientos(Base):
    __tablename__ = 'registros_movimientos'
    id_Registros_Movimientos = Column(Integer, primary_key=True, index=True)
    Fecha_movimiento = Column(Date, nullable=False)
    monto = Column(Double, nullable=False)
    Nro_control = Column(String(200), nullable=False)
    Nro_documento = Column(String(200), nullable=False)
    Empresas_id = Column(Integer, ForeignKey('empresas.id_empresas'))
    entidad_id = Column(Integer, ForeignKey('entidad.idEntidad'))

class RegistroReportes(Base):
    __tablename__ = 'registro_reportes'
    id_registro_reporte = Column(Integer, primary_key=True, index=True)
    registro_reporte = Column(Integer, ForeignKey('reportes.id_reporte'))
    movimientos_id = Column(Integer, ForeignKey('registros_movimientos.id_Registros_Movimientos'))

class Reportes(Base):
    __tablename__ = 'reportes'
    id_reporte = Column(Integer, primary_key=True, index=True)
    tipo_reporte = Column(String(200), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    nivel_detalle = Column(Text, nullable=False)
    formato = Column(Text, nullable=False)
    archivo = Column(Text, nullable=False)

class Roles(Base):
    __tablename__ = 'roles'
    id_rol = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)

class Token(Base):
    __tablename__ = 'token'
    id_token = Column(Integer, primary_key=True, index=True)
    recuperacion = Column(String(45), nullable=False)

class Usuarios(Base):
    __tablename__ = 'usuarios'
    idusuarios = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=False)
    correo = Column(String(45), nullable=False)
    clave = Column(String(45), nullable=False)
    roles_idroles = Column(Integer, ForeignKey('roles.id_rol'))
    token_idtoken = Column(Integer, ForeignKey('token.id_token'))

class UsuarioRegistroMovimiento(Base):
    __tablename__ = 'usuario_registro_movimiento'
    id_registro_movimiento = Column(Integer, primary_key=True, index=True)
    usuarios_idusuarios = Column(Integer, ForeignKey('usuarios.idusuarios'))
    registro_movimiento = Column(Integer, ForeignKey('registros_movimientos.id_Registros_Movimientos'))