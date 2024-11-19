import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db
from models import Vehicle


client = TestClient(app)


# Dependency override for testing database session
@pytest.fixture
def db_session():
    db = next(get_db())
    yield db
    db.close()


# Creating vehicle
def test_create_vehicle():
    response = client.post(
        "/vehicle",
        json={
            "vin": "1HGCM82633A123456",
            "manufacturer_name": "Honda",
            "description": "Reliable car",
            "horse_power": 150,
            "mod_name": "Civic",
            "mod_year": 2023,
            "purchase_price": 20000.00,
            "fuel_type": "Gasoline",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["vin"] == "1HGCM82633A123456"
    assert data["manufacturer_name"] == "Honda"
    assert data["mod_year"] == 2023


# Missing fuel_type
def test_create_invalid_vehicle():
    response = client.post(
        "/vehicle",
        json={
            "vin": "2HGCM82633A654321",
            "manufacturer_name": "Toyota",
            "description": "Compact car",
            "horse_power": 130,
            "mod_name": "Corolla",
            "mod_year": 2023,
            "purchase_price": 18000.00,
            # Missing fuel_type
        },
    )
    assert response.status_code == 422
    assert "fuel_type" in response.json()["errors"][0]["loc"]


# Duplicate VIN
def test_create_duplicate_vehicle(db_session):
    # Create vehicle
    db_session.add(
        Vehicle(
            vin="1HGCM82633A123457",
            man="Ford",
            desc="Sedan",
            hp=160,
            model="Fusion",
            year=2022,
            price=25000.00,
            fuel="Gasoline",
        )
    )
    db_session.commit()

    # Creating same VIN
    response = client.post(
        "/vehicle",
        json={
            "vin": "1hGCm82633A123457",
            "manufacturer_name": "Ford",
            "description": "Sedan #2",
            "horse_power": 161,
            "mod_name": "Fusion x2",
            "mod_year": 2023,
            "purchase_price": 30000.00,
            "fuel_type": "Gasoline",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Vehicle with this VIN already exists"


# Get vehicle by VIN
def test_get_vehicle(db_session):
    db_session.add(
        Vehicle(
            vin="1HGCM82633A123458",
            man="Nissan",
            desc="Compact SUV",
            hp=200,
            model="Rogue",
            year=2023,
            price=28000.00,
            fuel="Gasoline",
        )
    )
    db_session.commit()

    response = client.get("/vehicle/1HgCm82633a123458")
    assert response.status_code == 200
    data = response.json()
    assert data["vin"] == "1HGCM82633A123458"
    assert data["manufacturer_name"] == "Nissan"
    assert data["fuel_type"] == "Gasoline"


# Nonexistent vehicle
def test_get_vehicle_not_found():
    response = client.get("/vehicle/noexist")
    assert response.status_code == 400
    assert response.json()["detail"] == "Vehicle not found"


# Updating vehicle
def test_update_vehicle(db_session):
    db_session.add(
        Vehicle(
            vin="1HGCM82633A123459",
            man="Chevrolet",
            desc="Sports car",
            hp=300,
            model="Camaro",
            year=2023,
            price=35000.00,
            fuel="Gasoline",
        )
    )
    db_session.commit()

    response = client.put(
        "/vehicle/1hgCM82633A123459",
        json={
            "vin": "1HGCM82633A123459",
            "manufacturer_name": "Chevrolet",
            "description": "Updated sports car",
            "horse_power": 350,
            "mod_name": "Camaro",
            "mod_year": 2023,
            "purchase_price": 36000.00,
            "fuel_type": "Gasoline",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated sports car"
    assert data["horse_power"] == 350


# Deleting vehicle
def test_delete_vehicle(db_session):
    db_session.add(
        Vehicle(
            vin="1HGCM82633A123460",
            man="BMW",
            desc="Luxury SUV",
            hp=400,
            model="X5",
            year=2023,
            price=55000.00,
            fuel="Diesel",
        )
    )
    db_session.commit()

    response = client.delete("/vehicle/1hGCM82633A123460")
    assert response.status_code == 204

    response = client.get("/vehicle/1HGCM82633A123460")
    assert response.status_code == 400
    assert response.json()["detail"] == "Vehicle not found"


# Invalid JSON
def test_invalid_json():
    response = client.post("/vehicle", data="Invalid JSON")
    assert response.status_code == 400
    assert "Invalid JSON format" in response.json()["detail"]


# Empty required fields
def test_empty_required_fields():
    response = client.post(
        "/vehicle",
        json={
            "vin": "1HGCM82633A123461",
            "manufacturer_name": "",
            "description": "Luxury Sedan",
            "horse_power": 250,
            "mod_name": "Mercedes",
            "mod_year": 2023,
            "purchase_price": 70000.00,
            "fuel_type": "Gasoline",
        },
    )
    assert response.status_code == 422
    assert "manufacturer_name" in response.json()["errors"][0]["loc"]


# Test for invalid data types
def test_invalid_data_types():
    response = client.post(
        "/vehicle",
        json={
            "vin": "1HGCM82633A123462",
            "manufacturer_name": "Audi",
            "description": "Luxury car",
            "horse_power": "two hundred",  # Invalid type
            "mod_name": "A6",
            "mod_year": 2023,
            "purchase_price": 55000.00,
            "fuel_type": "Diesel",
        },
    )
    assert response.status_code == 422
    assert "horse_power" in response.json()["errors"][0]["loc"]
