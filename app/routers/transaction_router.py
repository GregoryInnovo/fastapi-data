import requests
from io import BytesIO
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload, selectinload
from app.models.transaction import (Transaction,
 Traveler,
 TransactionType,
 TransactionStatus, 
 Evidence, 
 Itinerario,
 TravelInfo,
 Documentos
 )
from app.db.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.user import User
from typing import Optional
from datetime import date

router = APIRouter(prefix="/transactions", tags=["transactions"])

class EvidenceCreate(BaseModel):
    evidence_file: str
    amount: float
    filename: str = None


class TravelerCreate(BaseModel):
    name: str
    dni: str
    date_birth: date
    phone: str

class TravelerUpdate(BaseModel):
    name: Optional[str]
    dni: Optional[str]
    date_birth: Optional[date]
    phone: Optional[str]

class ItinerarioCreate(BaseModel):
    aerolinea: str
    ruta: str
    fecha: datetime
    hora_salida: str
    hora_llegada: str

class ItinerarioUpdate(BaseModel):
    aerolinea: Optional[str] = None
    ruta: Optional[str] = None
    fecha: Optional[datetime] = None
    hora_salida: Optional[str] = None
    hora_llegada: Optional[str] = None

class CuentasRecaudo(BaseModel):
    banco: str
    numero: str
    nombre: str
    nit: str

class TravelInfoCrerate(BaseModel):
    hotel: str = None
    noches: int = None
    incluye: list = None
    no_incluye: list = None
    alimentacion: str = None
    acomodacion: str = None
    direccion_hotel: str = None
    pais_destino: str = None
    ciudad_destino: str = None

class TravelInfoUpdate(BaseModel):
    hotel: Optional[str] = None
    noches: Optional[int] = None
    incluye: Optional[list] = None
    no_incluye: Optional[list] = None
    alimentacion: Optional[str] = None
    acomodacion: Optional[str] = None
    direccion_hotel: Optional[str] = None
    pais_destino: Optional[str] = None
    ciudad_destino: Optional[str] = None


class DocumentosCreate(BaseModel):
    document_file: str
    tipo_documento: str
    filename: str

class DocumentosUpdate(BaseModel):
    document_file: Optional[str] = None
    tipo_documento: Optional[str] = None

class TransactionCreate(BaseModel):
    client_name: str
    client_email: str
    client_phone: str
    client_dni: str
    client_address: str
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
    travelers: List[TravelerCreate] = None
    travel_info: List[TravelInfoCrerate] = None
    evidence: EvidenceCreate = None
    itinerario: List[ItinerarioCreate] = None


class TransactionUpdate(BaseModel):
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_dni: Optional[str] = None
    client_address: Optional[str] = None
    package: Optional[str] = None
    quoted_flight: Optional[str] = None
    agency_cost: Optional[float] = None
    amount: Optional[float] = None
    transaction_type: Optional[TransactionType] = None
    status: Optional[TransactionStatus] = None
    seller_id: Optional[int] = None
    receipt: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    travelers: Optional[List[TravelerCreate]] = None
    travel_info: Optional[List[TravelInfoCrerate]] = None
    evidence: Optional[EvidenceCreate] = None
    itinerario: Optional[List[ItinerarioCreate]] = None
   


