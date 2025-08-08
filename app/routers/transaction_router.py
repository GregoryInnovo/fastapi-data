import requests
from io import BytesIO
import base64
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import func
from app.models.transaction import (Transaction,
 Traveler,
 TransactionType,
 TransactionStatus, 
 PaymentStatus,
 Evidence,
 EvidenceStatus,
 EvidenceInvoiceStatus,
 Itinerario,
 TravelInfo,
 Documentos,
 Factura
 )
from app.db.database import get_db
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models.user import User
from typing import Optional
from datetime import date
import locale

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
    payment_status: PaymentStatus = PaymentStatus.pago_incompleto
    seller_id: int
    receipt: str
    start_date: datetime = None
    end_date: datetime = None
    travelers: List[TravelerCreate] = None
    travel_info: List[TravelInfoCrerate] = None
    evidence: List[EvidenceCreate] = None
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
    payment_status: Optional[PaymentStatus] = None
    seller_id: Optional[int] = None
    receipt: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    travelers: Optional[List[TravelerCreate]] = None
    travel_info: Optional[List[TravelInfoCrerate]] = None
    evidence: Optional[EvidenceCreate] = None
    itinerario: Optional[List[ItinerarioCreate]] = None

class FacturaCreate(BaseModel):
    reserva_numero: str
    fecha_compra: date
    agencia_nombre: str
    nit_agencia: str
    rnt_agencia: str
    cliente_nombre: str
    cliente_documento: str
    pais_destino: str
    ciudad_salida: str
    ciudad_llegada: str
    fecha_inicio_viaje: date
    fecha_regreso_viaje: date
    hotel_nombre: Optional[str] = None
    num_noches: Optional[int] = None
    tarifa_por_pasajero: float
    tarifa_por_niño: Optional[float] = None
    abono: Optional[float] = None
    cuentas_recaudo: Optional[List[CuentasRecaudo]] = None
    pago_transferencia: bool = False
    pago_efectivo: bool = False
    nota_importante_contenido: Optional[str] = None
    nota_condicion_pago: Optional[str] = None
    monto_total_acumulado: Optional[float] = None
    travelers: Optional[List[TravelerCreate]] = None


class FacturaUpdate(BaseModel):
    reserva_numero: Optional[str] = None
    fecha_compra: Optional[date] = None
    agencia_nombre: Optional[str] = None
    nit_agencia: Optional[str] = None
    rnt_agencia: Optional[str] = None
    cliente_nombre: Optional[str] = None
    cliente_documento: Optional[str] = None
    pais_destino: Optional[str] = None
    ciudad_salida: Optional[str] = None
    ciudad_llegada: Optional[str] = None
    fecha_inicio_viaje: Optional[date] = None
    fecha_regreso_viaje: Optional[date] = None
    hotel_nombre: Optional[str] = None
    num_noches: Optional[int] = None
    tarifa_por_pasajero: Optional[float] = None
    tarifa_por_niño: Optional[float] = None
    abono: Optional[float] = None
    cuentas_recaudo: Optional[List[CuentasRecaudo]] = None
    pago_transferencia: Optional[bool] = None
    pago_efectivo: Optional[bool] = None
    nota_importante_contenido: Optional[str] = None
    nota_condicion_pago: Optional[str] = None
    monto_total_acumulado: Optional[float] = None   
    travelers: Optional[List[TravelerUpdate]] = None

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
        payment_status=transaction.payment_status.value,
        seller_id=transaction.seller_id,
        receipt=transaction.receipt,
        start_date=transaction.start_date,
        end_date=transaction.end_date,
        number_of_travelers=len(transaction.travelers) if transaction.travelers else 0
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

    if transaction.evidence:
        for evidence in transaction.evidence:
            evidencias = Evidence(
                evidence_file=evidence.evidence_file,
                amount=evidence.amount,
                transaction_id=new_transaction.id,
                status=EvidenceStatus.pending,
                invoice_status=EvidenceInvoiceStatus.no_facturado
            )
            db.add(evidencias)
    db.commit()

    return {"message": "Transacción creada con éxito", "transaction_id": new_transaction.id}

