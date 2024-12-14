from data.models import Tarea
from datetime import datetime
from sqlalchemy.orm import  sessionmaker
from data.models import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una sesión
session = SessionLocal()

def agregar_tarea(titulo, descripcion=None, estado=False, fecha_vencimiento=None, fecha_creacion=None):
    with SessionLocal() as session:
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
    if busqueda:
        tareas = session.query(Tarea).filter(
            (Tarea.titulo.ilike(f"%{busqueda}%")) | 
            (Tarea.descripcion.ilike(f"%{busqueda}%"))
        ).all()
    else:
        tareas = session.query(Tarea).all()
    session.close()
    return tareas

def eliminar_tarea(id_tarea):
    tarea = session.query(Tarea).filter(Tarea.id == id_tarea).first()
    if tarea:
        session.delete(tarea)
        session.commit()
    session.close()

def actualizar_tarea(id_tarea, nuevo_titulo=None, nueva_descripcion=None, nuevo_estado=None, nueva_fecha_vencimiento=None):
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
    session.close()