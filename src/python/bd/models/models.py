from ..base import engine, Base  # Importa Base desde base.py
import datetime
from sqlalchemy import (Double, Table, Column, Integer, String, Text, Float, CHAR, Boolean, Date, Time, TIMESTAMP, ForeignKey, Uuid, BigInteger,VARCHAR)
from sqlalchemy.orm import relationship

class AsientosContables(Base):
    __tablename__ = 'asientos_contables'

    id_asiento_contable = Column(Integer, primary_key=True, autoincrement=True)
    num_asiento = Column(Integer, nullable=False)
    documento_respaldo = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    id_empresas = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)
    cierre_contable = Column(Integer, ForeignKey('cierre_contable.id_cierre_contable'), nullable=False)
    tipo_comprobante = Column(Integer, ForeignKey('tipo_comprobante.id_tipo_comprobante'), nullable=False)
    id_cuentas_principales = Column(Integer, ForeignKey('cuentas_principales.id_cuentas_principales'), nullable=True)

    # Relación con otras tablas
    empresa = relationship("Empresas", back_populates="asientos_contables")
    cierre = relationship("CierreContable", back_populates="asientos_contables")
    comprobante = relationship("TipoComprobante", back_populates="asientos")
    cuentas_principales = relationship("CuentasPrincipales", back_populates="asientos_contables")
    cuentas = relationship("CuentasContablesAsientosContables", back_populates="asiento_contable")
    reportes = relationship("Reportes", back_populates="asiento_contable")  # Agrega esta relación


class Bitacora(Base):
    __tablename__ = 'bitacora'

    id_bitacora = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora = Column(Date, nullable=False)
    accion_realizada = Column(Text, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id_usuarios'), nullable=False)

    usuario = relationship("Usuarios", back_populates="bitacora")


class CierreContable(Base):
    __tablename__ = 'cierre_contable'

    id_cierre_contable = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(Text, nullable=False)
    fecha_contable_apertura = Column(Date, nullable=False)
    fecha_contable_cierre = Column(Date, nullable=False)

    asientos_contables = relationship("AsientosContables", back_populates="cierre")


class Comprobantes(Base):
    __tablename__ = 'comprobantes'
    
    id_comprobante = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha = Column(Date, nullable=False)
    archivo = Column(Text, nullable=False)
    tipo_comprobante = Column(Integer, ForeignKey('tipo_comprobante.id_tipo_comprobante'), nullable=False)

    tipo = relationship("TipoComprobante", back_populates="comprobantes")


class CuentasContables(Base):
    __tablename__ = 'cuentas_contables'

    id_cuenta_contable = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(VARCHAR(200), nullable=False)
    nombre_cuenta = Column(Text, nullable=False)
    nivel_cuenta = Column(Text, nullable=False)
    tipo_cuenta = Column(Text, nullable=False)
    saldo_normal = Column(Float, nullable=False)
    estado_cuenta = Column(Text, nullable=False)
    id_plan_cuenta = Column(Integer, ForeignKey('plan_cuentas.id_plan_cuentas'), nullable=False)

    plan_cuentas = relationship("PlanCuentas", back_populates="cuentas_contables")
    cuentas_principales = relationship("CuentasPrincipales", back_populates="cuenta_contable")
    asientos_contables_asientos = relationship("CuentasContablesAsientosContables", back_populates="cuenta_contable")


class CuentasContablesAsientosContables(Base):
    __tablename__ = 'cuentas_contables_asientos_contables'

    id_asiento_contable = Column(Integer, ForeignKey('asientos_contables.id_asiento_contable'), primary_key=True)
    id_cuenta_contable = Column(Integer, ForeignKey('cuentas_contables.id_cuenta_contable'), primary_key=True)
    tipo_saldo = Column(String(10), nullable=False)
    saldo = Column(Float, nullable=False)

    asiento_contable = relationship("AsientosContables", back_populates="cuentas")
    cuenta_contable = relationship("CuentasContables", back_populates="asientos_contables_asientos")

class CuentasPrincipales(Base):
    __tablename__ = 'cuentas_principales'

    id_cuentas_principales = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(VARCHAR(45), nullable=False)
    nombre_cuenta = Column(Text, nullable=False)
    nivel_cuenta = Column(Text, nullable=False)
    tipo_cuenta = Column(Text, nullable=False)
    id_cuenta_contable = Column(Integer, ForeignKey('cuentas_contables.id_cuenta_contable'), nullable=False)

    cuenta_contable = relationship("CuentasContables", back_populates="cuentas_principales")
    asientos_contables = relationship("AsientosContables", back_populates="cuentas_principales")


class Departamentos(Base):
    __tablename__ = 'departamentos'

    id_departamento = Column(Integer, primary_key=True, autoincrement=True)
    nombre_departamento = Column(Text, nullable=False)
    id_empresa = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)

    empresa = relationship("Empresas", back_populates="departamentos")
    registros_movimientos = relationship("RegistrosMovimientos", back_populates="departamento")


