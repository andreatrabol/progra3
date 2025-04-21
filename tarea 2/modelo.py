from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Modelo de vuelo (tabla)
class Vuelo(Base):
    __tablename__ = "vuelos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    origen = Column(String)
    destino = Column(String)
    prioridad = Column(String)  # ejemplo: emergencia, normal, etc

# Motor y sesión de la base de datos
DATABASE_URL = "sqlite:///./vuelos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def crear_base():
    Base.metadata.create_all(bind=engine)
