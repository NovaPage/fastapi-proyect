from fastapi import APIRouter, HTTPException, status # type: ignore
from models import Transaction, TransactionCreate, Customer
from db import sessionDep
from sqlmodel import select # type: ignore

router = APIRouter()

@router.post("/Transactions",tags=['transactions'])
async def create_transactions(transactions_data: TransactionCreate, session: sessionDep): # type: ignore
    transactions_data_dict = transactions_data.model_dump()
    session.get(Customer, transactions_data_dict.get('customer_id'))
    if not Customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    transaction_db = Transaction.model_validate(transactions_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db

@router.get("/transactions", tags=['transactions'])
async def lit_transaction(session: sessionDep): # type: ignore
    query = select(Transaction)
    transactions = session.exec(query).all()
    return transactions