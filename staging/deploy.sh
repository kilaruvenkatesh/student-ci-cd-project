#!/bin/bash

set -e

echo "Starting staging deployment"

echo "Stopping existing containers"
docker compose -f docker-compose.staging.yml down

echo "Pulling latest images from Docker Hub"
docker pull kilaruvenkatesh/student-backend:latest
docker pull kilaruvenkatesh/student-frontend:latest

echo "Starting containers"
docker compose -f docker-compose.staging.yml up -d

echo "Waiting for services to stabilize"
sleep 10

echo "Running database migration check"
docker compose -f docker-compose.staging.yml exec backend python -c "
import psycopg2, os
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS')
)
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
''')
conn.commit()
cur.close()
conn.close()
print('Database migration completed')
"

echo "Verifying running containers"
docker ps | grep student

echo "Verifying backend API"
curl -f http://localhost:5056/students > /dev/null

echo "Staging deployment completed successfully"
