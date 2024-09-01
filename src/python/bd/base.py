from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
usuario = "root"
password = ""
ruta = "127.0.0.1"
puerto = "3306"
nombre_bd = "asap"

# Crear el motor de la base de datos
engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{ruta}:{puerto}/{nombre_bd}", pool_pre_ping=True)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()