from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import Annotated, List
from sqlalchemy.orm import Session
from database import engine, get_db, Base
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)


db_dep = Annotated[Session, Depends(get_db)]


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.middleware("http")
async def handle_invalid_json(request: Request, call_next):
    try:
        return await call_next(request)
    except ValidationError:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid JSON format"},
        )


# API Endpoints
@app.get("/vehicle", response_model=List[models.VehicleBase])
def get_vehicles(db: db_dep):
    return [vehicle.to_json() for vehicle in db.query(models.Vehicle).all()]


@app.post("/vehicle", status_code=201, response_model=models.VehicleBase)
def post_vehicle(vehicle: models.VehicleBase, db: db_dep):
    # Ensure unique VIN
    if db.query(models.Vehicle).filter(models.Vehicle.vin == vehicle.vin).first():
        raise HTTPException(
            status_code=400, detail="Vehicle with this VIN already exists"
        )

    new_vehicle = models.Vehicle(
        vin=vehicle.vin,
        man=vehicle.manufacturer_name,
        desc=vehicle.description,
        hp=vehicle.horse_power,
        model=vehicle.mod_name,
        year=vehicle.mod_year,
        price=vehicle.purchase_price,
        fuel=vehicle.fuel_type,
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle.to_json()


@app.get("/vehicle/{vin}", response_model=models.VehicleBase)
def get_vehicle(vin: str, db: db_dep):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    return vehicle.to_json()


@app.put("/vehicle/{vin}", response_model=models.VehicleBase)
def put_vehicle(vin: str, new_vehicle: models.VehicleBase, db: db_dep):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")

    vehicle.man = new_vehicle.manufacturer_name
    vehicle.desc = new_vehicle.description
    vehicle.hp = new_vehicle.horse_power
    vehicle.model = new_vehicle.mod_name
    vehicle.year = new_vehicle.mod_year
    vehicle.price = new_vehicle.purchase_price
    vehicle.fuel = new_vehicle.fuel_type

    db.commit()
    db.refresh(vehicle)
    return vehicle.to_json()


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: db_dep):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=400, detail="Vehicle not found")
    db.delete(vehicle)
    db.commit()
    return None
