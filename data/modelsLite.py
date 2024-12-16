from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from data.conexionLite import engine
# from conexionLite import engine

# Crear la clase base para los modelos
Base = declarative_base()

# Crear la clase de sesión vinculada al engine
Session = sessionmaker(bind=engine)

class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=False, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=True)
    print("tabla de tareas creada")

# Crear las tablas si no existen
Base.metadata.create_all(engine)

def eliminar_tabla_tareas():
    # Eliminar la tabla `tareas` completamente
    Base.metadata.drop_all(engine, tables=[Tarea.__table__])
    print("Tabla de tareas eliminada")

# eliminar_tabla_tareas()