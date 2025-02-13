from enum import Enum
from typing import Optional
from pydantic import BaseModel # type: ignore
from sqlmodel import SQLModel, Field, Relationship # type: ignore

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
    customers: list['Customer'] = Relationship(back_populates="plans", link_model=CustomerPlan)


# Opcion 1
# class CustomerBase(BaseModel):
#     name: str
#     descripcion: str | None
#     email: str
#     age: int

# opcion 2
class CustomerBase(SQLModel):
    name: str = Field(default=None)
    descripcion: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass

# opcion 1
# class Customer(CustomerBase, SQLModel, table=True):
#     id: int | None = None

# opcion 2
class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list['Plan'] = Relationship(back_populates="customers", link_model=CustomerPlan)

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
    transaction: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum(transaction.ammount for transaction in self.transaction)