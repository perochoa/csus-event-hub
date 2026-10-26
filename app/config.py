import os
from zoneinfo import ZoneInfo

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./event_hub.db")

# Wall-clock timezone the club schedules events in.
CLUB_TIMEZONE = ZoneInfo(os.getenv("CLUB_TIMEZONE", "America/Toronto"))
