from datetime import UTC, datetime

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class EventBase(SQLModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = ""
    location: str = Field(min_length=1)
    starts_at: datetime
    capacity: int = Field(gt=0)


class Event(EventBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    starts_at: NaiveDatetime


class EventCreate(EventBase):
    pass


class EventUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    location: str | None = Field(default=None, min_length=1)
    starts_at: datetime | None = None
    capacity: int | None = Field(default=None, gt=0)


class EventRead(EventBase):
    id: int


class MemberBase(SQLModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=3)
    year: int = Field(ge=1, le=6)


class Member(MemberBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class MemberCreate(MemberBase):
    pass


class MemberRead(MemberBase):
    id: int


class RSVP(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="member.id")
    event_id: int = Field(foreign_key="event.id")
    checked_in: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RSVPCreate(SQLModel):
    member_id: int
    event_id: int


class RSVPRead(SQLModel):
    id: int
    member_id: int
    event_id: int
    checked_in: bool
    created_at: datetime
