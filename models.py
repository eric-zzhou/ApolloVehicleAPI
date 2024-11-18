from sqlalchemy import Column, String, Integer, DECIMAL
from database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(  # VIN
        String,
        case_sensitive=False,
        primary_key=True,
        index=True,
    )
    man = Column(String)  # Manufacturer name
    desc = Column(String)  # Description
    hp = Column(Integer)  # Horse power
    model = Column(String)  # Model name
    year = Column(Integer)  # Model year
    price = Column(DECIMAL)  # Price
    fuel = Column(String)  # Fuel type
