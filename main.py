# main.py

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from modelos import Base, Personaje, Mision, MisionCola

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ MODELOS Pydantic para entrada de datos desde Swagger UI
class PersonajeCreate(BaseModel):
    nombre: str

class MisionCreate(BaseModel):
    descripcion: str
    

# ✅ Función para obtener la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Crear personaje
@app.post("/personajes")
def crear_personaje(datos:str, db: Session = Depends(get_db)):
    personaje = Personaje(nombre=datos)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return personaje

# ✅ Crear misión
@app.post("/misiones")
def crear_mision(datos: MisionCreate, db: Session = Depends(get_db)):
    mision = Mision(descripcion=datos.descripcion)
    db.add(mision)
    db.commit()
    db.refresh(mision)
    return mision

# ✅ Aceptar misión (encolar)
@app.post("/personajes/{id}/misiones/{mision_id}")
def aceptar_mision(id: int, mision_id: int, db: Session = Depends(get_db)):
    total = db.query(MisionCola).filter(MisionCola.personaje_id == id).count()
    nueva = MisionCola(personaje_id=id, mision_id=mision_id, orden=total)
    db.add(nueva)
    db.commit()
    return {"mensaje": "Misión agregada a la cola"}

# ✅ Completar misión (desencolar + sumar XP)
@app.post("/personajes/{id}/completar")
def completar_mision(id: int, db: Session = Depends(get_db)):
    primera = db.query(MisionCola).filter(MisionCola.personaje_id == id).order_by(MisionCola.orden).first()
    if not primera:
        return {"mensaje": "No hay misiones"}

    mision = db.query(Mision).filter(Mision.id == primera.mision_id).first()
    personaje = db.query(Personaje).filter(Personaje.id == id).first()
    

    db.delete(primera)
    db.commit()
    return {"mensaje": f"Misión completada, ganaste "}

# ✅ Ver misiones en orden FIFO
@app.get("/personajes/{id}/misiones")
def ver_misiones(id: int, db: Session = Depends(get_db)):
    misiones = db.query(MisionCola).filter(MisionCola.personaje_id == id).order_by(MisionCola.orden).all()
    resultado = []
    for item in misiones:
        mision = db.query(Mision).filter(Mision.id == item.mision_id).first()
        resultado.append({"id": mision.id, "descripcion": mision.descripcion})
    return resultado 
