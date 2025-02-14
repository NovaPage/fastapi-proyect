from http.client import HTTPException
import time
from typing import Annotated
from urllib.request import Request
from fastapi import FastAPI, Depends, HTTPException, status  # type: ignore
from datetime import datetime
from models import Invoice
from db import create_all_tables
from .routers import customers, transactions, plans
from fastapi.security import HTTPBasic, HTTPBasicCredentials # type: ignore
from typing import Annotated

import zoneinfo

app = FastAPI()
# Ejecutar la creación de tablas al iniciar la aplicación
@app.on_event("startup")
def on_startup():
    create_all_tables(app)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response

security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == "H" and credentials.password == "1228":
        return {"message": f"Hola, {credentials.username}!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City"
}

@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

@app.post("/Invoices")
async def create_invoices(invoices_data: Invoice):
    return invoices_data