from fastapi import FastAPI, HTTPException, Depends
import models
from database import engine, SessionLocal, get_db, Base
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Pydantic models
class VehicleBase(BaseModel):
    vin: str
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str


db_dep = Annotated[Session, Depends(get_db)]


# API Endpoints
@app.get("/vehicle")
def get_vehicles(db: db_dep):
    return db.query(models.Vehicle).all()


@app.post("/vehicle")
def post_vehicle(vehicle: VehicleBase, db: db_dep):
    new_vehicle = models.Vehicle(
        vin=vehicle.vin,
        man=vehicle.manufacturer_name,
        desc=vehicle.description,
        hp=vehicle.horse_power,
        model=vehicle.model_name,
        year=vehicle.model_year,
        price=vehicle.purchase_price,
        fuel=vehicle.fuel_type,
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle


@app.get("/vehicle/{vin}")
def get_vehicle(vin: str, db: db_dep):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@app.put("/vehicle/{vin}")
def put_vehicle(vin: str, vehicle: VehicleBase, db: db_dep):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for key, value in vehicle.dict().items():
        if value is not None:
            setattr(vehicle, key, value)
    db.commit()
    db.refresh(vehicle)
    return vehicle


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: db_dep):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.vin == vin).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(vehicle)
    db.commit()
