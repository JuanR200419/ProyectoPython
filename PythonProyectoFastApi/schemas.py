from pydantic import BaseModel

class ContactoRequestModel(BaseModel):
    nombre: str
    correo: str
    apellido: str
    direccion: str
    telefono: int

class ContactoResponseModel(ContactoRequestModel):
    id: int
