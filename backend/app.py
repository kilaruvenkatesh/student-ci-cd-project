from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


# --------------------------------
# Database connection with retry
# --------------------------------
def get_db_connection():
    for _ in range(10):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(2)
    raise Exception("Database not available")


# --------------------------------
# Initialize database
# --------------------------------
def init_db():
    conn = get_db_connection()
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


# --------------------------------
# APIs
# --------------------------------

# GET all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM students ORDER BY id;")
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(students)


# ADD student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, email) VALUES (%s, %s);",
        (data["name"], data["email"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201


# UPDATE student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=%s, email=%s WHERE id=%s;",
        (data["name"], data["email"], student_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student updated successfully"})


# DELETE student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s;", (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Student deleted successfully"})


# --------------------------------
# App start
# --------------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
