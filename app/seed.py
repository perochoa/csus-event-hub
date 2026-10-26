"""Fill the local database with demo data: `python -m app.seed`."""

from datetime import datetime

from sqlmodel import Session, SQLModel

from app.db import engine
from app.models import RSVP, Event, Member

EVENTS = [
    ("Intro to Git Workshop", "Lab 105", datetime(2026, 9, 17, 18, 0), 40),
    ("Hack Night", "Library Commons", datetime(2026, 10, 8, 19, 0), 60),
    ("Resume Review with Alumni", "Room 316", datetime(2026, 11, 4, 17, 30), 20),
    ("Intro to FastAPI", "Lecture Hall 110", datetime(2026, 11, 18, 18, 0), 50),
    ("End-of-Term Social", "Student Union", datetime(2026, 12, 3, 19, 0), 80),
]

MEMBERS = [
    ("Ava Chen", "ava@example.com", 2),
    ("Ben Okafor", "ben@example.com", 3),
    ("Chloe Martin", "chloe@example.com", 1),
    ("Dev Patel", "dev@example.com", 4),
    ("Elif Kaya", "elif@example.com", 2),
    ("Farah Haddad", "farah@example.com", 1),
    ("Gabe Silva", "gabe@example.com", 3),
    ("Hana Sato", "hana@example.com", 5),
]

# (member index, event index, checked in)
RSVPS = [
    (0, 0, True), (1, 0, True), (2, 0, False), (3, 0, True),
    (0, 1, True), (1, 1, False), (4, 1, True), (5, 1, False), (6, 1, False), (7, 1, False),
    (0, 2, False), (3, 2, False), (6, 2, False),
    (0, 3, False), (1, 3, False), (2, 3, False), (4, 3, False), (5, 3, False),
    (0, 4, False), (7, 4, False),
]  # fmt: skip


def seed() -> None:
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        events = [
            Event(title=t, location=loc, starts_at=at, capacity=cap) for t, loc, at, cap in EVENTS
        ]
        members = [Member(name=n, email=e, year=y) for n, e, y in MEMBERS]
        session.add_all(events + members)
        session.commit()
        for m, e, checked in RSVPS:
            session.add(RSVP(member_id=members[m].id, event_id=events[e].id, checked_in=checked))
        session.commit()
    print(f"Seeded {len(EVENTS)} events, {len(MEMBERS)} members, {len(RSVPS)} RSVPs.")


if __name__ == "__main__":
    seed()
