from flask import Flask, request, jsonify
import sqlite3

app = Flask(_name_)
DB_NAME = "database.db"


# إنشاء قاعدة البيانات والجدول
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Create - إضافة موظف
@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, department) VALUES (?, ?)",
        (data["name"], data["department"])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee added successfully"}), 201


# Read - عرض جميع الموظفين
@app.route("/employees", methods=["GET"])
def get_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()

    result = []
    for emp in employees:
        result.append({
            "id": emp[0],
            "name": emp[1],
            "department": emp[2]
        })

    return jsonify(result)


# Update - تعديل بيانات موظف
@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employees SET name=?, department=? WHERE id=?",
        (data["name"], data["department"], emp_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee updated successfully"})


# Delete - حذف موظف
@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee deleted successfully"})


if _name_ == "_main_":
    init_db()
    app.run(debug=True)
