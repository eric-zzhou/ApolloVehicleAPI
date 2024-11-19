#!/bin/bash

set -e

# Load environment variables from the .env file
export $(cat .env | xargs)

# Create new database from default postgres database
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U postgres -d postgres -c "CREATE DATABASE \"$TARGET_DB\";"

PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "postgres" -d "$TARGET_DB" -c "CREATE EXTENSION IF NOT EXISTS citext;"

# Output
echo "Database $TARGET_DB created successfully"
