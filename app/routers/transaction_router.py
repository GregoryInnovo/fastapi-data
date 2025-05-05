from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, Traveler
from app.db.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.user import User

router = APIRouter(prefix="/transactions", tags=["transactions"])

class TravelerCreate(BaseModel):
    name: str
    dni: str
    age: int
    phone: str
    dni_image: str

class TransactionCreate(BaseModel):
    client_name: str
    client_email: str
    client_phone: str
    client_dni: str
    client_address: str
    invoice_image: str
    id_image: str
    package: str
    quoted_flight: str
    agency_cost: float
    amount: float
    transaction_type: str
    status: str
    seller_id: int
    receipt: str
    start_date: datetime = None
    end_date: datetime = None
    travelers: List[TravelerCreate]

@router.post("/", status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    new_transaction = Transaction(
        client_name=transaction.client_name,
        client_email=transaction.client_email,
        client_phone=transaction.client_phone,
        client_dni=transaction.client_dni,
        client_address=transaction.client_address,
        invoice_image=transaction.invoice_image,
        id_image=transaction.id_image,
        package=transaction.package,
        quoted_flight=transaction.quoted_flight,
        agency_cost=transaction.agency_cost,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        status=transaction.status,
        seller_id=transaction.seller_id,
        receipt=transaction.receipt,
        start_date=transaction.start_date,
        end_date=transaction.end_date,
        number_of_travelers=len(transaction.travelers)
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    for traveler_data in transaction.travelers:
        traveler = Traveler(
            name=traveler_data.name,
            dni=traveler_data.dni,
            age=traveler_data.age,
            phone=traveler_data.phone,
            dni_image=traveler_data.dni_image,
            transaction_id=new_transaction.id
        )
        db.add(traveler)

    db.commit()
    return {"message": "Transacción creada con éxito", "transaction": new_transaction}

@router.get("/")
def list_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones")
    
    result = []
    for transaction in transactions:
        # Obtener información del vendedor
        seller = db.query(User).filter(User.id == transaction.seller_id).first()
        travelers = db.query(Traveler).filter(Traveler.transaction_id == transaction.id).all()
        
        response = {
            "id": transaction.id,
            "client_name": transaction.client_name,
            "client_email": transaction.client_email,
            "client_phone": transaction.client_phone,
            "client_dni": transaction.client_dni,
            "client_address": transaction.client_address,
            "invoice_image": transaction.invoice_image,
            "id_image": transaction.id_image,
            "package": transaction.package,
            "quoted_flight": transaction.quoted_flight,
            "agency_cost": transaction.agency_cost,
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "status": transaction.status,
            "seller_id": transaction.seller_id,
            "seller_name": seller.name if seller else None,
            "receipt": transaction.receipt,
            "start_date": transaction.start_date,
            "end_date": transaction.end_date,
            "travelers": [
                {
                    "id": traveler.id,
                    "name": traveler.name,
                    "dni": traveler.dni,
                    "age": traveler.age,
                    "phone": traveler.phone,
                    "dni_image": traveler.dni_image
                } for traveler in travelers
            ]
        }
        result.append(response)
    
    return result


#Actualizar el Estado de una Transacción: (Por ejemplo, cambiar a "aprobado" o "rechazado").
@router.patch("/{transaction_id}/status", status_code=200)
def update_transaction_status(transaction_id: int, status: str, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    transaction.status = status
    db.commit()
    db.refresh(transaction)
    return {"message": "Estado de la transacción actualizado", "transaction": transaction}

#Obtener Detalles de una Transacción:
@router.get("/{transaction_id}")
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Obtener información del vendedor
    seller = db.query(User).filter(User.id == transaction.seller_id).first()
    
    # Obtener los viajeros asociados
    travelers = db.query(Traveler).filter(Traveler.transaction_id == transaction_id).all()
    
    # Estructura de respuesta
    response = {
        "id": transaction.id,
        "client_name": transaction.client_name,
        "client_email": transaction.client_email,
        "client_phone": transaction.client_phone,
        "client_dni": transaction.client_dni,
        "client_address": transaction.client_address,
        "invoice_image": transaction.invoice_image,
        "id_image": transaction.id_image,
        "package": transaction.package,
        "quoted_flight": transaction.quoted_flight,
        "agency_cost": transaction.agency_cost,
        "amount": transaction.amount,
        "transaction_type": transaction.transaction_type,
        "status": transaction.status,
        "seller_id": transaction.seller_id,
        "seller_name": seller.name if seller else None,
        "receipt": transaction.receipt,
        "start_date": transaction.start_date,
        "end_date": transaction.end_date,
        "travelers": [
            {
                "id": traveler.id,
                "name": traveler.name,
                "dni": traveler.dni,
                "age": traveler.age,
                "phone": traveler.phone,
                "dni_image": traveler.dni_image
            } for traveler in travelers
        ]
    }
    
    return response

#√Filtrar Transacciones por Estado: (Por ejemplo, "pendiente", "aprobado", etc.).
@router.get("/filter/{status}")
def filter_transactions_by_status(status: str, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.status == status).all()
    
    # Estructura de respuesta
    response = []
    for transaction in transactions:
        # Obtener información del vendedor
        seller = db.query(User).filter(User.id == transaction.seller_id).first()
        travelers = db.query(Traveler).filter(Traveler.transaction_id == transaction.id).all()
        
        response.append({
            "id": transaction.id,
            "client_name": transaction.client_name,
            "client_email": transaction.client_email,
            "client_phone": transaction.client_phone,
            "client_dni": transaction.client_dni,
            "client_address": transaction.client_address,
            "invoice_image": transaction.invoice_image,
            "id_image": transaction.id_image,
            "package": transaction.package,
            "quoted_flight": transaction.quoted_flight,
            "agency_cost": transaction.agency_cost,
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "status": transaction.status,
            "seller_id": transaction.seller_id,
            "seller_name": seller.name if seller else None,
            "receipt": transaction.receipt,
            "start_date": transaction.start_date,
            "end_date": transaction.end_date,
            "travelers": [
                {
                    "id": traveler.id,
                    "name": traveler.name,
                    "dni": traveler.dni,
                    "age": traveler.age,
                    "phone": traveler.phone,
                    "dni_image": traveler.dni_image
                } for traveler in travelers
            ]
        })
    
    return response

@router.get("/seller/{seller_id}")
def get_transactions_by_seller(seller_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.seller_id == seller_id).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones para este vendedor")
    
    # Obtener información del vendedor
    seller = db.query(User).filter(User.id == seller_id).first()
    
    # Estructura de respuesta
    response = []
    for transaction in transactions:
        travelers = db.query(Traveler).filter(Traveler.transaction_id == transaction.id).all()
        response.append({
            "id": transaction.id,
            "client_name": transaction.client_name,
            "client_email": transaction.client_email,
            "client_phone": transaction.client_phone,
            "client_dni": transaction.client_dni,
            "client_address": transaction.client_address,
            "invoice_image": transaction.invoice_image,
            "id_image": transaction.id_image,
            "package": transaction.package,
            "quoted_flight": transaction.quoted_flight,
            "agency_cost": transaction.agency_cost,
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "status": transaction.status,
            "seller_id": transaction.seller_id,
            "seller_name": seller.name if seller else None,
            "receipt": transaction.receipt,
            "start_date": transaction.start_date,
            "end_date": transaction.end_date,
            "travelers": [
                {
                    "id": traveler.id,
                    "name": traveler.name,
                    "dni": traveler.dni,
                    "age": traveler.age,
                    "phone": traveler.phone,
                    "dni_image": traveler.dni_image
                } for traveler in travelers
            ]
        })
    
    return response

@router.patch("/{transaction_id}", status_code=200)
def update_transaction(transaction_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    existing_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Actualizar solo los campos que se proporcionan
    if transaction.client_name is not None:
        existing_transaction.client_name = transaction.client_name
    if transaction.client_email is not None:
        existing_transaction.client_email = transaction.client_email
    if transaction.client_phone is not None:
        existing_transaction.client_phone = transaction.client_phone
    if transaction.client_dni is not None:
        existing_transaction.client_dni = transaction.client_dni
    if transaction.client_address is not None:
        existing_transaction.client_address = transaction.client_address
    if transaction.invoice_image is not None:
        existing_transaction.invoice_image = transaction.invoice_image
    if transaction.id_image is not None:
        existing_transaction.id_image = transaction.id_image
    if transaction.package is not None:
        existing_transaction.package = transaction.package
    if transaction.quoted_flight is not None:
        existing_transaction.quoted_flight = transaction.quoted_flight
    if transaction.agency_cost is not None:
        existing_transaction.agency_cost = transaction.agency_cost
    if transaction.amount is not None:
        existing_transaction.amount = transaction.amount
    if transaction.transaction_type is not None:
        existing_transaction.transaction_type = transaction.transaction_type
    if transaction.status is not None:
        existing_transaction.status = transaction.status
    if transaction.seller_id is not None:
        existing_transaction.seller_id = transaction.seller_id
    if transaction.receipt is not None:
        existing_transaction.receipt = transaction.receipt
    if transaction.start_date is not None:
        existing_transaction.start_date = transaction.start_date
    if transaction.end_date is not None:
        existing_transaction.end_date = transaction.end_date

    db.commit()
    db.refresh(existing_transaction)

    # Actualizar los viajeros si se proporciona una lista de viajeros
    if transaction.travelers is not None:
        # Primero, eliminar los viajeros existentes
        db.query(Traveler).filter(Traveler.transaction_id == transaction_id).delete()

        # Luego, agregar los nuevos viajeros
        for traveler_data in transaction.travelers:
            traveler = Traveler(
                name=traveler_data.name,
                dni=traveler_data.dni,
                age=traveler_data.age,
                phone=traveler_data.phone,
                dni_image=traveler_data.dni_image,
                transaction_id=existing_transaction.id
            )
            db.add(traveler)

    db.commit()
    return {"message": "Transacción actualizada con éxito", "transaction": existing_transaction}

@router.patch("/{transaction_id}/travelers/{traveler_id}", status_code=200)
def update_traveler(transaction_id: int, traveler_id: int, traveler_data: TravelerCreate, db: Session = Depends(get_db)):
    # Verificar si la transacción existe
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Verificar si el viajero existe
    traveler = db.query(Traveler).filter(Traveler.id == traveler_id, Traveler.transaction_id == transaction_id).first()
    if not traveler:
        raise HTTPException(status_code=404, detail="Viajero no encontrado")

    # Actualizar solo los campos que se proporcionan
    if traveler_data.name is not None:
        traveler.name = traveler_data.name
    if traveler_data.dni is not None:
        traveler.dni = traveler_data.dni
    if traveler_data.age is not None:
        traveler.age = traveler_data.age
    if traveler_data.phone is not None:
        traveler.phone = traveler_data.phone
    if traveler_data.dni_image is not None:
        traveler.dni_image = traveler_data.dni_image

    db.commit()
    db.refresh(traveler)

    return {"message": "Viajero actualizado con éxito", "traveler": traveler}
