# Se recomienda configurar esta parte
usuario = 'root'
contrasena = 'JDPerez1005'
host = 'localhost'
base_datos = 'to_do_list'
puerto = 3306

# URL de conexión (se construye dinámicamente)
url_conexion = f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_datos}'
# URL para conectarse sin especificar la base de datos
url_sin_bd = f"mysql+pymysql://{usuario}:{contrasena}@{host}:{puerto}/"
# URL para conectarse con la base de datos
url_con_bd = f"mysql+pymysql://{usuario}:{contrasena}@{host}:{puerto}/{base_datos}"