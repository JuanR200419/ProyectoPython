from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import database
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
    query = Contacto.delete().where(Contacto.c.id_contacto == contacto_id)
    deleted_contacto = await database.execute(query)
    if deleted_contacto == 0:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return {"message": "Contacto eliminado exitosamente"}


router = APIRouter()

class CategoriaIn(BaseModel):
    nombre_categoria: str

class CategoriaOut(CategoriaIn):
    id_categoria: int

@router.post("/", response_model=CategoriaOut)
async def create_categoria(categoria: CategoriaIn):
    query = Categoria.insert().returning(Categoria)
    new_categoria = await database.execute(query)
    return new_categoria

@router.get("/{categoria_id}", response_model=CategoriaOut)
async def read_categoria(categoria_id: int):
    query = Categoria.select().where(Categoria.id_categoria == categoria_id)
    categoria = await database.fetch_one(query)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaOut)
async def update_categoria(categoria_id: int, categoria: CategoriaIn):
    query = (
        Categoria.update()
        .where(Categoria.id_categoria == categoria_id)
        .returning(Categoria)
    )
    updated_categoria = await database.execute(query)
    if updated_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return updated_categoria

@router.delete("/{categoria_id}")
async def delete_categoria(categoria_id: int):
    query = Categoria.delete().where(Categoria.id_categoria == categoria_id)
    deleted_categoria = await database.execute(query)
    if deleted_categoria == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada exitosamente"}
