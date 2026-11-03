
# Jenkins automatic polling test
from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)

DATABASE = "employees.db"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/employees", methods=["GET"])
def get_employees():
    connection = get_db()

    employees = connection.execute(
        "SELECT * FROM employees"
    ).fetchall()

    connection.close()

    return jsonify([dict(employee) for employee in employees])


@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    department = data.get("department")

    if not name or not department:
        return jsonify({"error": "Name and department required"}), 400

    connection = get_db()

    connection.execute(
        "INSERT INTO employees (name, department) VALUES (?, ?)",
        (name, department)
    )

    connection.commit()
    connection.close()

    return jsonify({"message": "Employee added successfully"}), 201


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000, debug=False)
