from fastapi import APIRouter, Query, status, HTTPException # type: ignore
from sqlmodel import select # type: ignore
from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan, StatusEnum
from db import sessionDep

router = APIRouter()

@router.post("/Customers", response_model = Customer, status_code=status.HTTP_201_CREATED,tags=['customers'])
async def create_customer(customer_data: CustomerCreate, session: sessionDep): # type: ignore
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model = Customer, tags=['customers'])
async def read_customer(customer_id: int, session: sessionDep): # type: ignore
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="cutomer doesn't exits")
    return customer_db

@router.patch("/customers/{customer_id}", response_model = Customer, status_code = status.HTTP_201_CREATED, tags=['customers'])
async def read_customer(customer_id: int, customer_data: CustomerUpdate,session: sessionDep): # type: ignore
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="cutomer doesn't exits")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.delete("/customers/{customer_id}", tags=['customers'])
async def delete_customer(customer_id: int, session: sessionDep): # type: ignore
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="cutomer doesn't exits")
    session.delete(customer_db)
    session.commit()
    return {"Detail": "Ok"}

@router.get("/Customers", response_model = list[Customer], tags=['customers'])
async def list_customer(session: sessionDep): # type: ignore
    return session.exec(select(Customer)).all()
    # return db_customers

# customers?key=valor

@router.post("/customer/{customer_id}/plans/{plan_id}", tags=['customers'])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: sessionDep, plan_status: StatusEnum = Query()): # type: ignore
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The customer or plan doesn't exist")
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get("/customer/{customer_id}/plans", tags=['customers'])
async def subscribe_customer_to_plan(customer_id: int, session: sessionDep, plan_status: StatusEnum = Query()): # type: ignore
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where(CustomerPlan.status == plan_status)
    plans = session.exec(query).all()
    return plans