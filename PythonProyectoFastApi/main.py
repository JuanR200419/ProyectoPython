from  fastapi import FastAPI
from database import dbLite as connection
from database import *
from schemas import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
app= FastAPI(title='Agenda De Contactos',description='',version='1.0')
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([Contacto])

@app.on_event('shutdown')
def shutdown():
    if  not connection.is_closed():
        connection.close()
    

""" POST = agregar 
GET  = obtener
PUT = actualizar
Delete = eliminar
"""
# Funcion agregar
@app.post('/api/v1/contacto/agregar',tags=["Contactos"])
async def agregar_contacto(contacto_request:ContactoRequestModel):
    cont = Contacto().create(
        nombre = contacto_request.nombre,
        correo = contacto_request.correo,
        apellido = contacto_request.apellido,
        direccion = contacto_request.direccion,
        telefono = contacto_request.telefono
        ) 
    return (contacto_request)

# Funcion Eliminar
@app.delete('/api/v1/eliminar/{contacto_id}')
async def delete_contacto(contacto_id):
    cont = Contacto.select().where(Contacto.
            id == contacto_id).first()
    if cont:
        cont.delete_instance()
        return True, "Contacto eliminado con éxito"
    else:
        raise HTTPException(status_code=404, detail="El contacto no se encuentra")
    
# Funcion para obtener toda la lista
def cargarContactos():
    contactos = []
    for cont in Contacto.select().dicts():
        contactos.append(cont)
    return contactos
# Funcion Lista
@app.get('/api/v1/contactos')
def lista_contactos():
    tmp = cargarContactos()
    return tmp

