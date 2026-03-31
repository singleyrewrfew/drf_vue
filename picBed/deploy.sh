#!/bin/bash

echo "Starting deployment..."

echo "Building Docker images..."
docker-compose build

echo "Stopping existing containers..."
docker-compose down

echo "Starting containers..."
docker-compose up -d

echo "Running database migrations..."
docker-compose exec web python manage.py migrate

echo "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "Deployment completed successfully!"
docker-compose ps
