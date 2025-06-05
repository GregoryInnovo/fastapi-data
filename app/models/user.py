from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.db.database import Base
from passlib.context import CryptContext

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # vendedor, encargado, administrador
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Agregar campo de contraseña
    phone_number=Column(String, nullable=True)
    # Relación con transacciones
    transactions = relationship("Transaction", back_populates="seller")

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
