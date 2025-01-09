from flask import Blueprint, jsonify, request
import logging
import uuid
from app.models.models import mongo_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app_department = Blueprint('app_department', __name__)

@app_department.route('/departments', methods=['POST'])
def add_department():
    try:
        logger.info('\t Inside a Add Department Function')
        data = request.get_json()
        logger.info(f'\t Data: {data}')

        logging.info(f"\t Checking for required fields")
        required_fields = ['name', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400

        logging.info(f"\t Required fields are present")
        not_required_fields = []
        for each_field in data:
            if each_field not in required_fields:
                not_required_fields.append(each_field)
            
        logging.info(f"\t Checking for not required fields")
        if not_required_fields:
            logging.info(f"\t {not_required_fields} is not required and but present in the payload")
            return jsonify({'message': f'{not_required_fields} is not required'}), 400
                
        logging.info(f"\t Checking for data types")

        type_checks = {
            'name': str,
            'location': str
        }

        for field, expected_type in type_checks.items():
            if field in data and not isinstance(data[field], expected_type):
                logging.error(f"\t {field} should be of type {expected_type.__name__} but they have passed {data[field]} --> {type(data[field])}")
                return jsonify({'message': f'{field} should be a {expected_type.__name__}'}), 400

        logging.info(f"\t Data types are valid")
        
        department_data = {
            'departmentID': str(uuid.uuid4()),
            'name': data.get('name'),
            'location': data.get('location'),
            'employeeIDs': []
        }

        logging.info(f"\t Adding Department to the database")
        message, status_code = mongo_db.add_department_to_db(department_data)
        if status_code == 201:
            logging.info(f"\t Department added successfully")
            return jsonify({'departmentID': department_data.get('departmentID'), 'message': message}), status_code
        else:
            logging.error(f"\t Database error: {message}")
            return jsonify({'message': message}), status_code
    except Exception as e:
        logger.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    
@app_department.route('/departments', methods=['GET'])
def get_department_by_id():
    try:
        logging.info('\t Inside a Get Department By ID Function')
        department_id = request.args.get('departmentID')
        logging.info(f'\t The user has passed this Department ID: {department_id}')
        logging.info(f"\t Fetching the Department ID from the Database")
        department_id, status_code = mongo_db.get_specific_department_from_db(department_id)
        if status_code == 200:
            logging.info(f"\t Department ID found in the database")
            return jsonify(department_id), 200
        else:
            logging.error(f"\t Department ID not found in the database")
            return jsonify({'message': 'Department not found'}), 404
    except Exception as e: 
        logging.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    

@app_department.route('/departments/<departmentID>', methods=['PUT'])
def update_department_by_id(departmentID):
    try:
        logging.info('\t Inside a Update Department By ID Function')
        request_data = request.get_json()
        logging.info(f'\t The user has passed this Department ID: {departmentID}')

        logging.info(f"\t Checking for Unwanted fields")
        presence_fields = ['name', 'location', 'employeeIDs']
        for field in request_data:
            if field not in presence_fields:
                logging.error(f"\t {field} is not required")
                return jsonify({'message': f'{field} is not required'}), 400
        
        logging.info(f"\t Checking for data types")
        type_checks = {
            'name': str,
            'location': str,
            'employeeIDs': list
        }

        for field, expected_type in type_checks.items():
            if field in request_data and not isinstance(request_data[field], expected_type):
                logging.error(f"\t {field} should be of type {expected_type.__name__} but they have passed {request_data[field]} --> {type(request_data[field])}")
                return jsonify({'message': f'{field} should be a {expected_type.__name__}'}), 400
        
        logging.info(f"\t Data types are valid")

        logging.info(f"\t Updating the Department in the database")
        message, status_code = mongo_db.update_department_in_db(departmentID, request_data)

        if status_code == 200:
            logging.info(f"\t Department updated successfully")
            return jsonify({'message': message}), status_code
        else:
            logging.error(f"\t Error : {message}")
            return jsonify({'Error': message}), status_code
    
    except Exception as e:
        logging.info(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500
    
@app_department.route('/departments/<departmentID>', methods=['DELETE'])
def delete_department_by_id(departmentID):
    try:
        logging.info('\t Inside a Delete Department By ID Function')
        logging.info(f'\t The user has passed this Department ID: {departmentID}')
        logging.info(f"\t Fetching the Department ID from the Database")
        message, status_code = mongo_db.delete_department_from_db(departmentID)
        if status_code == 204:
            logging.info(f"\t Department deleted successfully")
            return jsonify({'message': message}), status_code
        else:
            logging.error(f"\t Error: {message}")
            return jsonify({'Error': message}), status_code
        
    except Exception as e:
        logging.error(f'\t Error: {e}')
        return jsonify({'message': 'An error occurred'}), 500