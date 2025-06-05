from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.transaction import (Transaction,
 Traveler,
 TransactionType,
 TransactionStatus, 
 Evidence, 
 Itinerario
 )
from app.db.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.user import User
from typing import Optional

router = APIRouter(prefix="/transactions", tags=["transactions"])

class EvidenceCreate(BaseModel):
    evidence_file: str
    amount: float


class TravelerCreate(BaseModel):
    name: str
    dni: str
    age: int
    phone: str
    dni_image: str

class ItinerarioCreate(BaseModel):
    aerolinea: str
    ruta: str
    fecha: datetime
    hora_salida: str
    hora_llegada: str

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
    transaction_type: TransactionType
    status: TransactionStatus = TransactionStatus.pending
    seller_id: int
    receipt: str
    start_date: datetime = None
    end_date: datetime = None
    travelers: List[TravelerCreate]
   
class ItineararioUpdate(BaseModel):
    aerolinea: Optional[str] = None
    ruta: Optional[str] = None
    fecha: Optional[datetime] = None
    hora_salida: Optional[str] = None
    hora_llegada: Optional[str] = None

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
        transaction_type=transaction.transaction_type.value,
        status=transaction.status.value,
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
        #itinearrio = db.query(Itinerario).filter(Itinerario.transaction_id == transaction.id).all()
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
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
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
            ],
            "itinerario": transaction.itinerario
        }
        result.append(response)
    
    return result


#Actualizar el Estado de una Transacción: (Por ejemplo, cambiar a "aprobado" o "rechazado").
@router.patch("/{transaction_id}/status", status_code=200)
def update_transaction_status(transaction_id: int, status: TransactionStatus, db: Session = Depends(get_db)):
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
        "created_at": transaction.created_at,
        "updated_at": transaction.updated_at,
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
        ],
        "itinerario": transaction.itinerario
    }
    
    return response

#√Filtrar Transacciones por Estado: (Por ejemplo, "pendiente", "aprobado", etc.).
@router.get("/filter/{status}")
def filter_transactions_by_status(status: TransactionStatus, db: Session = Depends(get_db)):
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
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
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
            ],
            "itinerario": transaction.itinerario
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
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
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
            ],
            "itinerario": transaction.itinerario
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
        existing_transaction.transaction_type = transaction.transaction_type.value
    if transaction.status is not None:
        existing_transaction.status = transaction.status.value
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

    db.refresh(traveler)
    db.commit()

    return {"message": "Viajero actualizado con éxito", "traveler": traveler}

@router.get("/date-range/")
def get_transactions_by_date_range(
    start_date: datetime,
    end_date: datetime,
    date_field: str = "created_at",  # Opciones: created_at, updated_at, start_date, end_date
    db: Session = Depends(get_db)
):
    # Validar el campo de fecha
    valid_date_fields = ["created_at", "updated_at", "start_date", "end_date"]
    if date_field not in valid_date_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Campo de fecha inválido. Debe ser uno de: {', '.join(valid_date_fields)}"
        )

    # Construir la consulta base
    query = db.query(Transaction)
    
    # Aplicar el filtro según el campo de fecha seleccionado
    date_column = getattr(Transaction, date_field)
    transactions = query.filter(
        date_column >= start_date,
        date_column <= end_date
    ).all()
    
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron transacciones en el rango de fechas especificado para el campo {date_field}"
        )
    
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
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
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
            ],
            "itinerario": transaction.itinerario
        })
    
    return response

@router.get("/filter-mixed/")
def filter_transactions_mixed(
    seller_id: int = None,
    status: TransactionStatus = None,
    start_date: datetime = None,
    end_date: datetime = None,
    date_field: str = "created_at",
    db: Session = Depends(get_db)
):
    # Construir la consulta base
    query = db.query(Transaction)
    
    # Aplicar filtros si se proporcionan
    if seller_id is not None:
        query = query.filter(Transaction.seller_id == seller_id)
    
    if status is not None:
        query = query.filter(Transaction.status == status)
    
    if start_date is not None and end_date is not None:
        # Validar el campo de fecha
        valid_date_fields = ["created_at", "updated_at", "start_date", "end_date"]
        if date_field not in valid_date_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Campo de fecha inválido. Debe ser uno de: {', '.join(valid_date_fields)}"
            )
        date_column = getattr(Transaction, date_field)
        query = query.filter(
            date_column >= start_date,
            date_column <= end_date
        )
    
    # Ejecutar la consulta
    transactions = query.all()
    
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron transacciones con los criterios especificados"
        )
    
    # Estructura de respuesta
    response = []
    for transaction in transactions:
        # Obtener información del vendedor
        seller = db.query(User).filter(User.id == transaction.seller_id).first()
        travelers = db.query(Traveler).filter(Traveler.transaction_id == transaction.id).all()
        itinerary = db.query(Itinerario).filter(Itinerario.transaction_id == transaction.id).all()
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
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
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
            ],
            "itinerario": [
                {
                    "id": itinerary.id,
                    "aerolinea": itinerary.aerolinea,
                    "ruta": itinerary.ruta,
                    "fecha": itinerary.fecha,
                    "hora_salida": itinerary.hora_salida,
                    "hora_llegada": itinerary.hora_llegada

                } for itinerary in transaction.itineraries
            ]
        })
    
    return response

