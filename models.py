from sqlalchemy import Column, String, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import CITEXT
from database import Base
from pydantic import BaseModel, Field


# Pydantic models
class VehicleBase(BaseModel):
    vin: str = Field(..., min_length=1)
    manufacturer_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    horse_power: int = Field(..., gt=0)
    mod_name: str = Field(..., min_length=1)
    mod_year: int = Field(..., gt=0)
    purchase_price: float = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=1)


class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(  # VIN
        CITEXT,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    man = Column(String)  # Manufacturer name
    desc = Column(String)  # Description
    hp = Column(Integer)  # Horse power
    model = Column(String)  # Model name
    year = Column(Integer)  # Model year
    price = Column(DECIMAL)  # Price
    fuel = Column(String)  # Fuel type

    def to_json(self):
        return VehicleBase(
            vin=self.vin,
            manufacturer_name=self.man,
            description=self.desc,
            horse_power=self.hp,
            mod_name=self.model,
            mod_year=self.year,
            purchase_price=self.price,
            fuel_type=self.fuel,
        )