@router.post("/", status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    new_transaction = Transaction(
        client_name=transaction.client_name,
        client_email=transaction.client_email,
        client_phone=transaction.client_phone,
        client_dni=transaction.client_dni,
        client_address=transaction.client_address,
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

    if transaction.travelers:
        for traveler_data in transaction.travelers:
            traveler = Traveler(
                name=traveler_data.name,
                dni=traveler_data.dni,
                date_birth=traveler_data.date_birth,
                phone=traveler_data.phone,
                transaction_id=new_transaction.id
            )
            db.add(traveler)

    if transaction.travel_info:
        for info in transaction.travel_info:
            travel_info = TravelInfo(
                hotel=info.hotel,
                noches=info.noches,
                incluye=info.incluye,
                no_incluye=info.no_incluye,
                transaction_id=new_transaction.id,
                alimentacion = info.alimentacion,
                acomodacion =  info.acomodacion,
                direccion_hotel = info.direccion_hotel,
                pais_destino = info.pais_destino,
                ciudad_destino = info.ciudad_destino
            )
            db.add(travel_info)
    # if transaction.evidence and transaction.evidence.evidence_file[:5] != "https":
    #     base64_string = transaction.evidence.evidence_file
    #     filename = transaction.evidence.filename
    #     # Elimina encabezado "data:image/png;base64,..." si existe
    #     if "," in base64_string:
    #         base64_string = base64_string.split(",")[1]
    #     image_data = base64.b64decode(base64_string)
    #     file = BytesIO(image_data)
    #     file.name = filename+".jpeg"
        

    #     url = "https://elder-link-staging-n8n.fwoasm.easypanel.host/webhook/6e0954b7-832f-4817-86cd-9c59f18d8a52"
    #     image_bytes = file
    #     files = {"data": (file.name,
    #                         image_bytes, "application/octet-stream")} 
    #     headers = {"Content-Type": "application/json"}
    #     res = requests.post(url, files=files)
    #     if res.status_code != 200:
    #         raise HTTPException(status_code=500, detail="Error al subir el documento")
    #     print(res.text)
    #     try:
    #         payload_resp = res.json()  # parsea el JSON
    #         document_url = payload_resp[0].get("imageUrl")
    #     except:
    #         texto = res.text.strip()
    #         raise HTTPException(
    #             status_code=500,
    #             detail=(
    #                 "El servicio de storage no devolvió un JSON válido. "
    #                 f"Contenido bruto: {texto!r}"
    #             )
    #         )


    #     evidence = Evidence(
    #         evidence_file=document_url,
    #         amount=transaction.evidence.amount,
    #         transaction_id=new_transaction.id
    #     )
    #     db.add(evidence)
    # if transaction.evidence and transaction.evidence.evidence_file[:5] == "https":
        # evidence = Evidence(
        #     evidence_file=transaction.evidence.evidence_file,
        #     amount=transaction.evidence.amount,
        #     transaction_id=new_transaction.id
        # )
        # db.add(evidence)
    
    if transaction.itinerario:
        for itinerario in transaction.itinerario:
            itinerarios = Itinerario(
                hora_llegada=itinerario.hora_llegada,
                hora_salida=itinerario.hora_salida,
                fecha=itinerario.fecha,
                ruta=itinerario.ruta,
                aerolinea=itinerario.aerolinea,
                transaction_id=new_transaction.id
            )
            db.add(itinerarios)
    db.commit()
    return {"message": "Transacción creada con éxito", "transaction_id": new_transaction.id}

@router.get("/", status_code=200)
def get_all_transaction_test(db: Session = Depends(get_db)):
    transactions = (
        db.query(Transaction)
        .options(
            joinedload(Transaction.seller),
            selectinload(Transaction.travelers),
            selectinload(Transaction.evidences),
            selectinload(Transaction.itinerario),
            selectinload(Transaction.documentos),
            selectinload(Transaction.travel_info),
            selectinload(Transaction.itinerario)
        )
        .order_by(Transaction.id.desc())
        .all()
    )
    if not transactions:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones")
    
    return transactions

@router.get("/test")
def list_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones")
    
    result = []
    for transaction in transactions:
        # Obtener información del vendedor
        seller = db.query(User).filter(User.id == transaction.seller_id).first()
        travelers = db.query(Traveler).filter(Traveler.transaction_id == transaction.id).all()
        #itinerario = db.query(Itinerario).filter(Itinerario.transaction_id == transaction.id).all()
        evidences = db.query(Evidence).filter(Evidence.transaction_id == transaction.id).all()
        response = {
            "id": transaction.id,
            "client_name": transaction.client_name,
            "client_email": transaction.client_email,
            "client_phone": transaction.client_phone,
            "client_dni": transaction.client_dni,
            "client_address": transaction.client_address,
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
                    "date_birth": traveler.date_birth,
                    "phone": traveler.phone
                } for traveler in travelers
            ],
            "itinerario": transaction.itinerario,
            "travelers": transaction.travelers,
            "travel_info": transaction.travel_info,
            "documentos": transaction.documentos,
            "evidences": [
                {
                "id": evidence.id,
                "transaction_id": evidence.transaction_id,
                "evidence_file": evidence.evidence_file,
                "upload_date": evidence.upload_date,
                "amount": evidence.amount
                } for evidence in evidences
            ]
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

    travel_info = db.query(TravelInfo).filter(TravelInfo.transaction_id == transaction_id).all()
    documents = db.query(Documentos).filter(Documentos.transaction_id == transaction_id).all()
    evidences = db.query(Evidence).filter(Evidence.transaction_id == transaction_id).all()
    itinerarios = db.query(Itinerario).filter(Itinerario.transaction_id == transaction_id).all()
    # Estructura de respuesta
    response = {
        "id": transaction.id,
        "client_name": transaction.client_name,
        "client_email": transaction.client_email,
        "client_phone": transaction.client_phone,
        "client_dni": transaction.client_dni,
        "client_address": transaction.client_address,
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
                "date_birth": traveler.date_birth,
                "phone": traveler.phone
            } for traveler in travelers
        ],
        "itinerario": transaction.itinerario,
        "travelers": transaction.travelers,
        "travel_info": travel_info,
        "documentos": documents,
        "evidence": [
                {
                "id": evidence.id,
                "transaction_id": evidence.transaction_id,
                "evidence_file": evidence.evidence_file,
                "upload_date": evidence.upload_date,
                "amount": evidence.amount
                } for evidence in evidences
            ],
        "itinerario": [
            {"id": itinerario.id,
             "transaction_id": itinerario.transaction_id,
             "aerolinea": itinerario.aerolinea,
             "ruta": itinerario.ruta,
             "hora_salida": itinerario.hora_salida,
             "hora_llegada": itinerario.hora_llegada
            } for itinerario in itinerarios
        ]
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
                    "date_birth": traveler.date_birth,
                    "phone": traveler.phone
                } for traveler in travelers
            ],
            "itinerario": transaction.itinerario
        })
    
    return response

