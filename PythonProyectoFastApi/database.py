from peewee import *

# Conexión a la base de datos SQLite
DATABASE_NAME = 'agenda.db'
dbLite = SqliteDatabase(DATABASE_NAME)

# Definición de modelos
class BaseModel(Model):
    class Meta:
        database = dbLite

class Contacto(BaseModel):
    nombre = TextField()
    correo = TextField()
    apellido = TextField()
    direccion = TextField()
    telefono = IntegerField()

class Usuario(BaseModel):
    nombre_usuario = TextField()
    apellido_usuario = TextField()
    correo_electronico = TextField()
    contrasena = TextField()
    direccion = TextField()

# Conectar a la base de datos
def conectar_bd():
    dbLite.connect()

# Desconectar de la base de datos
def desconectar_bd():
    if not dbLite.is_closed():
        dbLite.close()

# Crear tablas si no existen
def crear_tablas():
    with dbLite:
        dbLite.create_tables([Contacto, Usuario])

# Operaciones CRUD para Contacto
def crear_contacto(nombre, correo, apellido, direccion, telefono):
    with dbLite.atomic():
        return Contacto.create(nombre=nombre, correo=correo, apellido=apellido,
                                direccion=direccion, telefono=telefono)

def obtener_contacto_por_id(id_contacto):
    return Contacto.get_or_none(Contacto.id == id_contacto)

def actualizar_contacto(contacto, **actualizaciones):
    with dbLite.atomic():
        for campo, valor in actualizaciones.items():
            setattr(contacto, campo, valor)
        contacto.save()

def eliminar_contacto(contacto):
    with dbLite.atomic():
        contacto.delete_instance()

# Operaciones CRUD para Usuario
def crear_usuario(nombre_usuario, apellido_usuario, correo_electronico, contrasena, direccion):
    with dbLite.atomic():
        return Usuario.create(nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario,
                              correo_electronico=correo_electronico, contrasena=contrasena,
                              direccion=direccion)

def obtener_usuario_por_id(id_usuario):
    return Usuario.get_or_none(Usuario.id == id_usuario)

def actualizar_usuario(usuario, **actualizaciones):
    with dbLite.atomic():
        for campo, valor in actualizaciones.items():
            setattr(usuario, campo, valor)
        usuario.save()

def eliminar_usuario(usuario):
    with dbLite.atomic():
        usuario.delete_instance()
