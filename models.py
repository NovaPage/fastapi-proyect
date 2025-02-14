from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator # type: ignore
from sqlmodel import SQLModel, Field, Relationship, select # type: ignore
from db import get_session
from sqlalchemy.orm import Session  # type: ignore # Para manejar la sesión correctamente con `get_session`
from db import engine

class StatusEnum(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: StatusEnum = Field(default=StatusEnum.ACTIVE)

class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(default=None)
    price: int = Field(default=None)
    description: str = Field(default=None)
    customers: List['Customer'] = Relationship(back_populates="plans", link_model=CustomerPlan)

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    descripcion: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = next(get_session())  # ✅ SOLUCIÓN: Obtiene la sesión de la función generadora
        try:
            query = select(Customer).where(Customer.email == value)
            existing_customer = session.exec(query).first()
            if existing_customer:
                raise ValueError("This email is already registered")
        finally:
            session.close()  # ✅ Cerrar la sesión para evitar fugas de conexión
        return value





class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: List["Transaction"] = Relationship(back_populates="customer")
    plans: List['Plan'] = Relationship(back_populates="customers", link_model=CustomerPlan)

class TransactionBase(SQLModel):
    amount: float
    description: str

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    customer_id: int = Field(foreign_key="customer.id")

class Invoice(BaseModel):
    id: int
    customer: Customer
    transaction: List[Transaction]
    total: int

    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transaction)
