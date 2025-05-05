from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User, hash_password
from app.models.transaction import Transaction, Traveler
from app.models.event import Event
from datetime import datetime

# Crear una sesión de base de datos
db: Session = SessionLocal()

# Insertar usuarios
user1 = User(name="Sara", role="vendedor", email="sara@example.com", password=hash_password("password123"))
user2 = User(name="Scott", role="encargado", email="scott@example.com", password=hash_password("password123"))
db.add(user1)
db.add(user2)

# Insertar transacciones
transaction1 = Transaction(
    client_name="Cliente 1",
    client_email="cliente1@example.com",
    client_phone="123456789",
    client_dni="12345678",
    client_address="Calle Falsa 123",
    package="Tour",
    quoted_flight="Vuelo 123",
    agency_cost=100.0,
    amount=150.0,
    transaction_type="venta",
    seller_id=1,
    number_of_travelers=2
)
db.add(transaction1)

# Insertar viajeros
traveler1 = Traveler(name="Sara Dhamer", dni="1233748", age=12, phone="17273", dni_image="skueu27373.com", transaction_id=1)
traveler2 = Traveler(name="Scott Dhamer", dni="1233748", age=12, phone="17273", dni_image="skueu27373.com", transaction_id=1)
db.add(traveler1)
db.add(traveler2)

# Insertar eventos
event1 = Event(description="Evento de prueba", date=datetime.now())
db.add(event1)

# Confirmar los cambios
db.commit()

# Cerrar la sesión
db.close() 