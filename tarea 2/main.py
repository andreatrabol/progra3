from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from modelo import crear_base, SessionLocal
from crud import crear_vuelo, obtener_vuelos, borrar_vuelo
from modelo import Vuelo

app = FastAPI()

crear_base()

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/vuelos/")
def agregar_vuelo(nombre: str, origen: str, destino: str, prioridad: str, db: Session = Depends(get_db)):
    """
    Añade un vuelo al final (normal) o al frente (emergencia).
    """
    vuelo = crear_vuelo(db, nombre, origen, destino, prioridad)
    return {"mensaje": "Vuelo agregado", "vuelo": vuelo}


@app.get("/vuelos/total")
def total_vuelos(db: Session = Depends(get_db)):
    """
    Retorna el número total de vuelos en cola.
    """
    vuelos = obtener_vuelos(db)
    return {"total": len(vuelos)}


@app.get("/vuelos/proximo")
def vuelo_proximo(db: Session = Depends(get_db)):
    """
    Retorna el primer vuelo sin remover.
    """
    vuelos = obtener_vuelos(db)
    if vuelos:
        return vuelos[0]
    raise HTTPException(status_code=404, detail="No hay vuelos")


@app.get("/vuelos/ultimo")
def vuelo_ultimo(db: Session = Depends(get_db)):
    """
    Retorna el último vuelo sin remover.
    """
    vuelos = obtener_vuelos(db)
    if vuelos:
        return vuelos[-1]
    raise HTTPException(status_code=404, detail="No hay vuelos")


@app.post("/vuelos/insertar")
def insertar_vuelo(posicion: int, nombre: str, origen: str, destino: str, prioridad: str, db: Session = Depends(get_db)):
    """
    Inserta un vuelo en una posición específica.
    """
    vuelos = obtener_vuelos(db)
    if posicion < 0 or posicion > len(vuelos):
        raise HTTPException(status_code=400, detail="Posición inválida")

    nuevo = crear_vuelo(db, nombre, origen, destino, prioridad)

    # Simulamos inserción por posición (realmente solo ordenamos)
    vuelos.insert(posicion, nuevo)

    # Eliminar todos y volver a insertar (forma simple)
    db.query(Vuelo).delete()
    db.commit()
    for v in vuelos:
        crear_vuelo(db, v.nombre, v.origen, v.destino, v.prioridad)

    return {"mensaje": "Vuelo insertado", "nuevo_orden": obtener_vuelos(db)}


@app.delete("/vuelos/extraer")
def extraer_vuelo(posicion: int, db: Session = Depends(get_db)):
    """
    Remueve un vuelo de una posición dada.
    """
    vuelos = obtener_vuelos(db)
    if posicion < 0 or posicion >= len(vuelos):
        raise HTTPException(status_code=400, detail="Posición inválida")

    vuelo = vuelos[posicion]
    borrar_vuelo(db, vuelo.id)
    return {"mensaje": f"Vuelo '{vuelo.nombre}' eliminado", "restantes": obtener_vuelos(db)}


@app.get("/vuelos/lista")
def listar_vuelos(db: Session = Depends(get_db)):
    """
    Lista todos los vuelos en orden actual.
    """
    return obtener_vuelos(db)


@app.patch("/vuelos/reordenar")
def reordenar_vuelos(nuevo_orden: list[int], db: Session = Depends(get_db)):
    """
    Reordena manualmente la cola (por ejemplo: por retrasos).
    nuevo_orden: lista de IDs de vuelos en el nuevo orden deseado
    """
    vuelos = {vuelo.id: vuelo for vuelo in obtener_vuelos(db)}
    nuevos_vuelos = []

    for id_ in nuevo_orden:
        if id_ not in vuelos:
            raise HTTPException(status_code=400, detail=f"ID {id_} inválido")
        nuevos_vuelos.append(vuelos[id_])

    # Eliminar todos y volver a insertar en nuevo orden
    db.query(Vuelo).delete()
    db.commit()
    for v in nuevos_vuelos:
        crear_vuelo(db, v.nombre, v.origen, v.destino, v.prioridad)

    return {"mensaje": "Vuelos reordenados", "nuevo_orden": obtener_vuelos(db)}
