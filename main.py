from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uvicorn, os, json
from dotenv import load_dotenv
load_dotenv()
# Create a FastAPI instance
app = FastAPI()

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our declarative class
Base = declarative_base()

# Define the citas_medicas table model
class CitasMedicas(Base):
    __tablename__ = "citas_medicas"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String(50), unique=True)
    fecha = Column(DateTime)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# API endpoint to get fecha based on cedula
@app.get("/")
def get_fecha(cedula: str):
    db = SessionLocal()
    cita = db.query(CitasMedicas).filter(CitasMedicas.cedula == cedula).first()
    db.close()

    if cita:
        return {"fecha": cita.fecha}
    else:
        return {"fecha": None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT"))
