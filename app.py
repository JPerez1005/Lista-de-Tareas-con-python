import streamlit as st
from datetime import datetime
from data.crudLite import agregar_tarea, obtener_tareas_filtradas, eliminar_tarea, actualizar_tarea
import pandas as pd

st.set_page_config(layout="centered")

# Variables de control de la aplicación
if 'editar_tarea_id' not in st.session_state:
    st.session_state.editar_tarea_id = None

if 'editar_tarea_datos' not in st.session_state:
    st.session_state.editar_tarea_datos = {}

def alternar_formulario():
    """Alternar la visibilidad del formulario"""
    st.session_state.editar_tarea_id = None  # Resetear la tarea en edición
    st.session_state.editar_tarea_datos = {}  # Limpiar datos de edición

def traspaso_de_tareas():
    st.sidebar.subheader("📂 Importar tareas")
    archivo = st.sidebar.file_uploader("Sube un archivo CSV o JSON", type=['csv', 'json'])

    if archivo is not None:
        if archivo.name.endswith('.csv'):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith('.json'):
            df = pd.read_json(archivo)
        
        st.sidebar.write("Vista previa del archivo importado:")
        st.sidebar.dataframe(df)

        if st.sidebar.button("Importar Tareas"):
            for _, fila in df.iterrows():
                # ⚠️ Convertir fecha_vencimiento de milisegundos a una fecha legible
                fecha_vencimiento_raw = fila.get('fecha_vencimiento', None)
                
                if fecha_vencimiento_raw is not None:
                    # Verificar si la fecha está en milisegundos y convertirla
                    if isinstance(fecha_vencimiento_raw, (int, float)) and fecha_vencimiento_raw > 1000000000000:  # Milisegundos
                        fecha_vencimiento = datetime.fromtimestamp(fecha_vencimiento_raw / 1000)  # Convertir a segundos
                    elif isinstance(fecha_vencimiento_raw, (int, float)):  # Segundos (Unix)
                        fecha_vencimiento = datetime.fromtimestamp(fecha_vencimiento_raw)
                    else:
                        fecha_vencimiento = fecha_vencimiento_raw  # Puede estar en formato de texto
                else:
                    fecha_vencimiento = None

                agregar_tarea(
                    titulo=fila['titulo'], 
                    descripcion=fila.get('descripcion', None), 
                    estado=fila.get('estado', False), 
                    fecha_vencimiento=fecha_vencimiento  # Fecha convertida
                )

    # 2️⃣ **Exportar tareas a CSV o JSON**
    st.sidebar.subheader("💾 Exportar tareas")
    tareas = obtener_tareas_filtradas()
    df_exportar = pd.DataFrame([{
        'id': t.id,
        'titulo': t.titulo,
        'descripcion': t.descripcion,
        'estado': t.estado,
        'fecha_creacion': t.fecha_creacion,
        'fecha_vencimiento': t.fecha_vencimiento
    } for t in tareas])

    # Exportar a CSV
    csv = df_exportar.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='tareas.csv',
        mime='text/csv'
    )

    # Exportar a JSON
    json = df_exportar.to_json(orient='records')
    st.sidebar.download_button(
        label="Descargar JSON",
        data=json, 
        file_name='tareas.json',
        mime='application/json'
    )

def formulario_de_insercion_y_modificacion_de_tareas():

    st.header("Agregar Tarea")

    st.subheader("Nueva Tarea" if st.session_state.editar_tarea_id is None else "Modificar Tarea")
    
    # Prellenar los campos si se está editando una tarea
    titulo = st.text_input("Título de la tarea", value=st.session_state.editar_tarea_datos.get('titulo', ''))
    descripcion = st.text_area("Descripción de la tarea", value=st.session_state.editar_tarea_datos.get('descripcion', ''))
    
    col1, col2 = st.columns([1, 1])

    with col2:
        # Mostrar el campo "Estado" solo si se está modificando la tarea
        if st.session_state.editar_tarea_id is not None:
            estado = st.radio("Estado", ["Pendiente", "Completada"], 
                            index=0 if not st.session_state.editar_tarea_datos.get('estado', False) else 1, 
                            horizontal=True)
            estado = estado == "Completada"  # Convertir a booleano
        else:
            estado = False

    with col1:
        fecha_vencimiento = st.date_input("Fecha de Vencimiento", 
                                        value=st.session_state.editar_tarea_datos.get('fecha_vencimiento', datetime.today()))

    if st.session_state.editar_tarea_id is None:
        if st.button("Agregar Tarea"):
            if titulo:
                agregar_tarea(titulo, descripcion, estado ,fecha_vencimiento)  # Estado se pasa como False
                st.success(f"Tarea '{titulo}' agregada con éxito.")
                st.session_state.mostrar_formulario = False  # Ocultar formulario después de agregar la tarea
            else:
                st.warning("Por favor, ingresa el título de la tarea.")
    else:
        if st.button("Actualizar Tarea"):
            actualizar_tarea(st.session_state.editar_tarea_id, titulo, descripcion, estado, fecha_vencimiento)
            st.success(f"Tarea '{titulo}' actualizada.")
            st.session_state.mostrar_formulario = False  # Ocultar formulario después de actualizar
            st.session_state.editar_tarea_id = None  # Resetear ID de edición

def lista_tareas():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Lista de Tareas")

    with col2:
        busqueda = st.text_input("Buscar tareas (por título o descripción)", "")

    st.markdown("<br>", unsafe_allow_html=True)

    # Verificar si hay algo en el campo de búsqueda
    tareas = obtener_tareas_filtradas(busqueda)

    for tarea in tareas:
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.write(f"""
                **{tarea.titulo}**  
                **Descripción:** {tarea.descripcion if tarea.descripcion else 'Sin descripción'}  
                **Estado:** {'Completada' if tarea.estado else 'Pendiente'}  
                **Fecha de Creación:** {tarea.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}  
                **Fecha de Vencimiento:** {tarea.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if tarea.fecha_vencimiento else 'No establecida'}
            """)
        with col2:
            if st.button(f"✏️ Modificar", key=f"mod_{tarea.id}"):
                st.session_state.mostrar_formulario = True
                st.session_state.editar_tarea_id = tarea.id
                st.session_state.editar_tarea_datos = {
                    'titulo': tarea.titulo,
                    'descripcion': tarea.descripcion,
                    'estado': tarea.estado,
                    'fecha_vencimiento': tarea.fecha_vencimiento
                }
                st.success(f"cambie de pestaña para modificar.")
        with col3:
            if st.button(f"🗑️ Eliminar", key=f"del_{tarea.id}"):
                eliminar_tarea(tarea.id)
                st.success(f"Tarea '{tarea.titulo}' eliminada.")

def paginacion():
    tab1, tab2 = st.tabs(['Agregar o modificar tareas', 'Ver tareas']); 
    with tab1: formulario_de_insercion_y_modificacion_de_tareas()
    with tab2: lista_tareas()

traspaso_de_tareas()

paginacion()