import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


# URL de conexión SQLite (se crea un archivo .db local si no existe)
url_conexion = "sqlite:///to_do_list.db"

# Crea la base de datos si no existe
if not os.path.exists("to_do_list.db"):
    print("Base de datos no encontrada, creando base de datos...")
    engine = create_engine(url_conexion)
    Base = declarative_base()
else:
    engine = create_engine(url_conexion)

