# ApolloVehicleAPI
Repo for Apollo Engineering Coding Exercise on Vehicle API

## File Structure
```
ApolloVehicleAPI
├── README.md
├── setup.sh
├── env
├── requirements.txt
|── database.py
|── models.py
|── main.py
|── test_main.py
```
```setup.sh``` - Script to setup the virtual environment and install dependencies

```env``` - Virtual environment directory

```requirements.txt``` - File containing the dependencies

```database.py``` - File containing the database connection and queries

```models.py``` - File containing the database models

```main.py``` - File containing the API routes

```test_main.py``` - File containing the tests

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

## Test
