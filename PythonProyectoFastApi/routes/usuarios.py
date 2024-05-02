from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import database
from main import Usuario

router = APIRouter()

class UsuarioIn(BaseModel):
    nombres_usuario: str
    apellido_usuario: str
    correo_electronico: str
    contrasena: str
    direccion: str

class UsuarioOut(UsuarioIn):
    id_usuario: int

@router.post("/", response_model=UsuarioOut)
async def create_user(usuario: UsuarioIn):
    query = usuario.insert().returning(usuario)
    user = await database.execute(query)
    return user

@router.get("/{usuario_id}", response_model=UsuarioOut)
async def read_user(usuario_id: int):
    query = Usuario.select().where(Usuario.id_usuario == usuario_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{usuario_id}", response_model=UsuarioOut)
async def update_user(usuario_id: int, usuario: UsuarioIn):
    query = (
        usuario.update()
        .where(usuario.c.id_usuario == usuario_id)
        .returning(usuario)
    )
    updated_user = await database.execute(query)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user

@router.delete("/{usuario_id}")
async def delete_user(usuario_id: int):
    query = Usuario.delete().where(Usuario.id_usuario == usuario_id)
    deleted_user = await database.execute(query)
    if deleted_user == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}
