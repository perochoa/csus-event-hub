from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db import get_session
from app.services.legacy_stats import build_stats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def get_stats(session: Session = Depends(get_session)) -> dict:
    return build_stats(session)
