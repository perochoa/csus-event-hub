from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import init_db
from app.routes import events, members, rsvps, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="CSUS Event Hub", version="0.1.0", lifespan=lifespan)

app.include_router(events.router)
app.include_router(members.router)
app.include_router(rsvps.router)
app.include_router(stats.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
