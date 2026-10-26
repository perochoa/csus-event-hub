from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from app.db import get_session
from app.models import RSVP, Event, Member, RSVPCreate, RSVPRead

router = APIRouter(prefix="/rsvps", tags=["rsvps"])


@router.post("", response_model=RSVPRead, status_code=201)
def create_rsvp(payload: RSVPCreate, session: Session = Depends(get_session)):
    event = session.get(Event, payload.event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    member = session.get(Member, payload.member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    taken = session.exec(
        select(func.count()).select_from(RSVP).where(RSVP.event_id == event.id)
    ).one()
    if taken > event.capacity:
        raise HTTPException(status_code=409, detail="Event is full")

    rsvp = RSVP(member_id=member.id, event_id=event.id)
    session.add(rsvp)
    session.commit()
    session.refresh(rsvp)
    return rsvp


@router.get("", response_model=list[RSVPRead])
def list_rsvps(event_id: int | None = None, session: Session = Depends(get_session)):
    query = select(RSVP)
    if event_id is not None:
        query = query.where(RSVP.event_id == event_id)
    return session.exec(query.order_by(RSVP.created_at)).all()


@router.get("/{rsvp_id}", response_model=RSVPRead)
def get_rsvp(rsvp_id: int, session: Session = Depends(get_session)):
    rsvp = session.get(RSVP, rsvp_id)
    if rsvp is None:
        raise HTTPException(status_code=404, detail="RSVP not found")
    return rsvp


@router.post("/{rsvp_id}/check-in", response_model=RSVPRead)
def check_in(rsvp_id: int, session: Session = Depends(get_session)):
    rsvp = session.get(RSVP, rsvp_id)
    if rsvp is None:
        raise HTTPException(status_code=404, detail="RSVP not found")
    rsvp.checked_in = True
    session.add(rsvp)
    session.commit()
    session.refresh(rsvp)
    return rsvp
