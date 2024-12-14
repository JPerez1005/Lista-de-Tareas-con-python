from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine, text, inspect 
from sqlalchemy.orm import declarative_base
from datetime import datetime
from data.conexion import base_datos, url_sin_bd, url_con_bd
# from conexion import base_datos, engine, url_sin_bd, url_con_bd

# Crear la clase base para los modelos
Base = declarative_base()
# Crear la base de datos si no existe

# Definir la tabla Tarea
class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=False, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=True)

# Función para crear la base de datos si no existe
def crear_base_datos():
    try:
        # Conectar al servidor sin especificar la base de datos
        engine_sin_bd = create_engine(url_sin_bd)
        with engine_sin_bd.connect() as connection:
            # Usar text() para convertir la cadena SQL en un objeto ejecutable
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {base_datos}"))
            print(f"Base de datos '{base_datos}' creada o ya existía.")
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
        raise e

crear_base_datos()
engine = create_engine(url_con_bd)

def crear_tablas_si_no_existen(engine):
    inspector = inspect(engine)
    # Obtener las tablas existentes en la base de datos
    tablas_existentes = inspector.get_table_names()
    # Obtener las tablas definidas en tu modelo
    tablas_modelo = Base.metadata.tables.keys()

    # Verificar si alguna de las tablas definidas no existe
    tablas_a_crear = [tabla for tabla in tablas_modelo if tabla not in tablas_existentes]

    if tablas_a_crear:
        # Crear solo las tablas que no existen
        Base.metadata.create_all(engine, tables=[Base.metadata.tables[tabla] for tabla in tablas_a_crear])
        print(f"Tablas creadas: {', '.join(tablas_a_crear)}")
    else:
        print("Las tablas ya existen. No se crearon nuevas tablas.")

crear_tablas_si_no_existen(engine)

def eliminar_tablas(engine):
    # Eliminar todas las tablas definidas en el modelo (clases)
    Base.metadata.drop_all(engine)
    print("Tablas eliminadas con éxito.")
