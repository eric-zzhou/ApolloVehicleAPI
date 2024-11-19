# ApolloVehicleAPI
Repo for Apollo Engineering Coding Exercise on Vehicle API

## Setup
1. Clone the repo
2. Virtual Environment and Dependencies: ```./setup.sh```
3. Activate the virtual environment: ```source env/bin/activate```
4. Create a ```.env``` file in the root directory based on the ```.env.example``` file
5. Properly set up postgresql and update the ```.env``` file with the database credentials
    - Install postgresql and run it
    - Assuming default superuser and server both named ```postgres``` exist
6. Create new database named "ApolloVehicle": ```./create_db.sh```
    - Note: might need to do ```chmod +x create_db.sh``` and fill out default postgres user password

## Run

```uvicorn main:app --reload```

## Test

```./run_tests.sh```

## File Structure
```
ApolloVehicleAPI
├── env (folder)
├── .env
├── .env.example
├── .gitignore
├── create_db.sh
├── database.py
├── main.py
├── models.py
├── README.md
├── requirements.txt
├── reset_db.sh
├── run_tests.sh
├── setup.sh
|── test_vehicles.py
```

- Helper Shell Scripts:
    - ```setup.sh```: set up the virtual environment
    - ```create_db.sh```: create database
    - ```reset_db.sh```: reset/clear database
    - ```run_tests.sh```: run tests
- Python Files:
    - ```main.py```: FastAPI app
    - ```database.py```: database connection and session management
    - ```models.py```: SQL and Pydantic models
    - ```test_vehicles.py```: test file

## API Endpoints
- ```GET /vehicle```: Get all vehicles
- ```POST /vehicle```: Create a new vehicle
- ```GET /vehicle/{vin}```: Get a vehicle by vin
- ```PUT /vehicle/{vin}```: Update a vehicle by vin
- ```DELETE /vehicle/{vin}```: Delete a vehicle by vin

