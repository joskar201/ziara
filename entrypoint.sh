#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Check if we need to populate the database with fake data
if [ "$POPULATE_FAKE_DATA" = "true" ]
then
  echo "Populating the database with fake data..."
  python manage.py seed --users 10
fi

# Start the application
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
