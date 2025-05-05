from app.db.database import Base, engine
from app.models.user import User
from app.models.transaction import Transaction, Traveler
from app.models.event import Event

# Crear las tablas
print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas con éxito")
