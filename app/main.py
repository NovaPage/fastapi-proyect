from fastapi import FastAPI
from datetime import datetime
from models import Invoice
from db import create_all_tables
from .routers import customers, transactions, plans

import zoneinfo

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

@app.get("/")
async def root():
    return {"message": "NovaPage"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City"
}

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

# db_customers: list[Customer] = []

@app.post("/Invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data