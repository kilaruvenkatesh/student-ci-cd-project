#!/bin/bash

echo "Starting database migration..."

docker compose exec -T backend python - <<EOF
import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
""")

conn.commit()
cur.close()
conn.close()

print("Database migration completed successfully")
EOF
