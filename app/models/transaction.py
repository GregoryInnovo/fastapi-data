
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime, timezone

class Traveler(Base):
    __tablename__ = "travelers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    dni = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=False)
    dni_image = Column(String, nullable=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))

    # Relationship with Transaction
    transaction = relationship("Transaction", back_populates="travelers")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    client_phone = Column(String, nullable=False)
    client_dni = Column(String, nullable=False)
    client_address = Column(String, nullable=False)
    invoice_image = Column(String, nullable=True)
    id_image = Column(String, nullable=True)
    package = Column(String, nullable=False)
    quoted_flight = Column(String, nullable=False)
    agency_cost = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # venta, abono
    status = Column(String, default="pendiente") # pendiendte ,completado , rechazado 
    seller_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    receipt = Column(String, nullable=True)
    number_of_travelers = Column(Integer, nullable=False)

    seller = relationship("User", back_populates="transactions")
    travelers = relationship("Traveler", back_populates="transaction")