@router.get("/", status_code=200)
def get_all_transaction_test(db: Session = Depends(get_db)):
    transactions = (
        db.query(Transaction)
        .options(
            joinedload(Transaction.seller),
            selectinload(Transaction.travelers),
            selectinload(Transaction.evidence),
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
            "evidence": [
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
    transaction = (
        db.query(Transaction)
          .filter(Transaction.id == transaction_id)
          .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    

    # 3) Recupera la *primera* evidencia (más antigua) o la *última* (más reciente)
    #    Para la más antigua (first):
    first_evidence = (
        db.query(Evidence)
          .filter(Evidence.transaction_id == transaction_id)
          .order_by(Evidence.id.desc())
          .first()
    )
    #    Si quisieras la más reciente, usarías desc():
    # latest_evidence = (
    #     db.query(Evidence)
    #       .filter(Evidence.transaction_id == transaction_id)
    #       .order_by(desc(Evidence.id))
    #       .first()
    # )

    # 4) Actualiza el estado de esa evidencia (sólo si existe)
    if first_evidence:
        if transaction.status == "pending":
            if not status  in ["incompleta", "pending", "terminado"]:
                first_evidence.status = status
    
    # 2) Actualiza el estado de la transacción
    transaction.status = status

    # Actualizar el estado de pago si es necesario
    update_transaction_payment_status(transaction_id, db)

    db.commit()
    db.refresh(transaction)

    return {
        "message": "Estado de la transacción actualizado",
        "transaction": transaction
    }

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
    # Calcular el total pagado
    total_paid = sum(evidence.amount for evidence in evidences if evidence.status == EvidenceStatus.approved)
    
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
        "payment_status": transaction.payment_status,
        "total_paid": total_paid,
        "pending_amount": transaction.amount - total_paid,
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
                "amount": evidence.amount,
                "status": evidence.status,
                "invoice_status": evidence.invoice_status
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
    if transaction.payment_status is not None:
        existing_transaction.payment_status = transaction.payment_status.value
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
            amount=transaction.evidence.amount,
            status=EvidenceStatus.pending,
            invoice_status=EvidenceInvoiceStatus.no_facturado
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
            selectinload(Transaction.evidence),
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

                } for itinerary in transaction.itinerario
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
        amount=evidence.amount,
        status=EvidenceStatus.pending,
        invoice_status=EvidenceInvoiceStatus.no_facturado
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

@router.patch("/evidence/{evidence_id}/status", status_code=200)
def update_evidence_status(
    evidence_id: int,
    status: EvidenceStatus,
    db: Session = Depends(get_db)
):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    evidence.status = status
    db.commit()
    db.refresh(evidence)

    # Actualizar el estado de pago de la transacción si la evidencia fue aprobada
    if status == EvidenceStatus.approved:
        update_transaction_payment_status(evidence.transaction_id, db)

    return {
        "message": f"Estado de evidencia actualizado a {status}",
        "evidence": {
            "id": evidence.id,
            "transaction_id": evidence.transaction_id,
            "evidence_file": evidence.evidence_file,
            "upload_date": evidence.upload_date,
            "amount": evidence.amount,
            "status": evidence.status,
            "invoice_status": evidence.invoice_status
        }
    }

@router.patch("/evidence/{evidence_id}/invoice-status", status_code=200)
def update_evidence_invoice_status(
    evidence_id: int,
    invoice_status: EvidenceInvoiceStatus,
    db: Session = Depends(get_db)
):
    evidence = db.query(Evidence).filter(Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidencia no encontrada")

    evidence.invoice_status = invoice_status
    db.commit()
    db.refresh(evidence)

    # Mantener consistencia de pago al cambiar el estado de facturación
    update_transaction_payment_status(evidence.transaction_id, db)

    return {
        "message": f"Estado de facturación de evidencia actualizado a {invoice_status}",
        "evidence": {
            "id": evidence.id,
            "transaction_id": evidence.transaction_id,
            "evidence_file": evidence.evidence_file,
            "upload_date": evidence.upload_date,
            "amount": evidence.amount,
            "status": evidence.status,
            "invoice_status": evidence.invoice_status
        }
    }

@router.get("/evidence/filter/{status}")
def get_evidence_by_status(
    status: EvidenceStatus,
    transaction_status: Optional[TransactionStatus] = None,
    db: Session = Depends(get_db)
):
    # Construir la consulta base
    #query = db.query(Evidence).filter(Evidence.status == status)
    query = (
        db.query(Evidence, Transaction, User)
        .join(Transaction, Evidence.transaction_id == Transaction.id)
        .join(User, Transaction.seller_id == User.id)
        .filter(Evidence.status == status)
    )
    # Si se proporciona transaction_status, filtrar por transacciones con ese estado
    if transaction_status:
        query = query.filter(Transaction.status == transaction_status)

    evidences = query.all()
    if not evidences:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron evidencias con estado {status}"
        )
    
    return [
        {
            "id": evidence.id,
            "transaction_id": evidence.transaction_id,
            "evidence_file": evidence.evidence_file,
            "upload_date": evidence.upload_date,
            "amount": evidence.amount,
            "status": evidence.status,
            "invoice_status": evidence.invoice_status,
            "transaction_info":{
                "seller": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                },
            "client_name": transaction.client_name,
            "package": transaction.package,
            "start_date": transaction.start_date,
            "end_date": transaction.end_date,
            "payment_status": transaction.payment_status
            }
        }
        for evidence, transaction, user in evidences
    ]

@router.get("/evidence/filter/{status}/not-invoiced")
def get_evidence_by_status_not_invoiced(
    status: EvidenceStatus,
    transaction_status: Optional[TransactionStatus] = None,
    invoice: Optional[EvidenceInvoiceStatus] = None,
    payment_status: Optional[PaymentStatus] = None,
    db: Session = Depends(get_db)
):
    """
    Nuevo endpoint para obtener evidencias con estado específico que NO estén facturadas
    """
    # Construir la consulta base
    if not invoice:
        query = (
            db.query(Evidence, Transaction, User)
            .join(Transaction, Evidence.transaction_id == Transaction.id)
            .join(User, Transaction.seller_id == User.id)
            .filter(
                Evidence.status == status,
                Evidence.invoice_status == EvidenceInvoiceStatus.no_facturado
            )
        )
    else: 
        query = (
            db.query(Evidence, Transaction, User)
            .join(Transaction, Evidence.transaction_id == Transaction.id)
            .join(User, Transaction.seller_id == User.id)
            .filter(
                Evidence.status == status,
                Evidence.invoice_status == EvidenceInvoiceStatus.facturado
            )
        )
    # Si se proporciona transaction_status, filtrar por transacciones con ese estado
    if transaction_status:
        query = query.filter(Transaction.status == transaction_status)

    if payment_status:
        query = query.filter(Transaction.payment_status == payment_status)


    evidences = query.all()
    if not evidences:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron evidencias con estado {status} y no facturadas"
        )
    
    return [
        {
            "id": evidence.id,
            "transaction_id": evidence.transaction_id,
            "evidence_file": evidence.evidence_file,
            "upload_date": evidence.upload_date,
            "amount": evidence.amount,
            "status": evidence.status,
            "invoice_status": evidence.invoice_status,
            "transaction_info":{
                "seller": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                },
            "client_name": transaction.client_name,
            "package": transaction.package,
            "start_date": transaction.start_date,
            "end_date": transaction.end_date,
            "payment_status": transaction.payment_status
            }
        }
        for evidence, transaction, user in evidences
    ]

