from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from routes import usuarios, categorias, contactos
from routes.usuarios import router, UsuarioIn, UsuarioOut
from fastapi import FastAPI, HTTPException
app = FastAPI()
app.include_router(usuarios.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(categorias.router, prefix="/categorias", tags=["categorias"])
app.include_router(contactos.router, prefix="/contactos", tags=["contactos"])

# Paso 1: Configurar la conexión a la base de datos
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

# Paso 2: Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Paso 3: Definir la base declarativa
Base = declarative_base()

# Paso 4: Definir los modelos de base de datos
class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombres_usuario = Column(String)
    apellido_usuario = Column(String)
    correo_electronico = Column(String)
    contrasena = Column(String)
    direccion = Column(String)

class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String)

class CategoriaPorContacto(Base):
    __tablename__ = "categoria_por_contacto"

    id_categoria = Column(Integer, ForeignKey("categoria.id_categoria"), primary_key=True)
    id_contacto = Column(Integer, ForeignKey("contacto.id_contacto"), primary_key=True)

class TelefonosPorContacto(Base):
    __tablename__ = "telefonos_por_contacto"

    id_telefono = Column(Integer, primary_key=True, index=True)
    id_contacto = Column(Integer, ForeignKey("contacto.id_contacto"))
    numero_telefono = Column(String)

class Contacto(Base):
    __tablename__ = "contacto"

    id_contacto = Column(Integer, primary_key=True, index=True)
    id_favorito = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_categoria = Column(Integer, ForeignKey("categoria.id_categoria"))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    nombre_contacto = Column(String)
    apellido_contacto = Column(String)
    correo_electronico = Column(String)
    direccion = Column(String)

    usuario = relationship("Usuario", back_populates="contactos")
    categoria = relationship("Categoria", back_populates="contactos")

# Paso 5: Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Paso 6: Iniciar la aplicación FastAPI
app = FastAPI()

# Paso 7: Conectar y desconectar la base de datos al iniciar y cerrar la aplicación
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Paso 8: Definir las rutas y operaciones CRUD utilizando los modelos
# (Esto lo haremos después)
## add usuario -------------------------------------------------------------------------------------------------
@router.post("/usuarios/", response_model=UsuarioOut)
async def create_user(usuario: UsuarioIn):
    query = Usuario.insert().returning(Usuario)
    user = await database.execute(query)
    return user
# buscar usuario
@router.get("/usuarios/{usuario_id}", response_model=UsuarioOut)
async def read_user(usuario_id: int):
    query = Usuario.select().where(Usuario.id_usuario == usuario_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
# actualizar usuario
@router.put("/usuarios/{usuario_id}", response_model=UsuarioOut)
async def update_user(usuario_id: int, usuario: UsuarioIn):
    query = (
        Usuario.update()
        .where(Usuario.id_usuario == usuario_id)
        .returning(Usuario)
    )
    updated_user = await database.execute(query)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated_user
# borrarUsuario
@router.delete("/usuarios/{usuario_id}")
async def delete_user(usuario_id: int):
    query = Usuario.delete().where(Usuario.id_usuario == usuario_id)
    deleted_user = await database.execute(query)
    if deleted_user == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

# Crear categoría----------------------------------------------------------------------------------------------------------------
@router.post("/categorias/", response_model=Categoria)
async def create_categoria(categoria: Categoria):
    query = Categoria.insert().values(nombre_categoria=categoria.nombre_categoria)
    categoria_id = await database.execute(query)
    return {**categoria.dict(), "id_categoria": categoria_id}

# Leer categoría por ID
@router.get("/categorias/{categoria_id}", response_model=Categoria)
async def read_categoria(categoria_id: int):
    query = Categoria.select([Categoria]).where(Categoria.id_categoria == categoria_id)
    categoria = await database.fetch_one(query)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# Actualizar categoría
@router.put("/categorias/{categoria_id}", response_model=Categoria)
async def update_categoria(categoria_id: int, categoria: Categoria):
    query = (
        Categoria.update()
        .where(Categoria.id_categoria == categoria_id)
        .values(nombre_categoria=categoria.nombre_categoria)
    )
    await database.execute(query)
    return {**categoria.dict(), "id_categoria": categoria_id}

# Eliminar categoría
@router.delete("/categorias/{categoria_id}")
async def delete_categoria(categoria_id: int):
    query = Categoria.delete().where(Categoria.id_categoria == categoria_id)
    deleted_rows = await database.execute(query)
    if not deleted_rows:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"message": "Categoría eliminada exitosamente"}
#-----------------------------------------------------------------------------------------------------------------------------------
# Crear contacto
@router.post("/contactos/", response_model=Contacto)
async def create_contacto(contacto: Contacto):
    query = Contacto.insert().values(
        id_favorito=contacto.id_favorito,
        id_categoria=contacto.id_categoria,
        id_usuario=contacto.id_usuario,
        nombre_contacto=contacto.nombre_contacto,
        apellido_contacto=contacto.apellido_contacto,
        correo_electronico=contacto.correo_electronico,
        direccion=contacto.direccion
    )
    contacto_id = await database.execute(query)
    return {**contacto.dict(), "id_contacto": contacto_id}

# Leer contacto por ID
@router.get("/contactos/{contacto_id}", response_model=Contacto)
async def read_contacto(contacto_id: int):
    query = Contacto.select([Contacto]).where(Contacto.id_contacto == contacto_id)
    contacto = await database.fetch_one(query)
    if contacto is None:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto

# Actualizar contacto
@router.put("/contactos/{contacto_id}", response_model=Contacto)
async def update_contacto(contacto_id: int, contacto: Contacto):
    query = (
        Contacto.update()
        .where(Contacto.id_contacto == contacto_id)
        .values(
            id_favorito=contacto.id_favorito,
            id_categoria=contacto.id_categoria,
            id_usuario=contacto.id_usuario,
            nombre_contacto=contacto.nombre_contacto,
            apellido_contacto=contacto.apellido_contacto,
            correo_electronico=contacto.correo_electronico,
            direccion=contacto.direccion
        )
    )
    await database.execute(query)
    return {**contacto.dict(), "id_contacto": contacto_id}

# Eliminar contacto
@router.delete("/contactos/{contacto_id}")
async def delete_contacto(contacto_id: int):
    query = Contacto.delete().where(Contacto.id_contacto == contacto_id)
    deleted_rows = await database.execute(query)
    if not deleted_rows:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return {"message": "Contacto eliminado exitosamente"}