@router.get("/seller/{seller_id}")
def get_transactions_by_seller(seller_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.seller_id == seller_id).order_by(Transaction.id.desc()).all()
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
                    "date_birth": traveler.date_birth,
                    "phone": traveler.phone
                } for traveler in travelers
            ],
            "itinerario": transaction.itinerario,
            "travelers": transaction.travelers,
            "travel_info": transaction.travel_info,
            "documentos": transaction.documentos
        })
    
    return response

@router.patch("/{transaction_id}", status_code=200)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    existing_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not existing_transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Actualizar campos básicos de la transacción
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

    # Actualizar viajeros
    if transaction.travelers is not None:
        #db.query(Traveler).filter(Traveler.transaction_id == transaction_id).delete()
        for traveler_data in transaction.travelers:
            traveler = Traveler(
                name=traveler_data.name,
                dni=traveler_data.dni,
                date_birth=traveler_data.date_birth,
                phone=traveler_data.phone,
                transaction_id=existing_transaction.id
            )
            db.add(traveler)
    
    # Actualizar información de viaje
    if transaction.travel_info is not None:
        #db.query(TravelInfo).filter(TravelInfo.transaction_id == transaction_id).delete()
        for travel_info_data in transaction.travel_info:
            travel_info = TravelInfo(
                transaction_id=existing_transaction.id,
                hotel=travel_info_data.hotel,
                noches=travel_info_data.noches,
                incluye=travel_info_data.incluye,
                no_incluye=travel_info_data.no_incluye,
                alimentacion = travel_info.alimentacion,
                acomodacion =  travel_info.acomodacion,
                direccion_hotel = travel_info.direccion_hotel,
                pais_destino = travel_info.pais_destino,
                ciudad_destino = travel_info.ciudad_destino
            )
            db.add(travel_info)

    # Actualizar itinerario
    if transaction.itinerario is not None:
        #db.query(Itinerario).filter(Itinerario.transaction_id == transaction_id).delete()
        for itinerario_data in transaction.itinerario:
            itinerario = Itinerario(
                transaction_id=existing_transaction.id,
                aerolinea=itinerario_data.aerolinea,
                ruta=itinerario_data.ruta,
                fecha=itinerario_data.fecha,
                hora_salida=itinerario_data.hora_salida,
                hora_llegada=itinerario_data.hora_llegada
            )
            db.add(itinerario)

    # Actualizar evidencias
    if transaction.evidence is not None:
        db.query(Evidence).filter(Evidence.transaction_id == transaction_id).delete()
        evidence = Evidence(
            transaction_id=existing_transaction.id,
            evidence_file=transaction.evidence.evidence_file,
            amount=transaction.evidence.amount
        )
        db.add(evidence)

    db.commit()
    db.refresh(existing_transaction)

    # Obtener la transacción actualizada con todas sus relaciones
    updated_transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .options(
            joinedload(Transaction.seller),
            selectinload(Transaction.travelers),
            selectinload(Transaction.evidences),
            selectinload(Transaction.itinerario),
            selectinload(Transaction.documentos),
            selectinload(Transaction.travel_info)
        )
        .first()
    )

    return {
        "message": "Transacción actualizada con éxito",
        "transaction": updated_transaction
    }
    
