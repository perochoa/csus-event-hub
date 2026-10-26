from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import Member, MemberCreate, MemberRead

router = APIRouter(prefix="/members", tags=["members"])


@router.post("", response_model=MemberRead, status_code=201)
def create_member(payload: MemberCreate, session: Session = Depends(get_session)):
    member = Member.model_validate(payload)
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.get("", response_model=list[MemberRead])
def list_members(session: Session = Depends(get_session)):
    return session.exec(select(Member).order_by(Member.name)).all()


@router.get("/{member_id}", response_model=MemberRead)
def get_member(member_id: int, session: Session = Depends(get_session)):
    member = session.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
