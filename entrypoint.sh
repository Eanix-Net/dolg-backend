#!/bin/sh

# Source environment variables if .env file exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! pg_isready -h ${DB_HOST:-192.168.2.7} -p ${DB_PORT:-5432} -U ${DB_USER:-lawnmate}; do
    sleep 1
done
echo "PostgreSQL is ready!"

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start the application
echo "Starting application..."
exec "$@" 