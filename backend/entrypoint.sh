#!/bin/ash
# Apply migrations automatically in development
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Start Django server
echo "Starting Django development server..."
exec "$@"