@router.patch("/{transaction_id}/travelers/{traveler_id}", status_code=200)
def update_traveler(transaction_id: int, traveler_id: int, traveler_data: TravelerUpdate, db: Session = Depends(get_db)):
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
    if traveler_data.date_birth is not None:
        traveler.date_birth = traveler_data.date_birth
    if traveler_data.phone is not None:
        traveler.phone = traveler_data.phone


    db.commit()
    db.refresh(traveler)

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
                    "date_birth": traveler.date_birth,
                    "phone": traveler.phone
                } for traveler in travelers
            ],
            "itinerario": transaction.itinerario,
            "travelers": transaction.travelers,
            "travel_info": transaction.travel_info,
            "documentos": transaction.documentos
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
                    "date_birth": traveler.date_birth,
                    "phone": traveler.phone
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
        transaction_id=transaction_id,
        evidence_file=evidence.evidence_file,
        amount=evidence.amount
    )
    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)

    return {"message": "Evidencia agregada con éxito", "evidence": new_evidence}

@router.get("/{transaction_id}/evidence")
def get_evidences_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.transaction_id == transaction_id).all()
    if not evidence:
        raise HTTPException(status_code=404, detail="No se encontraron evidencias para esta transacción")
    return evidence

@router.delete("/{transaction_id}/evidence/{evidence_id}", status_code=204)
def delete_evidence(transaction_id: int, evidence_id: int, db: Session = Depends(get_db)):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id, Evidence.transaction_id == transaction_id).first()
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
def update_itinerario(transaction_id: int, itinerario_id: int, itinerario_data: ItinerarioUpdate, db: Session = Depends(get_db)):
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

