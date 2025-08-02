from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.transaction import CuentasRecaudo
from app.db.database import get_db
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/cuentas-recaudo", tags=["cuentas-recaudo"])

class CuentasRecaudoCreate(BaseModel):
    # Aquí puedes agregar más campos según necesites
    banco: str
    numero_cuenta: str
    tipo_cuenta: str
    titular: str

class CuentasRecaudoResponse(BaseModel):
    id: int
    banco: str
    numero_cuenta: str
    tipo_cuenta: str
    titular: str

    class Config:
        from_attributes = True

@router.post("/", response_model=CuentasRecaudoResponse, status_code=201)
def create_cuenta_recaudo(cuenta: CuentasRecaudoCreate, db: Session = Depends(get_db)):
    new_cuenta = CuentasRecaudo(
        banco=cuenta.banco,
        numero_cuenta=cuenta.numero_cuenta,
        tipo_cuenta=cuenta.tipo_cuenta,
        titular=cuenta.titular
    )
    db.add(new_cuenta)
    db.commit()
    db.refresh(new_cuenta)
    return new_cuenta

@router.get("/", response_model=List[CuentasRecaudoResponse])
def get_cuentas_recaudo(db: Session = Depends(get_db)):
    cuentas = db.query(CuentasRecaudo).all()
    return cuentas

@router.delete("/{cuenta_id}", status_code=204)
def delete_cuenta_recaudo(cuenta_id: int, db: Session = Depends(get_db)):
    cuenta = db.query(CuentasRecaudo).filter(CuentasRecaudo.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta de recaudo no encontrada")
    
    db.delete(cuenta)
    db.commit()
    return {"message": "Cuenta de recaudo eliminada con éxito"}