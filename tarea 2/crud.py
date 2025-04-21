from modelo import Vuelo

def crear_vuelo(db, nombre, origen, destino, prioridad):
    vuelo = Vuelo(nombre=nombre, origen=origen, destino=destino, prioridad=prioridad)
    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)
    return vuelo

def obtener_vuelos(db):
    return db.query(Vuelo).all()

def borrar_vuelo(db, vuelo_id):
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if vuelo:
        db.delete(vuelo)
        db.commit()
        return {"mensaje": "Vuelo eliminado"}
    return {"error": "Vuelo no encontrado"}
