from datetime import UTC, datetime

from fastapi import HTTPException
from sqlmodel import Session, select

from app.config import CLUB_TIMEZONE
from app.models import Event, EventCreate, EventUpdate


def _to_club_time(value: datetime) -> datetime:
    """Normalize a timestamp to club wall-clock time for storage."""
    if value.tzinfo is None:
        return value
    offset = datetime.now(CLUB_TIMEZONE).utcoffset()
    return (value.astimezone(UTC) + offset).replace(tzinfo=None)


def create_event(session: Session, data: EventCreate) -> Event:
    event = Event.model_validate(data, update={"starts_at": _to_club_time(data.starts_at)})
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def list_events(session: Session) -> list[Event]:
    return list(session.exec(select(Event).order_by(Event.starts_at)).all())


def get_event(session: Session, event_id: int) -> Event:
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


def update_event(session: Session, event_id: int, data: EventUpdate) -> Event:
    event = get_event(session, event_id)
    changes = data.model_dump(exclude_unset=True)
    if "starts_at" in changes:
        changes["starts_at"] = _to_club_time(changes["starts_at"])
    event.sqlmodel_update(changes)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


def delete_event(session: Session, event_id: int) -> None:
    event = get_event(session, event_id)
    session.delete(event)
    session.commit()
