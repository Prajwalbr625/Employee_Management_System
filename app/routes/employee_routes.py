from flask import Blueprint, jsonify, request
import logging
from app.models.models import mongo_db
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_employee = Blueprint('app_employee', __name__)



@app_employee.route('/employees', methods=['POST'])
def add_employee():
    try:
        logger.info('\t Inside a Add Employee Function')
        data = request.get_json()
        logger.info(f'\t Data: {data}')


        logging.info(f"\t Checking for required fields")

        required_fields = ['name', 'age', 'sex', 'departmentID', 'position', 'salary']
        for field in required_fields:
            if field not in data:
                logging.error(f"\t {field} is required and not present in the payload")
                return jsonify({'message': f'{field} is required'}), 400
        
        logging.info(f"\t Required fields are present")

        logging.info(f"\t Checking for not required fields")
        not_required_fields = []
        for each_field in data:
            if each_field not in required_fields:
                not_required_fields.append(each_field)
        
        if not_required_fields:
            logging.info(f"\t {not_required_fields} is not required and but present in the payload")
            return jsonify({'message': f'{not_required_fields} is not required'}), 400
        logging.info(f"\t Not required fields are not present")
        
        logging.info(f"\t Checking for data types")

        type_checks = {
            'name': str,
            'age': int,
            'sex': str,
            'departmentID': str,
            'position': str,
            'salary': int
        }

        for field, expected_type in type_checks.items():
            if field in data and not isinstance(data[field], expected_type):
                logging.error(f"\t {field} should be of type {expected_type.__name__} but they have passed {data[field]} --> {type(data[field])}")
                return jsonify({'message': f'{field} should be a {expected_type.__name__}'}), 400

        logging.info(f"\t Data types are valid")

        
        department_id, status_code = mongo_db.get_specific_department_from_db(data.get('departmentID'))
        if not status_code == 200:
            logging.error(f"\t Error: {department_id}")
            return jsonify({'message': 'Department not found'}), 404

        employee_data = {
            'employeeID': str(uuid.uuid4()),
            'name': data.get('name'),
            'age': data.get('age'),
            'sex': data.get('sex'),
            'departmentID': data.get('departmentID'),
            'position': data.get('position'),
            'salary': data.get('salary'),
        }

        logging.info(f"\t Adding employee to the database --> {employee_data}")
        message, status_code = mongo_db.add_employee_to_db(employee_data)
        if status_code == 201:
            logging.info(f"\t Employee added successfully to the DB")
            return jsonify({'employeeID': employee_data.get('employeeID') , 'message': message}), status_code
        else:
            logging.error(f"\t Error: {message}")
            return jsonify({'message': message}), status_code
            
    except Exception as e:
        logger.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    


@app_employee.route('/employees', methods=['GET']) 
def get_employee_by_id():
    try:
        logging.info('\t Inside a Get Employee By ID Function')
        employee_id = request.args.get('employeeID')
        logging.info(f'\t The user has passed this Employee ID: {employee_id}')
        logging.info(f"\t Fetching the Employee ID from the Database")
        employee_details, status_code = mongo_db.get_specific_employee_from_db(employee_id)
        if status_code == 200:
            logging.info(f"\t Employee ID found in the database")
            return jsonify(employee_details), 200
        else:
            logging.error(f"\t Employee ID not found in the database")
            return jsonify({'message': 'Employee not found'}), 404
    except Exception as e:
        logger.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    
@app_employee.route('/employees/<employee_id>', methods=['PUT'])
def update_employee_by_id(employee_id):
    try:
        logging.info('\t Inside a Update Employee By ID Function')
        data = request.get_json()
        logging.info(f'\t The user has passed this data: {data}')
        
        logging.info(f"\t Checking for not required fields")
        present_fields = ['name', 'age', 'sex', 'departmentID', 'position', 'salary']
        for each_field in data:
            if each_field not in present_fields:
                logging.error(f"\t {each_field} is should not be present in the payload")
                return jsonify({'message': f'{each_field} is should not be present in the payload'}), 400
        logging.info(f"\t Not required fields are not present")
        
        logging.info(f"\t Checking for data types")
        type_checks = {
            'name': str,
            'age': int,
            'sex': str,
            'departmentID': str,
            'position': str,
            'salary': int
        }

        for field, expected_type in type_checks.items():
            if field in data and not isinstance(data[field], expected_type):
                logging.error(f"\t {field} should be of type {expected_type.__name__} but they have passed {data[field]} --> {type(data[field])}")
                return jsonify({'message': f'{field} should be a {expected_type.__name__}'}), 400
        logging.info(f"\t Data types are valid")
        
        message, status_code = mongo_db.update_employee_in_db(employee_id, data)
        if status_code == 200:
            logging.info(f"\t Employee updated successfully")
            return jsonify({'message': message}), 200
        else:
            logging.error(f"\t Error: {message}")
            return jsonify({'message': message}), status_code

    except Exception as e:
        logging.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    

@app_employee.route('/employees/<employee_id>', methods=['DELETE'])
def delete_employee_by_id(employee_id):
    try:
        logging.info('\t Inside a Delete Employee By ID Function')
        message, status_code = mongo_db.delete_employee_from_db(employee_id)
        if status_code == 204:
            logging.info(f"\t Employee deleted successfully")
            return jsonify({'message': message}), status_code
        else:
            logging.error(f"\t Error: {message}")
            return jsonify({'message': message}), status_code
    except Exception as e:
        logging.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500

@app_employee.route('/list-employees', methods=['GET'])
def list_employees():
    try:
        logging.info('\t Inside List Employees Function')
        logging.info(f"\t Fetching all employees from the database")
        employees, status_code = mongo_db.get_all_employees_from_db()
        if status_code == 200:
            logging.info(f"\t Employees fetched successfully")
            return jsonify(employees), 200
        else:
            logging.error(f"\t Error: {employees}")
            return jsonify({'Error': employees}), status_code
    except Exception as e:
        logging.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