@router.post("/{transaction_id}/evidence", status_code=201)
def add_evidence(transaction_id: int, evidence: EvidenceCreate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    new_evidence = Evidence(
        id_transaction=transaction_id,
        evidence_file=evidence.evidence_file,
        amount=evidence.amount
    )
    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)

    return {"message": "Evidencia agregada con éxito", "evidence": new_evidence}

@router.get("/{transaction_id}/evidence")
def get_evidences_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id_transaction == transaction_id).all()
    if not evidence:
        raise HTTPException(status_code=404, detail="No se encontraron evidencias para esta transacción")
    return evidence

@router.delete("/{transaction_id}/evidence/{evidence_id}", status_code=204)
def delete_evidence(transaction_id: int, evidence_id: int, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id, Evidence.id_transaction == transaction_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    db.delete(evidence)
    db.commit()
    return {"message": "Evidencia eliminada con éxito"}

@router.get("/evidence/list")
def list_all_evidences(db: Session = Depends(get_db)):
    evidences = db.query(Evidence).all()
    if not evidences:
        raise HTTPException(status_code=404, detail="No se encontraron evidencias")
    return evidences

@router.post("/{transaction_id}/itinerario", status_code=201)
def add_itinerario(transaction_id: int, itinerario: ItinerarioCreate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    new_itinerario = Itinerario(
        transaction_id=transaction_id,
        aerolinea=itinerario.aerolinea,
        ruta=itinerario.ruta,
        fecha=itinerario.fecha,
        hora_salida=itinerario.hora_salida,
        hora_llegada=itinerario.hora_llegada
    )
    db.add(new_itinerario)
    db.commit()
    db.refresh(new_itinerario)

    return {"message": "Itinerario agregado con éxito", "itinerario": new_itinerario}

@router.get("/{transaction_id}/itinerario")
def get_itinerario_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    itinerario = db.query(Itinerario).filter(Itinerario.transaction_id == transaction_id).all()
    if not itinerario:
        raise HTTPException(status_code=404, detail="No se encontró itinerario para esta transacción")
    return itinerario


@router.delete("/{transaction_id}/itinerario/{itinerario_id}", status_code=200)
def delete_itinerario(transaction_id: int, itinerario_id: int, db: Session = Depends(get_db)):
    itinerario = db.query(Itinerario).filter(Itinerario.id == itinerario_id, Itinerario.transaction_id == transaction_id).first()
    if not itinerario:
        raise HTTPException(status_code=404, detail="Itinerario no encontrado")

    db.delete(itinerario)
    db.commit()
    return {"message": "Itinerario eliminado con éxito"}


@router.get("/itinerario/list")
def list_all_itinerarios(db: Session = Depends(get_db)):
    itinerarios = db.query(Itinerario).all()
    if not itinerarios:
        raise HTTPException(status_code=404, detail="No se encontraron itinerarios")
    return itinerarios

@router.patch("/{transaction_id}/itinerario/{itinerario_id}", status_code=200)
def update_itinerario(transaction_id: int, itinerario_id: int, itinerario_data: ItineararioUpdate, db: Session = Depends(get_db)):
    itinerario = db.query(Itinerario).filter(Itinerario.id == itinerario_id, Itinerario.transaction_id == transaction_id).first()
    if not itinerario:
        raise HTTPException(status_code=404, detail="Itinerario no encontrado")

    # Actualizar solo los campos que se proporcionan
    if itinerario_data.aerolinea is not None:
        itinerario.aerolinea = itinerario_data.aerolinea
    if itinerario_data.ruta is not None:
        itinerario.ruta = itinerario_data.ruta
    if itinerario_data.fecha is not None:
        itinerario.fecha = itinerario_data.fecha
    if itinerario_data.hora_salida is not None:
        itinerario.hora_salida = itinerario_data.hora_salida
    if itinerario_data.hora_llegada is not None:
        itinerario.hora_llegada = itinerario_data.hora_llegada

    db.commit()
    db.refresh(itinerario)

    return {"message": "Itinerario actualizado con éxito", "itinerario": itinerario}