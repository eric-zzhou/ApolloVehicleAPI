#!/bin/bash

set -e

# Load environment variables from the .env file
export $(cat .env | xargs)

# Drop the database if it exists
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "postgres" -d "postgres" -c "SELECT 1 FROM pg_database WHERE datname='$TARGET_DB';" | grep -q 1 && \
echo "Database $TARGET_DB exists, dropping it..." && \
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "postgres" -d "postgres" -c "DROP DATABASE \"$TARGET_DB\";"

# Recreate database
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "postgres" -d "postgres" -c "CREATE DATABASE \"$TARGET_DB\";"
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "postgres" -d "$TARGET_DB" -c "CREATE EXTENSION IF NOT EXISTS citext;"
echo "Database $TARGET_DB created successfully"