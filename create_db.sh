#!/bin/bash

# Load environment variables from the .env file
export $(cat .env | xargs)

# Create new database from default postgres database
psql -h $DB_HOST -U postgres -d postgres -c "CREATE DATABASE \"$TARGET_DB\";"

# Output
echo "Database $TARGET_DB created successfully"
