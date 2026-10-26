from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.models import EventCreate, EventRead, EventUpdate
from app.services import events as event_service

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventRead, status_code=201)
def create_event(payload: EventCreate, session: Session = Depends(get_session)):
    return event_service.create_event(session, payload)


@router.get("", response_model=list[EventRead])
def list_events(session: Session = Depends(get_session)):
    return event_service.list_events(session)


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, session: Session = Depends(get_session)):
    return event_service.get_event(session, event_id)


@router.patch("/{event_id}", response_model=EventRead)
def update_event(event_id: int, payload: EventUpdate, session: Session = Depends(get_session)):
    return event_service.update_event(session, event_id, payload)


@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    event_service.delete_event(session, event_id)
