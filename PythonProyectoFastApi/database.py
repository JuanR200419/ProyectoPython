from peewee import *
dbLite = SqliteDatabase('agenda.db')
class Contacto(Model):
    nombre = TextField()
    correo = TextField()
    apellido = TextField()
    direccion = TextField()
    telefono = IntegerField()
    class Meta:
        database = dbLite
        table_name = 'contactos'

dbLite.connect()
