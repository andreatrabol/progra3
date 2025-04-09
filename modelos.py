# modelos.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class Personaje(Base):
    __tablename__ = "personajes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
   
class Mision(Base):
    __tablename__ = "misiones"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    

class MisionCola(Base):
    __tablename__ = "cola_misiones"
    id = Column(Integer, primary_key=True)
    personaje_id = Column(Integer, ForeignKey('personajes.id'))
    mision_id = Column(Integer, ForeignKey('misiones.id'))
    orden = Column(Integer)
