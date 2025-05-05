from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.event import Event
from app.db.database import get_db

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events
