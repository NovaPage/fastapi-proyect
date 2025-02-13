from fastapi import APIRouter # type: ignore
from sqlmodel import select # type: ignore
from models import Plan
from db import sessionDep

router = APIRouter()

@router.post("/plans", tags=['plans'])
def create_plan(plan_data: Plan, session: sessionDep): # type: ignore
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", response_model=list[Plan], tags=['plans'])
def list_plan(session: sessionDep): # type: ignore
    plans = session.exec(select(Plan)).all()
    return plans