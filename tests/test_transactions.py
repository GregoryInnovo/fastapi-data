from fastapi.testclient import TestClient
from app.main import app
from app.models.transaction import Transaction, Traveler
from app.db.database import get_db
from sqlalchemy.orm import Session

client = TestClient(app)

# Helper function to get a database session
def get_db_session():
    db = next(get_db())
    return db

# Test creating a transaction
def test_create_transaction():
    response = client.post("/transactions/", json={
        "client_name": "Jane Doe",
        "client_email": "jane@example.com",
        "client_phone": "123456789",
        "client_dni": "12345678",
        "client_address": "123 Main St",
        "invoice_image": "invoice.jpg",
        "id_image": "id.jpg",
        "package": "Vacation Package",
        "quoted_flight": "Flight 123",
        "agency_cost": 100.0,
        "amount": 200.0,
        "transaction_type": "venta",
        "status": "pendiente",
        "seller_id": 1,
        "receipt": "receipt.jpg",
        "start_date": "2025-01-05T01:34:18.581Z",
        "end_date": "2025-01-10T01:34:18.581Z",
        "travelers": [
            {
                "name": "Traveler One",
                "dni": "87654321",
                "age": 30,
                "phone": "987654321",
                "dni_image": "traveler_id.jpg"
            }
        ]
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Transacción creada con éxito"

# Test getting a transaction
def test_get_transaction():
    # First create a transaction
    test_create_transaction()
    
    response = client.get("/transactions/13")  # Assuming the ID of the created transaction is 1
    assert response.status_code == 200
    assert response.json()["client_name"] == "Laura Sánchez"

# Test updating a transaction
def test_update_transaction():
    # First create a transaction
    test_create_transaction()
    
    response = client.patch("/transactions/13", json={
        "client_name": "Jane Smith",
        "client_email": "jane.smith@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Transacción actualizada con éxito"

    # Verify the update
    updated_response = client.get("/transactions/13")
    assert updated_response.json()["client_name"] == "Jane Smith"

# Test patching a traveler
def test_update_traveler():
    # First create a transaction
    test_create_transaction()
    
    # Assuming the traveler ID is 1
    response = client.patch("/transactions/13/travelers/1", json={
        "name": "Traveler Updated",
        "dni": "87654321",
        "age": 31,
        "phone": "987654321",
        "dni_image": "updated_traveler_id.jpg"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Viajero actualizado con éxito"

    # Verify the update
    transaction_response = client.get("/transactions/13")
    assert transaction_response.json()["travelers"][0]["name"] == "Traveler Updated"

# Test filtering transactions by status
def test_filter_transactions_by_status():
    # First create a transaction
    test_create_transaction()
    
    response = client.get("/transactions/filter/pendiente")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Ensure there is at least one transaction

# Test getting transactions by seller
def test_get_transactions_by_seller():
    # First create a transaction
    test_create_transaction()
    
    response = client.get("/transactions/seller/1")  # Assuming seller_id is 1
    assert response.status_code == 200
    assert len(response.json()) > 0  # Ensure there is at least one transaction

# Test updating transaction status
def test_update_transaction_status():
    # First create a transaction
    test_create_transaction()
    
    response = client.patch("/transactions/1/status", json={"status": "aprobado"})
    assert response.status_code == 200
    assert response.json()["message"] == "Estado de la transacción actualizado"

    # Verify the update
    updated_response = client.get("/transactions/1")
    assert updated_response.json()["status"] == "aprobado"

"""
Explicación de las pruebas:
test_create_transaction: Prueba la creación de una nueva transacción y verifica que la respuesta sea correcta.
test_get_transaction: Verifica que se pueda obtener una transacción específica después de crearla.
test_update_transaction: Prueba la actualización de una transacción y verifica que los cambios se reflejen correctamente.
test_update_traveler: Prueba la actualización de un traveler específico dentro de una transacción.
test_filter_transactions_by_status: Verifica que se puedan filtrar las transacciones por estado.
test_get_transactions_by_seller: Verifica que se puedan obtener transacciones asociadas a un vendedor específico.
test_update_transaction_status: Prueba la actualización del estado de una transacción y verifica que el cambio se refleje correctamente.
"""