@router.post("/{transaction_id}/travel_info", status_code=201)
def create_travel_info(transaction_id: int, travel_info: TravelInfoCrerate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaccion no encontrada")

    new_travel_info = TravelInfo(
        transaction_id = transaction_id,
        hotel = travel_info.hotel,
        noches = travel_info.noches,
        incluye = travel_info.incluye,
        no_incluye = travel_info.no_incluye,
        alimentacion = travel_info.alimentacion,
        acomodacion =  travel_info.acomodacion,
        direccion_hotel = travel_info.direccion_hotel,
        pais_destino = travel_info.pais_destino,
        ciudad_destino = travel_info.ciudad_destino
    )

    db.add(new_travel_info)
    db.commit()
    db.refresh(new_travel_info)
    return {"message": "Travel Info upload", "travel_info": new_travel_info}


@router.get("/{transaction_id}/travel_info")
def get_travel_info_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    travel_info = db.query(TravelInfo).filter(TravelInfo.transaction_id == transaction_id).all()
    if not travel_info:
        raise HTTPException(status_code=404, detail="No se encontraron datos de viaje para esta transaccion")
    return travel_info

@router.delete("/{transaction_id}/travel_info/{travel_info_id}", status_code=200)
def delete_travel_info(transaction_id: int, travel_info_id: int, db: Session = Depends(get_db)):
    travel_info = db.query(TravelInfo).filter(TravelInfo.id == travel_info_id, Transaction.id == transaction_id).first()
    if not travel_info:
        raise HTTPException(status_code = 404, detail = "No se encontro esta informacion de viaje para este itinerario")

    db.delete(travel_info)
    db.commit()
    return {"message": "Informacion de viaje eliminada con exito"}

@router.patch("/{transaction_id}/travel_info/{travel_info_id}", status_code=200)
def update_travel_info_by_transaction_id(transaction_id: int, travel_info_id: int, data: TravelInfoUpdate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="No Se encontro la transaccion")
    
    travel_info = db.query(TravelInfo).filter(TravelInfo.id == travel_info_id).first()

    if data.hotel is not None:
        travel_info.hotel = data.hotel
    if data.noches is not None:
        travel_info.noches = data.noches
    if data.incluye is not None:
        travel_info.incluye = data.incluye
    if data.no_incluye is not None:
        travel_info.no_incluye = data.no_incluye

    db.commit()
    db.refresh(travel_info)
    return {"message": "TravelInfo actualizado con exito", "documento": travel_info}


@router.get("/travel_info/list")
def list_all_travel_info(db: Session = Depends(get_db)):
    travel_info = db.query(TravelInfo).all()
    if not travel_info:
        raise HTTPException(status_code = 404, detail = "No se encontraron registros de informacion de viaje")
    return travel_info


@router.post("/{transaction_id}/documentos/{traveler_id}", status_code=201)
async def add_documentos(transaction_id: int, traveler_id: int, data: DocumentosCreate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} no encontrada")

    new_documento = Documentos(
        transaction_id=transaction_id,
        viajero_id=traveler_id,
        document_url=data.document_file,
        tipo_documento=data.tipo_documento
    )

    db.add(new_documento)
    db.commit()
    db.refresh(new_documento)

    return {"message": "Documento agregado con éxito", "documento": new_documento}


# @router.post("/{transaction_id}/documentos/{traveler_id}", status_code=201)
# # async def add_documentos(transaction_id: int, traveler_id: int, documentos: DocumentosCreate, db: Session = Depends(get_db)):
# async def add_documentos(transaction_id: int, traveler_id: int, document_file: UploadFile = File(...), tipo_documento: str = Form(...), db: Session = Depends(get_db)):
#     transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
#     if not transaction:
#         raise HTTPException(status_code=404, detail="Transacción no encontrada")

#     #Upload the document file to a storage service (AWS S3) retrive the url
#     url = "https://elder-link-staging-n8n.fwoasm.easypanel.host/webhook/dc87c6e6-7f0b-4734-965e-89ab5d5b7b00"
#     image_bytes = await document_file.read()
#     #data = {"data": base64_encoded_file}
#     files = {"data": (document_file.filename,
#                         image_bytes, "application/octet-stream")}      
#     # image_bytes = await documentos.document_file.read()
#     # base64_encoded_file = base64.b64encode(image_bytes).decode("utf-8")
#     #image_bytes = await document_file.read()
#     #base64_encoded_file = base64.b64encode(image_bytes).decode("utf-8")
#     #data = {"data": base64_encoded_file}
#     headers = {"Content-Type": "application/json"}
#     res = requests.post(url, files=files)
#     if res.status_code != 200:
#         raise HTTPException(status_code=500, detail="Error al subir el documento")
#     print(res.text)
#     try:
#         payload_resp = res.json()  # parsea el JSON
#         document_url = payload_resp.get("imageUrl")
#     except:
#         texto = res.text.strip()
#         raise HTTPException(
#             status_code=500,
#             detail=(
#                 "El servicio de storage no devolvió un JSON válido. "
#                 f"Contenido bruto: {texto!r}"
#             )
#         )
#     new_documento = Documentos(
#         transaction_id=transaction_id,
#         viajero_id=traveler_id,
#         document_url=document_url,
#         tipo_documento=tipo_documento
#     )
#     db.add(new_documento)
#     db.commit()
#     db.refresh(new_documento)
#     return {"message": "Documento agregado con éxito", "documento": new_documento}

@router.get("/{transaction_id}/documentos")
def get_documentos_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    documentos = db.query(Documentos).filter(Documentos.transaction_id == transaction_id).all()
    if not documentos:
        raise HTTPException(status_code=404, detail="No se encontraron documentos para esta transacción")
    return documentos

@router.delete("/{transaction_id}/documentos/{documento_id}", status_code=204)
def delete_documento(transaction_id: int, documento_id: int, db: Session = Depends(get_db)):
    documento = db.query(Documentos).filter(Documentos.id == documento_id, Documentos.transaction_id == transaction_id).first()
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    db.delete(documento)
    db.commit()
    return {"message": "Documento eliminado con éxito"}

@router.get("/documentos/list")
def list_all_documentos(db: Session = Depends(get_db)):
    documentos = db.query(Documentos).all()
    if not documentos:
        raise HTTPException(status_code=404, detail="No se encontraron documentos")
    return documentos


@router.get("/user/paid/{id_user}")
def get_transaction_payments(id_user: int, db: Session = Depends(get_db)):
    # Obtener todas las transacciones del vendedor con sus evidencias
    transactions = (
        db.query(Transaction)
        .filter(Transaction.seller_id == id_user)
        .options(selectinload(Transaction.evidences))
        .all()
    )
    
    if not transactions:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron transacciones totalmente pagadas para este vendedor"
        )
    
    # Filtrar las transacciones que están completamente pagadas
    paid_transactions = []
    for transaction in transactions:
        total_paid = sum(evidence.amount for evidence in transaction.evidences)
        if total_paid >= transaction.amount:  # >= por si hay sobrepagos
            paid_transactions.append({
                "id": transaction.id,
                "client_name": transaction.client_name,
                "package": transaction.package,
                "total_amount": transaction.amount,
                "total_paid": total_paid,
                "status": transaction.status,
                "created_at": transaction.created_at,
                "evidences": [
                    {
                        "id": evidence.id,
                        "amount": evidence.amount,
                        "evidence_file": evidence.evidence_file,
                        "upload_date": evidence.upload_date
                    } for evidence in transaction.evidences
                ]
            })
    
    return {
        "seller_id": id_user,
        "total_paid_transactions": len(paid_transactions),
        "transactions": paid_transactions
    }


