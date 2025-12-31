#!/bin/bash

echo " Starting staging deployment..."

echo " Stopping existing containers..."
docker compose -f docker-compose.staging.yml down

echo " Pulling latest images from Docker Hub..."
docker pull kilaruvenkatesh/student-backend:latest
docker pull kilaruvenkatesh/student-frontend:latest

echo " Starting new containers..."
docker compose -f docker-compose.staging.yml up -d

echo " Waiting for services to stabilize..."
sleep 10

echo " Checking running containers..."
docker ps | grep student

echo " Staging deployment completed successfully!"
