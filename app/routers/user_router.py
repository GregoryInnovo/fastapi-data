from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User, hash_password
from app.db.database import get_db
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/users", tags=["users"])

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserUpdate(BaseModel):
    name: str = None
    email: EmailStr = None
    role: str = None
    password: str = None  # Permitir la actualización de la contraseña
    
@router.post("/", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Crear un nuevo usuario
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),  # Hashear la contraseña
        role=user.role  # Asignar el rol
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario creado con éxito", "user": new_user}

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.patch("/{user_id}", status_code=200)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar solo los campos que se proporcionan
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.password is not None:
        user.password = hash_password(user_data.password)  # Hashear la nueva contraseña

    db.commit()
    db.refresh(user)
    return {"message": "Usuario actualizado con éxito", "user": user}


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado con éxito"}
