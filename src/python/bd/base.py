import configparser
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


usuario = "root"
password = ""
ruta = "127.0.0.1"
puerto = "3306"

nombre_bd = "login"

engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{ruta}:{puerto}/{nombre_bd}")

Session = sessionmaker(bind=engine)
session = Session()

session.autobegin = True
session.autoflush = True

Base = declarative_base()