@router.get("/admin/paid-transactions")
def get_all_paid_transactions(db: Session = Depends(get_db)):
    # Obtener todas las transacciones con sus evidencias
    transactions = (
        db.query(Transaction)
        .options(
            selectinload(Transaction.evidences),
            selectinload(Transaction.seller)
        )
        .all()
    )
    
    if not transactions:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron transacciones en el sistema"
        )
    
    # Filtrar las transacciones que están completamente pagadas
    paid_transactions = []
    for transaction in transactions:
        total_paid = sum(evidence.amount for evidence in transaction.evidences)
        if total_paid >= transaction.amount:  # >= por si hay sobrepagos
            paid_transactions.append({
                "id": transaction.id,
                "client_name": transaction.client_name,
                "package": transaction.package,
                "total_amount": transaction.amount,
                "total_paid": total_paid,
                "status": transaction.status,
                "created_at": transaction.created_at,
                "seller": {
                    "id": transaction.seller.id,
                    "name": transaction.seller.name,
                    "email": transaction.seller.email
                } if transaction.seller else None,
                "evidences": [
                    {
                        "id": evidence.id,
                        "amount": evidence.amount,
                        "evidence_file": evidence.evidence_file,
                        "upload_date": evidence.upload_date
                    } for evidence in transaction.evidences
                ]
            })
    
    # Calcular estadísticas
    total_amount = sum(t["total_amount"] for t in paid_transactions)
    total_paid = sum(t["total_paid"] for t in paid_transactions)
    
    return {
        "total_paid_transactions": len(paid_transactions),
        "total_amount": total_amount,
        "total_paid": total_paid,
        "transactions": paid_transactions
    }