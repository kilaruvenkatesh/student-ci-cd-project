#!/bin/bash

echo "Starting staging deployment..."

echo "Stopping existing containers..."
docker compose -f docker-compose.staging.yml down

echo "Pulling latest images..."
docker pull kilaruvenkatesh/student-backend:latest
docker pull kilaruvenkatesh/student-frontend:latest

echo "Starting containers..."
docker compose -f docker-compose.staging.yml up -d

echo "Waiting for services to start..."
sleep 10

echo "Running database migrations..."
./scripts/migrate.sh

echo "Verifying running containers..."
docker ps | grep student

echo "Staging deployment completed successfully"
