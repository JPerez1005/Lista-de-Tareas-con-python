from data.modelsLite import Tarea
from sqlalchemy.orm import sessionmaker
from data.conexionLite import engine
from datetime import datetime

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

if session:
    print("Session iniciada")

def agregar_tarea(titulo, descripcion=None, estado=False, fecha_vencimiento=None, fecha_creacion=None):
    with Session() as session:
        nueva_tarea = Tarea(
            titulo=titulo, 
            descripcion=descripcion, 
            estado=estado, 
            fecha_vencimiento=fecha_vencimiento,
            fecha_creacion=fecha_creacion or datetime.utcnow()
        )
        session.add(nueva_tarea)
        session.commit()

def obtener_tareas_filtradas(busqueda=""):
    with Session() as session:
        if busqueda:
            tareas = session.query(Tarea).filter(
                (Tarea.titulo.ilike(f"%{busqueda}%")) | 
                (Tarea.descripcion.ilike(f"%{busqueda}%"))
            ).all()
        else:
            tareas = session.query(Tarea).all()
        return tareas

def eliminar_tarea(id_tarea):
    with Session() as session:
        tarea = session.query(Tarea).filter(Tarea.id == id_tarea).first()
        if tarea:
            session.delete(tarea)
            session.commit()

def actualizar_tarea(id_tarea, nuevo_titulo=None, nueva_descripcion=None, nuevo_estado=None, nueva_fecha_vencimiento=None):
    with Session() as session:
        tarea = session.query(Tarea).filter(Tarea.id == id_tarea).first()
        if tarea:
            if nuevo_titulo:
                tarea.titulo = nuevo_titulo
            if nueva_descripcion:
                tarea.descripcion = nueva_descripcion
            if nuevo_estado is not None:
                tarea.estado = nuevo_estado
            if nueva_fecha_vencimiento:
                tarea.fecha_vencimiento = nueva_fecha_vencimiento
            session.commit()