@router.get("/evidence/list")
def list_all_evidences(db: Session = Depends(get_db)):
    evidences = db.query(Evidence).all()
    if not evidences:
        raise HTTPException(status_code=404, detail="No se encontraron evidencias")
    return [
        {
            "id": evidence.id,
            "transaction_id": evidence.transaction_id,
            "evidence_file": evidence.evidence_file,
            "upload_date": evidence.upload_date,
            "amount": evidence.amount,
            "status": evidence.status,
            "invoice_status": evidence.invoice_status
        }
        for evidence in evidences
    ]

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
    if data.alimentacion is not None:
        travel_info.alimentacion = data.alimentacion
    if data.direccion_hotel is not None:
        travel_info.direccion_hotel = data.direccion_hotel
    if data.ciudad_destino is not None:
        travel_info.ciudad_destino = data.ciudad_destino
    if data.acomodacion is not None:
        travel_info.acomodacion = data.acomodacion
    if data.pais_destino is not None:
        travel_info.pais_destino = data.pais_destino


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
    # Obtener todas las transacciones del vendedor con sus evidencias y vendedor
    transactions = (
        db.query(Transaction)
        .filter(Transaction.seller_id == id_user)
        .options(
            selectinload(Transaction.evidence),
            selectinload(Transaction.seller)
        )
        .filter(Transaction.status == TransactionStatus.approved)
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
        # Usar el cálculo centralizado y alinear el total con la misma lógica (approved + facturado)
        computed_status = calculate_payment_status(transaction.id, db)
        if computed_status == PaymentStatus.pago_completo:
            total_paid = sum(
                evidence.amount
                for evidence in transaction.evidence
                if evidence.status == EvidenceStatus.approved
                and evidence.invoice_status == EvidenceInvoiceStatus.facturado
            )
            paid_transactions.append({
                "id": transaction.id,
                "client_name": transaction.client_name,
                "package": transaction.package,
                "amount": transaction.amount,
                "total_amount": transaction.amount,
                "total_paid": total_paid,
                "status": transaction.status,
                "payment_status": computed_status,
                "created_at": transaction.created_at,
                "seller_id": transaction.seller_id,
                "seller_name": transaction.seller.name if transaction.seller else None,
                "start_date": transaction.start_date,
                "end_date": transaction.end_date,
                "evidence": [
                    {
                        "id": evidence.id,
                        "amount": evidence.amount,
                        "evidence_file": evidence.evidence_file,
                        "upload_date": evidence.upload_date,
                        "status": evidence.status,
                        "invoice_status": evidence.invoice_status
                    } for evidence in transaction.evidence
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
            selectinload(Transaction.evidence),
            selectinload(Transaction.seller)
        )
        .filter(Transaction.status == TransactionStatus.approved)
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
        computed_status = calculate_payment_status(transaction.id, db)
        if computed_status == PaymentStatus.pago_completo:
            total_paid = sum(
                evidence.amount
                for evidence in transaction.evidence
                if evidence.status == EvidenceStatus.approved
                and evidence.invoice_status == EvidenceInvoiceStatus.facturado
            )
            paid_transactions.append({
                "id": transaction.id,
                "client_name": transaction.client_name,
                "package": transaction.package,
                "total_amount": transaction.amount,
                "total_paid": total_paid,
                "status": transaction.status,
                "payment_status": computed_status,
                "created_at": transaction.created_at,
                "seller": {
                    "id": transaction.seller.id,
                    "name": transaction.seller.name,
                    "email": transaction.seller.email
                } if transaction.seller else None,
                "evidence": [
                    {
                        "id": evidence.id,
                        "amount": evidence.amount,
                        "evidence_file": evidence.evidence_file,
                        "upload_date": evidence.upload_date,
                        "status": evidence.status,
                        "invoice_status": evidence.invoice_status
                    } for evidence in transaction.evidence
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

@router.get("/user/unpaid/{id_user}")
def get_transaction_unpaid(id_user: int, db: Session = Depends(get_db)):
    # Obtener todas las transacciones del vendedor con sus evidencias y vendedor
    transactions = (
        db.query(Transaction)
        .filter(Transaction.seller_id == id_user)
        .options(
            selectinload(Transaction.evidence),
            selectinload(Transaction.seller)
        )
        .filter(Transaction.status == TransactionStatus.approved)
        .all()
    )
    
    if not transactions:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron transacciones para este vendedor"
        )
    
    # Filtrar las transacciones que NO están completamente pagadas
    unpaid_transactions = []
    for transaction in transactions:
        # Calcular el total solo con evidencias aprobadas
        total_paid = sum(evidence.amount for evidence in transaction.evidence if evidence.status == EvidenceStatus.approved)
        if total_paid < transaction.amount:  # < para identificar las que faltan por pagar
            pending_amount = transaction.amount - total_paid
            unpaid_transactions.append({
                "id": transaction.id,
                "client_name": transaction.client_name,
                "package": transaction.package,
                "amount": transaction.amount,
                "total_amount": transaction.amount,
                "total_paid": total_paid,
                "pending_amount": pending_amount,
                "status": transaction.status,
                "payment_status": transaction.payment_status,
                "created_at": transaction.created_at,
                "seller_id": transaction.seller_id,
                "seller_name": transaction.seller.name if transaction.seller else None,
                "start_date": transaction.start_date,
                "end_date": transaction.end_date,
                "evidence": [
                    {
                        "id": evidence.id,
                        "amount": evidence.amount,
                        "evidence_file": evidence.evidence_file,
                        "upload_date": evidence.upload_date,
                        "status": evidence.status,
                        "invoice_status": evidence.invoice_status
                    } for evidence in transaction.evidence
                ]
            })
    
    return {
        "seller_id": id_user,
        "total_unpaid_transactions": len(unpaid_transactions),
        "transactions": unpaid_transactions
    }

@router.get("/admin/unpaid-transactions")
def get_all_unpaid_transactions(db: Session = Depends(get_db)):
    # Obtener todas las transacciones con sus evidencias y vendedor
    transactions = (
        db.query(Transaction)
        .options(
            selectinload(Transaction.evidence),
            selectinload(Transaction.seller),
        )
        .filter(Transaction.status == TransactionStatus.approved)
        .all()
    )
    
    if not transactions:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron transacciones en el sistema"
        )
    
    # Filtrar las transacciones que NO están completamente pagadas
    unpaid_transactions = []
    for transaction in transactions:
        total_paid = sum(evidence.amount for evidence in transaction.evidence if evidence.status == EvidenceStatus.approved)
        if total_paid < transaction.amount:  # < para identificar las que faltan por pagar
            pending_amount = transaction.amount - total_paid
            unpaid_transactions.append({
                "id": transaction.id,
                "client_name": transaction.client_name,
                "package": transaction.package,
                "total_amount": transaction.amount,
                "total_paid": total_paid,
                "pending_amount": pending_amount,
                "status": transaction.status,
                "payment_status": transaction.payment_status,
                "created_at": transaction.created_at,
                "seller": {
                    "id": transaction.seller.id,
                    "name": transaction.seller.name,
                    "email": transaction.seller.email
                } if transaction.seller else None,
                "evidence": [
                    {
                        "id": evidence.id,
                        "amount": evidence.amount,
                        "evidence_file": evidence.evidence_file,
                        "upload_date": evidence.upload_date,
                        "status": evidence.status,
                        "invoice_status": evidence.invoice_status
                    } for evidence in transaction.evidence
                ]
            })
    
    # Calcular estadísticas
    total_amount = sum(t["total_amount"] for t in unpaid_transactions)
    total_paid = sum(t["total_paid"] for t in unpaid_transactions)
    total_pending = sum(t["pending_amount"] for t in unpaid_transactions)
    
    return {
        "total_unpaid_transactions": len(unpaid_transactions),
        "total_amount": total_amount,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "transactions": unpaid_transactions
    }

# Endpoints para la factura
from datetime import date

def serialize_date(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    return obj

@router.post("/{transaction_id}/factura", status_code=201)
def create_factura(transaction_id: int, factura: FacturaCreate, db: Session = Depends(get_db)):
    # Verificar si la transacción existe
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Obtener la última factura para calcular el monto total acumulado
    facturas_previas = (
        db.query(Factura)
        .filter(Factura.transaction_id == transaction_id)
        .all()
    )
    
    # Calcular el monto total acumulado sumando los abonos de facturas anteriores
    monto_total_acumulado = sum(f.abono for f in facturas_previas) + factura.abono

    # Convertir las cuentas de recaudo a diccionarios
    cuentas_recaudo_dict = [cuenta.dict() for cuenta in factura.cuentas_recaudo] if factura.cuentas_recaudo else None

    # Convertir los travelers con serialización de fechas
    travelers_dict = None
    if factura.travelers:
        travelers_dict = []
        for traveler in factura.travelers:
            traveler_data = traveler.dict()
            traveler_data['date_birth'] = serialize_date(traveler_data['date_birth'])
            travelers_dict.append(traveler_data)

    # Crear nueva factura
    new_factura = Factura(
        transaction_id=transaction_id,
        reserva_numero=factura.reserva_numero,
        fecha_compra=serialize_date(factura.fecha_compra),
        agencia_nombre=factura.agencia_nombre,
        nit_agencia=factura.nit_agencia,
        rnt_agencia=factura.rnt_agencia,
        cliente_nombre=factura.cliente_nombre,
        cliente_documento=factura.cliente_documento,
        pais_destino=factura.pais_destino,
        ciudad_salida=factura.ciudad_salida,
        ciudad_llegada=factura.ciudad_llegada,
        fecha_inicio_viaje=serialize_date(factura.fecha_inicio_viaje),
        fecha_regreso_viaje=serialize_date(factura.fecha_regreso_viaje),
        hotel_nombre=factura.hotel_nombre,
        num_noches=factura.num_noches,
        tarifa_por_pasajero=factura.tarifa_por_pasajero,
        tarifa_por_niño=factura.tarifa_por_niño,
        abono=factura.abono,
        cuentas_recaudo=cuentas_recaudo_dict,
        pago_transferencia=factura.pago_transferencia,
        pago_efectivo=factura.pago_efectivo,
        nota_importante_contenido=factura.nota_importante_contenido,
        nota_condicion_pago=factura.nota_condicion_pago,
        monto_total_acumulado=monto_total_acumulado,
        travelers=travelers_dict
    )
    
    db.add(new_factura)
    db.commit()
    db.refresh(new_factura)
    
    return {
        "message": "Factura creada con éxito",
        "factura": {
            **new_factura.__dict__,
            "abono_actual": new_factura.abono,
            "monto_total_acumulado": new_factura.monto_total_acumulado,
            "saldo_pendiente": transaction.amount - monto_total_acumulado
        }
    }

@router.get("/{transaction_id}/factura")
def get_facturas_by_transaction(transaction_id: int, db: Session = Depends(get_db)):
    # Verificar si la transacción existe
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Buscar todas las facturas de la transacción
    facturas = (
        db.query(Factura)
        .filter(Factura.transaction_id == transaction_id)
        .order_by(Factura.fecha_compra)
        .all()
    )

    if not facturas:
        raise HTTPException(status_code=404, detail="No se encontraron facturas para esta transacción")
    
    # Preparar la respuesta con los cálculos necesarios
    facturas_response = []
    for factura in facturas:
        facturas_response.append({
            **factura.__dict__,
            "monto_total_acumulado": factura.monto_total_acumulado,
            "saldo_pendiente": transaction.amount - factura.monto_total_acumulado
        })
    
    return {
        "transaction_id": transaction_id,
        "monto_total_transaccion": transaction.amount,
        "facturas": facturas_response
    }

@router.patch("/{transaction_id}/factura", status_code=200)
def update_factura(transaction_id: int, factura_data: FacturaUpdate, db: Session = Depends(get_db)):
    # Verificar si la transacción existe
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    # Buscar la factura
    factura = db.query(Factura).filter(Factura.transaction_id == transaction_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Actualizar solo los campos que no son None
    for field, value in factura_data.dict(exclude_unset=True).items():
        setattr(factura, field, value)
    
    db.commit()
    db.refresh(factura)
    
    return {"message": "Factura actualizada con éxito", "factura": factura}

def calculate_payment_status(transaction_id: int, db: Session) -> PaymentStatus:
    """
    Calcula el estado de pago de una transacción basado en las evidencias aprobadas
    """
    # Obtener todas las evidencias aprobadas de la transacción
    approved_evidences = (
        db.query(Evidence)
        .filter(
            Evidence.transaction_id == transaction_id,
            Evidence.status == EvidenceStatus.approved,
            Evidence.invoice_status == EvidenceInvoiceStatus.facturado
        )
        .all()
    )
    
    # Calcular el total pagado
    total_paid = sum(evidence.amount for evidence in approved_evidences)
    
    # Obtener el monto total de la transacción
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return PaymentStatus.pago_incompleto
    
    # Determinar si el pago está completo
    if total_paid >= transaction.amount:
        return PaymentStatus.pago_completo
    else:
        return PaymentStatus.pago_incompleto

def update_transaction_payment_status(transaction_id: int, db: Session):
    """
    Actualiza el estado de pago de una transacción
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        new_payment_status = calculate_payment_status(transaction_id, db)
        transaction.payment_status = new_payment_status
        db.commit()


@router.get("/manageFlies/by-seller/{seller_id}")
def get_manage_flies_by_seller(seller_id: int, current_date: str, db: Session = Depends(get_db)):
    """
    Obtiene todas las transacciones filtradas por seller_id y status aprobado,
    agrupadas por estado del viaje basado en las fechas.
    
    Args:
        seller_id: ID del vendedor
        current_date: Fecha actual en formato YYYY-MM-DD
    
    Returns:
        Dict con arrays de transacciones agrupadas por estado
    """
    from datetime import datetime, timedelta
    
    try:
        current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
    
    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.seller_id == seller_id,
            Transaction.status == TransactionStatus.approved
        )
        .all()
    )
    
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No se encontraron transacciones para el seller_id {seller_id}")
    
    # Inicializar grupos
    groups = {
        "proximos": [],
        "por_comenzar": [],
        "a_punto": [],
        "en_viaje": [],
        "regresando": [],
        "finalizados": []
    }
    
    for transaction in transactions:
        if not transaction.start_date or not transaction.end_date:
            continue  # Saltar transacciones sin fechas
            
        start_date = transaction.start_date
        end_date = transaction.end_date
        
        # Convertir a date para comparaciones más fáciles
        current_date_only = current_date_obj.date()
        start_date_only = start_date.date() if isinstance(start_date, datetime) else start_date
        end_date_only = end_date.date() if isinstance(end_date, datetime) else end_date
        
        # Calcular días que faltan para el viaje
        days_to_start = (start_date_only - current_date_only).days
        days_leave = max(0, days_to_start)  # No puede ser negativo
        
        # Crear objeto de transacción simplificado
        transaction_data = {
            "id": transaction.id,
            "client_name": transaction.client_name,
            "package": transaction.package,
            "start_date": start_date_only.isoformat(),
            "daysLeave": days_leave,
            "amount": transaction.amount,
            "payment_status": 0 if transaction.payment_status == "pago_incompleto" else 1
        }
        
        # Clasificar en grupos
        if current_date_only < start_date_only:
            # Antes del viaje
            if days_to_start > 30:  # Más de 1 mes
                groups["proximos"].append(transaction_data)
            elif days_to_start > 3:  # Entre 1 mes y 3 días
                groups["por_comenzar"].append(transaction_data)
            else:  # 3 días o menos
                groups["a_punto"].append(transaction_data)
        elif current_date_only == end_date_only:
            # El día que termina el viaje
            groups["regresando"].append(transaction_data)
        elif start_date_only <= current_date_only <= end_date_only:
            # Durante el viaje
            groups["en_viaje"].append(transaction_data)
        else:
            # Después del viaje
            groups["finalizados"].append(transaction_data)
    
    return groups


@router.get("/ingresos-totales/")
def get_ingresos_totales(
    fecha_inicio: str = None,  # YYYY-MM-DD
    fecha_fin: str = None,     # YYYY-MM-DD
    user_id: int = None,       # ID del usuario para filtrar (opcional)
    db: Session = Depends(get_db)
):
    """
    Obtiene el total de ingresos por rango de fechas y usuario opcional.
    
    Args:
        fecha_inicio: Fecha de inicio en formato YYYY-MM-DD (opcional)
        fecha_fin: Fecha de fin en formato YYYY-MM-DD (opcional)
        user_id: ID del usuario para filtrar (opcional)
    
    Returns:
        Dict con el total de ingresos, ganancias y estadísticas de ventas
    """
    from datetime import datetime, date
    from sqlalchemy import and_
    
    # Validar usuario si se especifica
    usuario_info = None
    if user_id is not None:
        usuario = db.query(User).filter(User.id == user_id).first()
        if not usuario:
            raise HTTPException(
                status_code=404,
                detail=f"Usuario con ID {user_id} no encontrado"
            )
        usuario_info = {
            'id': usuario.id,
            'email': usuario.email,
            'nombre': getattr(usuario, 'name', 'N/A')
        }
    
    # Construir la consulta base
    if user_id is not None:
        # Filtrar por usuario específico
        query = db.query(Evidence).join(Transaction).filter(
            and_(
                Evidence.status == EvidenceStatus.approved,
                Transaction.seller_id == user_id
            )
        )
    else:
        # Sin filtro de usuario
        query = db.query(Evidence).filter(Evidence.status == EvidenceStatus.approved)
    
    # Si no se especifican fechas, obtener histórico completo
    if not fecha_inicio and not fecha_fin:
        if user_id is not None:
            titulo_periodo = f"Histórico Completo - Usuario: {usuario_info['email']}"
        else:
            titulo_periodo = "Histórico Completo"
        fecha_inicio_obj = None
        fecha_fin_obj = None
        
    else:
        # Validar que ambas fechas estén presentes si se especifica una
        if fecha_inicio and not fecha_fin:
            raise HTTPException(
                status_code=400,
                detail="Si especifica fecha_inicio, debe especificar también fecha_fin"
            )
        if fecha_fin and not fecha_inicio:
            raise HTTPException(
                status_code=400,
                detail="Si especifica fecha_fin, debe especificar también fecha_inicio"
            )
        
        # Convertir fechas
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )
        
        # Validar que fecha_inicio <= fecha_fin
        if fecha_inicio_obj > fecha_fin_obj:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio debe ser menor o igual a la fecha de fin"
            )
        
        # Aplicar filtro de fechas
        query = query.filter(
            and_(
                func.date(Evidence.upload_date) >= fecha_inicio_obj,
                func.date(Evidence.upload_date) <= fecha_fin_obj
            )
        )
        
        if user_id is not None:
            titulo_periodo = f"Período: {fecha_inicio} a {fecha_fin} - Usuario: {usuario_info['email']}"
        else:
            titulo_periodo = f"Período: {fecha_inicio} a {fecha_fin}"
    
    # Ejecutar la consulta de evidencias
    evidencias = query.all()
    
    # Calcular el total de ingresos
    total_ingresos = sum(evidence.amount for evidence in evidencias) if evidencias else 0.0
    
    # Calcular ganancias (15% de ingresos)
    total_ganancias = total_ingresos * 0.15
    
    # Calcular comisión (5% de ingresos)
    total_comision = total_ingresos * 0.05
    
    # Obtener estadísticas de transacciones por estado
    # Construir consulta base para transacciones
    trans_query = db.query(Transaction)
    
    # Aplicar filtro de usuario si se especificó
    if user_id is not None:
        trans_query = trans_query.filter(Transaction.seller_id == user_id)
    
    # Aplicar filtro de fechas si se especificó
    if fecha_inicio and fecha_fin:
        trans_query = trans_query.filter(
            and_(
                func.date(Transaction.created_at) >= fecha_inicio_obj,
                func.date(Transaction.created_at) <= fecha_fin_obj
            )
        )
    
    # Obtener todas las transacciones del período
    transacciones = trans_query.all()
    
    # Contar por estado
    total_ventas = len(transacciones)
    ventas_pending = len([t for t in transacciones if t.status == TransactionStatus.pending])
    ventas_approved = len([t for t in transacciones if t.status == TransactionStatus.approved])
    ventas_incompleta = len([t for t in transacciones if t.status == TransactionStatus.incompleta])
    ventas_rejected = len([t for t in transacciones if t.status == TransactionStatus.rejected])
    ventas_terminado = len([t for t in transacciones if t.status == TransactionStatus.terminado])

    response_data = {
        "titulo_periodo": titulo_periodo,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_ingresos": total_ingresos,
        "total_ganancias": total_ganancias,
        "total_comision": total_comision,
        "cantidad_evidencias": len(evidencias),
        "estadisticas_ventas": {
            "total_ventas": total_ventas,
            "pending": ventas_pending,
            "approved": ventas_approved,
            "incompleta": ventas_incompleta,
            "rejected": ventas_rejected,
            "terminado": ventas_terminado
        }
    }
    
    # Agregar información del usuario si se especificó
    if usuario_info is not None:
        response_data["usuario"] = usuario_info
    
    return response_data

@router.get("/ingresos-totales-usuario/")
def get_ingresos_totales_usuario(
    user_id: int,
    fecha_inicio: str = None,  # YYYY-MM-DD
    fecha_fin: str = None,     # YYYY-MM-DD
    db: Session = Depends(get_db)
):
    """
    Obtiene el total de ingresos por usuario y rango de fechas.
    Suma todos los amounts de las evidencias aprobadas del usuario en ese rango.
    Si no se especifica rango de fechas, devuelve el histórico completo del usuario.

    Args:
        user_id: ID del usuario (seller) para filtrar
        fecha_inicio: Fecha de inicio en formato YYYY-MM-DD (opcional)
        fecha_fin: Fecha de fin en formato YYYY-MM-DD (opcional)

    Returns:
        Dict con el total de ingresos, ganancias, comisión y estadísticas de ventas del usuario
    """
    from datetime import datetime, date
    from sqlalchemy import and_

    # Verificar que el usuario existe
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    # Construir la consulta base para evidencias del usuario
    query = db.query(Evidence).join(Transaction).filter(
        and_(
            Evidence.status == EvidenceStatus.approved,
            Transaction.seller_id == user_id
        )
    )

    # Si no se especifican fechas, obtener histórico completo del usuario
    if not fecha_inicio and not fecha_fin:
        titulo_periodo = f"Histórico Completo - Usuario: {usuario.email}"
        fecha_inicio_obj = None
        fecha_fin_obj = None

    else:
        # Validar que ambas fechas estén presentes si se especifica una
        if fecha_inicio and not fecha_fin:
            raise HTTPException(
                status_code=400,
                detail="Si especifica fecha_inicio, debe especificar también fecha_fin"
            )
        if fecha_fin and not fecha_inicio:
            raise HTTPException(
                status_code=400,
                detail="Si especifica fecha_fin, debe especificar también fecha_inicio"
            )

        # Convertir fechas
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Formato de fecha inválido. Use YYYY-MM-DD"
            )

        # Validar que fecha_inicio <= fecha_fin
        if fecha_inicio_obj > fecha_fin_obj:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio debe ser menor o igual a la fecha de fin"
            )

        # Aplicar filtro de fechas a evidencias
        query = query.filter(
            and_(
                func.date(Evidence.upload_date) >= fecha_inicio_obj,
                func.date(Evidence.upload_date) <= fecha_fin_obj
            )
        )

        titulo_periodo = f"Período: {fecha_inicio} a {fecha_fin} - Usuario: {usuario.email}"

    # Ejecutar la consulta de evidencias
    evidencias = query.all()

    # Calcular el total de ingresos
    total_ingresos = sum(evidence.amount for evidence in evidencias) if evidencias else 0.0

    # Calcular ganancias (15% de ingresos)
    total_ganancias = total_ingresos * 0.15

    # Calcular comisión (5% de ingresos)
    total_comision = total_ingresos * 0.05

    # Obtener estadísticas de transacciones por estado del usuario
    # Construir consulta base para transacciones del usuario
    trans_query = db.query(Transaction).filter(Transaction.seller_id == user_id)

    # Aplicar filtro de fechas si se especificó
    if fecha_inicio and fecha_fin:
        trans_query = trans_query.filter(
            and_(
                func.date(Transaction.created_at) >= fecha_inicio_obj,
                func.date(Transaction.created_at) <= fecha_fin_obj
            )
        )

    # Obtener todas las transacciones del usuario en el período
    transacciones = trans_query.all()

    # Contar por estado
    total_ventas = len(transacciones)
    ventas_pending = len([t for t in transacciones if t.status == TransactionStatus.pending])
    ventas_approved = len([t for t in transacciones if t.status == TransactionStatus.approved])
    ventas_incompleta = len([t for t in transacciones if t.status == TransactionStatus.incompleta])
    ventas_rejected = len([t for t in transacciones if t.status == TransactionStatus.rejected])
    ventas_terminado = len([t for t in transacciones if t.status == TransactionStatus.terminado])

    return {
        "titulo_periodo": titulo_periodo,
        "user_id": user_id,
        "usuario_email": usuario.email,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total_ingresos": total_ingresos,
        "total_ganancias": total_ganancias,
        "total_comision": total_comision,
        "cantidad_evidencias": len(evidencias),
        "estadisticas_ventas": {
            "total_ventas": total_ventas,
            "pending": ventas_pending,
            "approved": ventas_approved,
            "incompleta": ventas_incompleta,
            "rejected": ventas_rejected,
            "terminado": ventas_terminado
        }
    }

@router.get("/ingresos-totales-mensual/")
def get_ingresos_totales_mensual(
    fecha_inicio: str,  # YYYY-MM-DD
    fecha_fin: str,     # YYYY-MM-DD
    db: Session = Depends(get_db)
):
    """
    Obtiene el total de ingresos desglosado por mes en un rango de fechas.
    Devuelve la información de cada mes y el acumulado total.

    Args:
        fecha_inicio: Fecha de inicio en formato YYYY-MM-DD
        fecha_fin: Fecha de fin en formato YYYY-MM-DD

    Returns:
        Dict con ingresos, ganancias y comisiones por mes y total acumulado
    """
    from datetime import datetime, date, timedelta
    from sqlalchemy import and_, extract
    from calendar import month_name
    import locale

    # Configurar locale para nombres de meses en español
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
        except:
            pass  # Si no se puede configurar, usaremos nombres en inglés

    # Validar fechas
    try:
        fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido. Use YYYY-MM-DD"
        )

    # Validar que fecha_inicio <= fecha_fin
    if fecha_inicio_obj > fecha_fin_obj:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio debe ser menor o igual a la fecha de fin"
        )

    # Generar lista de meses en el rango
    meses = []
    current_date = fecha_inicio_obj.replace(day=1)  # Primer día del mes
    
    while current_date <= fecha_fin_obj:
        # Obtener el último día del mes actual
        if current_date.month == 12:
            next_month = current_date.replace(year=current_date.year + 1, month=1, day=1)
        else:
            next_month = current_date.replace(month=current_date.month + 1, day=1)
        
        ultimo_dia_mes = next_month - timedelta(days=1)
        
        # Ajustar el rango del mes para que no exceda las fechas especificadas
        mes_inicio = max(current_date, fecha_inicio_obj)
        mes_fin = min(ultimo_dia_mes, fecha_fin_obj)
        
        meses.append({
            'año': current_date.year,
            'mes': current_date.month,
            'nombre_mes': current_date.strftime('%B').capitalize(),
            'fecha_inicio': mes_inicio,
            'fecha_fin': mes_fin
        })
        
        # Avanzar al siguiente mes
        current_date = next_month

    # Obtener datos por mes
    datos_mensuales = []
    total_acumulado = {
        'ingresos': 0.0,
        'ganancias': 0.0,
        'comision': 0.0,
        'cantidad_evidencias': 0,
        'total_ventas': 0,
        'ventas_pending': 0,
        'ventas_approved': 0,
        'ventas_incompleta': 0,
        'ventas_rejected': 0,
        'ventas_terminado': 0
    }

    for mes_info in meses:
        # Consultar evidencias del mes
        evidencias_mes = db.query(Evidence).filter(
            and_(
                Evidence.status == EvidenceStatus.approved,
                func.date(Evidence.upload_date) >= mes_info['fecha_inicio'],
                func.date(Evidence.upload_date) <= mes_info['fecha_fin']
            )
        ).all()

        # Calcular ingresos del mes
        ingresos_mes = sum(evidence.amount for evidence in evidencias_mes) if evidencias_mes else 0.0
        ganancias_mes = ingresos_mes * 0.15
        comision_mes = ingresos_mes * 0.05

        # Consultar transacciones del mes
        transacciones_mes = db.query(Transaction).filter(
            and_(
                func.date(Transaction.created_at) >= mes_info['fecha_inicio'],
                func.date(Transaction.created_at) <= mes_info['fecha_fin']
            )
        ).all()

        # Contar transacciones por estado
        total_ventas_mes = len(transacciones_mes)
        ventas_pending_mes = len([t for t in transacciones_mes if t.status == TransactionStatus.pending])
        ventas_approved_mes = len([t for t in transacciones_mes if t.status == TransactionStatus.approved])
        ventas_incompleta_mes = len([t for t in transacciones_mes if t.status == TransactionStatus.incompleta])
        ventas_rejected_mes = len([t for t in transacciones_mes if t.status == TransactionStatus.rejected])
        ventas_terminado_mes = len([t for t in transacciones_mes if t.status == TransactionStatus.terminado])

        # Datos del mes
        datos_mes = {
            'año': mes_info['año'],
            'mes': mes_info['mes'],
            'nombre_mes': mes_info['nombre_mes'],
            'fecha_inicio': mes_info['fecha_inicio'].isoformat(),
            'fecha_fin': mes_info['fecha_fin'].isoformat(),
            'ingresos': ingresos_mes,
            'ganancias': ganancias_mes,
            'comision': comision_mes,
            'cantidad_evidencias': len(evidencias_mes),
            'estadisticas_ventas': {
                'total_ventas': total_ventas_mes,
                'pending': ventas_pending_mes,
                'approved': ventas_approved_mes,
                'incompleta': ventas_incompleta_mes,
                'rejected': ventas_rejected_mes,
                'terminado': ventas_terminado_mes
            }
        }

        datos_mensuales.append(datos_mes)

        # Acumular totales
        total_acumulado['ingresos'] += ingresos_mes
        total_acumulado['ganancias'] += ganancias_mes
        total_acumulado['comision'] += comision_mes
        total_acumulado['cantidad_evidencias'] += len(evidencias_mes)
        total_acumulado['total_ventas'] += total_ventas_mes
        total_acumulado['ventas_pending'] += ventas_pending_mes
        total_acumulado['ventas_approved'] += ventas_approved_mes
        total_acumulado['ventas_incompleta'] += ventas_incompleta_mes
        total_acumulado['ventas_rejected'] += ventas_rejected_mes
        total_acumulado['ventas_terminado'] += ventas_terminado_mes

    return {
        "rango_fechas": {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        },
        "cantidad_meses": len(meses),
        "datos_mensuales": datos_mensuales,
        "total_acumulado": {
            "ingresos": total_acumulado['ingresos'],
            "ganancias": total_acumulado['ganancias'],
            "comision": total_acumulado['comision'],
            "cantidad_evidencias": total_acumulado['cantidad_evidencias'],
            "estadisticas_ventas": {
                "total_ventas": total_acumulado['total_ventas'],
                "pending": total_acumulado['ventas_pending'],
                "approved": total_acumulado['ventas_approved'],
                "incompleta": total_acumulado['ventas_incompleta'],
                "rejected": total_acumulado['ventas_rejected'],
                "terminado": total_acumulado['ventas_terminado']
            }
        }
    }

@router.get("/comisiones-por-usuario/")
def get_comisiones_por_usuario(
    fecha_inicio: str,  # YYYY-MM-DD
    fecha_fin: str,     # YYYY-MM-DD
    db: Session = Depends(get_db)
):
    """
    Obtiene las comisiones de cada usuario (seller) en un rango de fechas.
    Calcula la comisión (5% de ingresos) por cada vendedor.

    Args:
        fecha_inicio: Fecha de inicio en formato YYYY-MM-DD
        fecha_fin: Fecha de fin en formato YYYY-MM-DD

    Returns:
        Dict con comisiones por usuario y total general
    """
    from datetime import datetime, date
    from sqlalchemy import and_, func

    # Validar fechas
    try:
        fecha_inicio_obj = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de fecha inválido. Use YYYY-MM-DD"
        )

    # Validar que fecha_inicio <= fecha_fin
    if fecha_inicio_obj > fecha_fin_obj:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio debe ser menor o igual a la fecha de fin"
        )

    # Obtener todos los usuarios (sellers) que tienen transacciones en el período
    sellers_con_transacciones = db.query(Transaction.seller_id).filter(
        and_(
            func.date(Transaction.created_at) >= fecha_inicio_obj,
            func.date(Transaction.created_at) <= fecha_fin_obj
        )
    ).distinct().all()

    # Extraer los IDs de sellers
    seller_ids = [seller[0] for seller in sellers_con_transacciones]

    # Si no hay sellers con transacciones en el período
    if not seller_ids:
        return {
            "rango_fechas": {
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin
            },
            "cantidad_usuarios": 0,
            "usuarios": [],
            "total_general": {
                "ingresos": 0.0,
                "ganancias": 0.0,
                "comision": 0.0,
                "cantidad_evidencias": 0,
                "total_ventas": 0
            }
        }

    # Obtener información de los usuarios
    usuarios = db.query(User).filter(User.id.in_(seller_ids)).all()
    usuarios_dict = {user.id: user for user in usuarios}

    # Calcular comisiones por usuario
    datos_usuarios = []
    total_general = {
        'ingresos': 0.0,
        'ganancias': 0.0,
        'comision': 0.0,
        'cantidad_evidencias': 0,
        'total_ventas': 0
    }

    for seller_id in seller_ids:
        # Obtener evidencias aprobadas del usuario en el período
        evidencias_usuario = db.query(Evidence).join(Transaction).filter(
            and_(
                Evidence.status == EvidenceStatus.approved,
                Transaction.seller_id == seller_id,
                func.date(Evidence.upload_date) >= fecha_inicio_obj,
                func.date(Evidence.upload_date) <= fecha_fin_obj
            )
        ).all()

        # Calcular ingresos del usuario
        ingresos_usuario = sum(evidence.amount for evidence in evidencias_usuario) if evidencias_usuario else 0.0
        ganancias_usuario = ingresos_usuario * 0.15
        comision_usuario = ingresos_usuario * 0.05

        # Obtener transacciones del usuario en el período
        transacciones_usuario = db.query(Transaction).filter(
            and_(
                Transaction.seller_id == seller_id,
                func.date(Transaction.created_at) >= fecha_inicio_obj,
                func.date(Transaction.created_at) <= fecha_fin_obj
            )
        ).all()

        # Contar transacciones por estado
        total_ventas_usuario = len(transacciones_usuario)
        ventas_pending = len([t for t in transacciones_usuario if t.status == TransactionStatus.pending])
        ventas_approved = len([t for t in transacciones_usuario if t.status == TransactionStatus.approved])
        ventas_incompleta = len([t for t in transacciones_usuario if t.status == TransactionStatus.incompleta])
        ventas_rejected = len([t for t in transacciones_usuario if t.status == TransactionStatus.rejected])
        ventas_terminado = len([t for t in transacciones_usuario if t.status == TransactionStatus.terminado])

        # Obtener información del usuario
        usuario = usuarios_dict.get(seller_id)
        email_usuario = usuario.email if usuario else "Usuario no encontrado"
        nombre_usuario = getattr(usuario, 'name', 'N/A') if usuario else "N/A"

        # Datos del usuario
        datos_usuario = {
            'user_id': seller_id,
            'email': email_usuario,
            'nombre': nombre_usuario,
            'ingresos': ingresos_usuario,
            'ganancias': ganancias_usuario,
            'comision': comision_usuario,
            'cantidad_evidencias': len(evidencias_usuario),
            'estadisticas_ventas': {
                'total_ventas': total_ventas_usuario,
                'pending': ventas_pending,
                'approved': ventas_approved,
                'incompleta': ventas_incompleta,
                'rejected': ventas_rejected,
                'terminado': ventas_terminado
            }
        }

        datos_usuarios.append(datos_usuario)

        # Acumular totales generales
        total_general['ingresos'] += ingresos_usuario
        total_general['ganancias'] += ganancias_usuario
        total_general['comision'] += comision_usuario
        total_general['cantidad_evidencias'] += len(evidencias_usuario)
        total_general['total_ventas'] += total_ventas_usuario

    # Ordenar usuarios por comisión (de mayor a menor)
    datos_usuarios.sort(key=lambda x: x['comision'], reverse=True)

    return {
        "rango_fechas": {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        },
        "cantidad_usuarios": len(datos_usuarios),
        "usuarios": datos_usuarios,
        "total_general": {
            "ingresos": total_general['ingresos'],
            "ganancias": total_general['ganancias'],
            "comision": total_general['comision'],
            "cantidad_evidencias": total_general['cantidad_evidencias'],
            "total_ventas": total_general['total_ventas']
        }
    }