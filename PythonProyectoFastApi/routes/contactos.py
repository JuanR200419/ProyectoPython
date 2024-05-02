from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import database
from main import  Contacto,Categoria,Usuario

router = APIRouter()

class ContactoIn(BaseModel):
    nombre_contacto: str
    apellido_contacto: str
    correo_electronico: str
    direccion: str

class ContactoOut(ContactoIn):
    id_contacto: int

@router.post("/", response_model=ContactoOut)
async def create_contacto(contacto: ContactoIn):
    query = Contacto.insert().returning(Contacto)
    new_contacto = await database.execute(query)
    return new_contacto

@router.get("/{contacto_id}", response_model=ContactoOut)
async def read_contacto(contacto_id: int):
    query = Contacto.select().where(Contacto.id_contacto == contacto_id)
    contacto = await database.fetch_one(query)
    if contacto is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto

@router.put("/{contacto_id}", response_model=ContactoOut)
async def update_contacto(contacto_id: int, contacto: ContactoIn):
    query = (
        Contacto.update()
        .where(Contacto.id_contacto == contacto_id)
        .returning(Contacto)
    )
    updated_contacto = await database.execute(query)
    if updated_contacto is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return updated_contacto

@router.delete("/{contacto_id}")
async def delete_contacto(contacto_id: int):
    query = Contacto.delete().where(Contacto.id_contacto == contacto_id)
    deleted_contacto = await database.execute(query)
    if deleted_contacto == 0:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return {"message": "Contacto eliminado exitosamente"}