class Empresas(Base):
    __tablename__ = 'empresas'

    id_empresas = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    fecha_constitucion = Column(Date, nullable=False)
    rif = Column(VARCHAR(11), nullable=False)
    fecha_ejercicio_economico = Column(Date, nullable=False)
    actividad_economica = Column(Text, nullable=False)
    direccion = Column(Text, nullable=False)
    correo = Column(Text, nullable=False)

    departamentos = relationship("Departamentos", back_populates="empresa")
    plan_cuentas = relationship("PlanCuentas", back_populates="empresa")
    registros_movimientos = relationship("RegistrosMovimientos", back_populates="empresa")
    asientos_contables = relationship("AsientosContables", back_populates="empresa")


class MovimientosPlan(Base):
    __tablename__ = 'movimientos_plan'

    id_movimientos_plan = Column(Integer, primary_key=True, autoincrement=True)
    id_plan_cuentas = Column(Integer, ForeignKey('plan_cuentas.id_plan_cuentas'), nullable=False)
    id_registro = Column(Integer, ForeignKey('registros_movimientos.id_registros_movimientos'), nullable=False)

    plan_cuentas = relationship("PlanCuentas", back_populates="movimientos_plan")
    registro = relationship("RegistrosMovimientos", back_populates="movimientos_plan")


class MovimientosUsuarios(Base):
    __tablename__ = 'movimientos_usuarios'

    id_movimientos_usuarios = Column(Integer, primary_key=True, autoincrement=True)
    id_usuarios = Column(Integer, ForeignKey('usuarios.id_usuarios'), nullable=False)
    id_movimientos = Column(Integer, ForeignKey('registros_movimientos.id_registros_movimientos'), nullable=False)

    usuario = relationship("Usuarios", back_populates="movimientos_usuarios")
    registro = relationship("RegistrosMovimientos", back_populates="movimientos_usuarios")


class PlanCuentas(Base):
    __tablename__ = 'plan_cuentas'

    id_plan_cuentas = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(VARCHAR(200), nullable=False)
    descripcion_cuenta = Column(Text, nullable=False)
    id_empresas = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)

    empresa = relationship("Empresas", back_populates="plan_cuentas")
    cuentas_contables = relationship("CuentasContables", back_populates="plan_cuentas")
    movimientos_plan = relationship("MovimientosPlan", back_populates="plan_cuentas")


class RegistrosMovimientos(Base):
    __tablename__ = 'registros_movimientos'

    id_registros_movimientos = Column(Integer, primary_key=True, autoincrement=True)
    fecha_movimiento = Column(Date, nullable=False)
    id_empresas = Column(Integer, ForeignKey('empresas.id_empresas'), nullable=False)
    nro_control = Column(VARCHAR(200), nullable=False)
    nro_documentos = Column(VARCHAR(200), nullable=False)
    id_departamentos = Column(Integer, ForeignKey('departamentos.id_departamento'), nullable=False)

    empresa = relationship("Empresas", back_populates="registros_movimientos")
    departamento = relationship("Departamentos", back_populates="registros_movimientos")
    movimientos_plan = relationship("MovimientosPlan", back_populates="registro")
    movimientos_usuarios = relationship("MovimientosUsuarios", back_populates="registro")


class Reportes(Base):
    __tablename__ = 'reportes'

    id_reportes = Column(Integer, primary_key=True, autoincrement=True)
    tipo_reporte = Column(Text, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    nivel_detalle = Column(Text, nullable=False)
    formato = Column(Text, nullable=False)
    archivo = Column(Text, nullable=False)
    id_asiento_contable = Column(Integer, ForeignKey('asientos_contables.id_asiento_contable'), nullable=False)

    asiento_contable = relationship("AsientosContables", back_populates="reportes")


class TipoComprobante(Base):
    __tablename__ = 'tipo_comprobante'
    
    id_tipo_comprobante = Column(Integer, primary_key=True, autoincrement=True)
    nombre_comprobante = Column(Text, nullable=False)
    
    comprobantes = relationship("Comprobantes", back_populates="tipo")
    asientos = relationship("AsientosContables", back_populates="comprobante")


class Usuarios(Base):
    __tablename__ = 'usuarios'

    id_usuarios = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    correo = Column(VARCHAR(50), nullable=False)
    clave = Column(VARCHAR(20), nullable=False)

    bitacora = relationship("Bitacora", back_populates="usuario")
    movimientos_usuarios = relationship("MovimientosUsuarios", back_populates="usuario")