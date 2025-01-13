from flask import Blueprint, jsonify, request
from app.utils.test_runner import run_tests
from app.models.models import mongo_db

app_report = Blueprint('app_report', __name__)

@app_report.route('/report', methods=['GET'])
def report():
    test_results = run_tests()
    return jsonify({"test_results": test_results})

@app_report.route('/departments/list', methods=['POST'])
def list_departments_by_name():
    data = request.get_json()
    department_name = data.get('name')
    if not department_name:
        return jsonify({"error": "Department name is required"}), 400

    departments = mongo_db.departmentCollection.find({"name": department_name})
    department_list = []
    for department in departments:
        department.pop('_id', None)
        department_list.append(department)

    return jsonify({"departments": department_list}), 200

@app_report.route('/employees/salary', methods=['POST'])
def list_employees_by_salary():
    data = request.get_json()
    salary = data.get('salary')
    if salary is None:
        return jsonify({"error": "Salary is required"}), 400

    salary_range = data.get('salary')
    if salary_range:
        employees = mongo_db.employeeCollection.find({"salary": {"$gte": salary_range[0], "$lte": salary_range[1]}})
    else:
        employees = mongo_db.employeeCollection.find({"salary": {"$gte": salary}})
    employee_list = []
    for employee in employees:
        employee.pop('_id', None)
        employee_list.append(employee)

    return jsonify({"employees": employee_list}), 200