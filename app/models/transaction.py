from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Enum, Date
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, timezone
import enum

class TransactionType(str, enum.Enum):
    venta = "venta"
    abono = "abono"

class TransactionStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    terminado = "terminado"
    incompleta = "incompleta"

class CuentasRecaudo(Base):
    __tablename__ = "cuentas_recaudo"

    id = Column(Integer, primary_key=True, index=True)

class Traveler(Base):
    __tablename__ = "travelers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    dni = Column(String, nullable=False)
    date_birth = Column(Date, nullable=False)
    phone = Column(String, nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))

    # Relationship with Transaction
    transaction = relationship("Transaction", back_populates="travelers")
    documentos = relationship("Documentos", back_populates="traveler")

class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    evidence_file = Column(String, nullable=False)
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    amount = Column(Float, nullable=False)

    transaction = relationship("Transaction", back_populates="evidences")

class Itinerario(Base):
    __tablename__ = "itinerario"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    aerolinea = Column(String, nullable=False)
    ruta = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)
    hora_salida = Column(String, nullable=False)
    hora_llegada = Column(String, nullable=False)

    transaction = relationship("Transaction", back_populates="itinerario")

class TravelInfo(Base):
    __tablename__ = "travel_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    hotel = Column(String, nullable=True)
    noches = Column(Integer, nullable=True)
    incluye = Column(ARRAY(String), nullable=True)
    no_incluye = Column(ARRAY(String), nullable=True)
    alimentacion = Column(String, nullable=True)
    acomodacion = Column(String, nullable=True)
    direccion_hotel = Column(String, nullable=True)
    pais_destino = Column(String, nullable=True)
    ciudad_destino = Column(String, nullable=True)

 

    transaction = relationship("Transaction", back_populates="travel_info")

class Documentos(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    viajero_id = Column(Integer, ForeignKey("travelers.id"), nullable=False)
    document_url = Column(String, nullable=False)
    tipo_documento = Column(String, nullable=False)

    transaction = relationship("Transaction", back_populates="documentos")
    traveler = relationship("Traveler", back_populates="documentos")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    client_phone = Column(String, nullable=False)
    client_dni = Column(String, nullable=False)
    client_address = Column(String, nullable=False)
    package = Column(String, nullable=False)
    quoted_flight = Column(String, nullable=False)
    agency_cost = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.pending)
    seller_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    receipt = Column(String, nullable=True)
    number_of_travelers = Column(Integer, nullable=False)

    itinerario = relationship("Itinerario", back_populates="transaction")
    seller = relationship("User", back_populates="transactions")
    travelers = relationship("Traveler", back_populates="transaction")
    evidences = relationship("Evidence", back_populates="transaction")
    travel_info = relationship("TravelInfo", back_populates="transaction")
    documentos = relationship("Documentos", back_populates="transaction")
