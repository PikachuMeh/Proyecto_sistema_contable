from Proyecto_5to.python.main import app

"""
from models.unidad_estatal import accion,cargos,grupos,localidad,maestros,regiones,tbl_organismo,tbl_sedes,tbl_tiposede,usuarios
import bd.base as bd """


@app.get("/")
async def inicio():
    return "hola mundo!"

@app.get("/fetch")
async def fetch():
    dato = 1
    #dato = bd.session.query(usuarios).first()
        
    """returns 80s movie stars"""
    #logger.info("fetching movie stars to front end (Vue)")
    return {"usuarios": dato}

@app.get("/otro")
async def otro():
    dato = 1
    #dato = bd.session.query(maestros).first()
    return {"maestros": dato} 


