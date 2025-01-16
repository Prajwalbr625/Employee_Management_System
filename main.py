from flask import Blueprint, jsonify, request, Flask
from app.models.models import mongo_db
import uuid

app = Flask(__name__)


#Employee POST method
@app.route('/employees', methods=['POST'])
def add_employee():
    print('\t Inside a Add Employee Function')
    data = request.get_json()
    required_fields = ['name', 'age', 'sex', 'departmentID', 'position', 'salary']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} is required'}), 400
    _, status_code = mongo_db.get_specific_department_from_db(data.get('departmentID'))
    if not status_code == 200:
        return jsonify({'message': 'Department not found'}), 404
    employee_data = {
        'employeeID': str(uuid.uuid4()),
        'name': data.get('name'), # --> data['name']
        'age': data.get('age'), 
        'sex': data.get('sex'),
        'departmentID': data.get('departmentID'),
        'position': data.get('position'),
        'salary': data.get('salary'),
    }
    message, status_code = mongo_db.add_employee_to_db(employee_data)
    if status_code == 201:
        return jsonify({'employeeID': employee_data.get('employeeID') , 'message': message}), status_code
    else:
        return jsonify({'message': message}), status_code

#Employee GET method
@app.route('/employees', methods=['GET']) 
def get_employee_by_id():
    employee_id = request.args.get('employeeID')
    employee_details, status_code = mongo_db.get_specific_employee_from_db(employee_id)
    if status_code == 200:
        return jsonify(employee_details), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

#Employee DELETE method
@app.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee_by_id(employee_id):
    message, status_code = mongo_db.delete_employee_from_db(employee_id)
    if status_code == 204:
        return jsonify({'message': message}), status_code
    else:
        return jsonify({'Error': message}), status_code

#List all Employee GET method
@app.route('/list-employees', methods=['GET'])
def list_employees():
    employees, status_code = mongo_db.get_all_employees_from_db()
    if status_code == 200:
        return jsonify(employees), 200
    else:
        return jsonify({'Error': employees}), status_code

#Department POST method
@app.route('/departments', methods=['POST'])
def add_department():
        data = request.get_json()

        required_fields = ['name', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400

        department_data = {
            'departmentID': str(uuid.uuid4()),
            'name': data.get('name'),
            'location': data.get('location'),
            "employeeIDs": []
        }

        message, status_code = mongo_db.add_department_to_db(department_data)
        if status_code == 201:
            return jsonify({'departmentID': department_data.get('departmentID'), 'message': message}), status_code
        else:
            return jsonify({'message': message}), status_code

#Department GET method    
@app.route('/departments', methods=['GET'])
def get_department_by_id():
    department_id = request.args.get('departmentID')
    department_id, status_code = mongo_db.get_specific_department_from_db(department_id)
    if status_code == 200:
        return jsonify(department_id), 200
    else:
        return jsonify({'message': 'Department not found'}), 404
    
#Department PUT method
@app.route('/departments/<departmentID>', methods=['PUT'])
def update_department_by_id(departmentID):
    request_data = request.get_json()
    presence_fields = ['name','location']
    for field in request_data:
        if field not in presence_fields:
            return jsonify({'message': f'{presence_fields} only these fields can be updated'}), 400

    message, status_code = mongo_db.update_department_in_db(departmentID, request_data)
    if status_code == 200:
        return jsonify({'message': message}), status_code
    else:
        return jsonify({'Error': message}), status_code


#Department DELETE method    
@app.route('/departments/<departmentID>', methods=['DELETE'])
def delete_department_by_id(departmentID):
    message, status_code = mongo_db.delete_department_from_db(departmentID)
    if status_code == 204:
        return jsonify({'message': message}), status_code
    else:
        return jsonify({'Error': message}), status_code

    
#List all Department GET method
@app.route('/list-departments', methods=['GET'])
def list_departments():
    departments, status_code = mongo_db.get_all_departments_from_db()
    if status_code == 200:
        return jsonify(departments), 200
    else:
        return jsonify({'message': 'Error fetching departments'}), status_code
    
# Report Routes

@app.route('/report/departmentList', methods=['POST'])
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
    
    if not department_list:
        return jsonify({"message": "No departments found"}), 404
    
    return jsonify({"departments": department_list}), 200


@app.route('/report/employeeSalary', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',  port=8080, debug=True)