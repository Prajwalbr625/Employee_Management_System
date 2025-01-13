from pymongo import MongoClient
import logging
import certifi
import app.config as config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DB:

    def __init__(self):
        self.db = self.setup_db()
        self.employeeCollection = self.db[config.MONGO_EMPLOYEE_COLLECTION_NAME]
        self.departmentCollection = self.db[config.MONGO_DEPARTMENT_COLLECTION_NAME]


    def setup_db(self):
        try:
            logging.info(f'\t Connecting to the database')
            client = MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
            self.db = client[config.MONGO_DB_NAME]
            logging.info(f'\t Connection to the database is successfull')
            return self.db
        except Exception as e:
            logger.error(f'\t Error: Something went wrong while connecting to the database -->  {e}')
            return e, 500
        

# ----------------------------------- Employee DB Functions --------------------------------- #

    def add_employee_to_db(self, employee_data):
        try:    
            logging.info(f'\t Inside a Add Employee Function --> Models.py')
            result = self.employeeCollection.find_one({"name": employee_data.get('name')})
            if result:
                logging.error(f'\t Employee with the name {employee_data.get("name")} already exists')
                return 'Employee with the same name already exists, Please provide Different Name', 400
            self.employeeCollection.insert_one(employee_data)
            self.departmentCollection.update_one({'departmentID': employee_data.get('departmentID')}, {'$push': {'employeeIDs': employee_data.get('employeeID')}})
            return 'Employee added successfully', 201
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return e, 500
        
    def get_specific_employee_from_db(self, employee_id):
        try:
            logging.info(f'\t Inside a Get Employee By ID Function --> Models.py')
            response = self.employeeCollection.find_one({"employeeID":employee_id})
            if response is None:
                logging.error(f'\t Employee not found in the DB')
                return 'Employee not found in the DB', 404
            response.pop('_id', None)
            return response, 200
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return e, 500
        
    def update_employee_in_db(self, employee_id, employee_data):
        try:
            logging.info(f'\t Inside a Update Employee By ID Function --> Models.py')
            _, employee_presence_status_code = self.get_specific_employee_from_db(employee_id)
            if employee_presence_status_code != 200:
                logging.error(f'\t Employee not found in the DB')
                return 'Employee not found in the DB', 404

            self.employeeCollection.update_one({'employeeID': employee_id}, {'$set': employee_data})
            return 'Employee updated successfully', 200
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return e, 500
        
    def delete_employee_from_db(self, employee_id):
        try:
            logging.info(f'\t Inside a Delete Employee By ID Function --> Models.py')
            employee_data, employee_presence_status_code = self.get_specific_employee_from_db(employee_id)
            if employee_presence_status_code != 200:
                logging.error(f'\t Employee not found in the DB')
                return 'Employee not found in the DB', 404
            result = self.employeeCollection.delete_one({'employeeID': employee_id})
            if result.deleted_count == 1:
                logging.info(f'\t Employee ID is deleted successfully from the Employee DB')
                self.departmentCollection.update_one({'departmentID': employee_data.get('departmentID')}, {'$pull': {'employeeIDs': employee_id}})
                logging.info(f'\t Employee ID is removed successfully from the Department DB')
                return 'Employee deleted successfully', 204
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return str(e), 500       

    def get_all_employees_from_db(self):
        try:
            logging.info(f'\t Inside Get All Employees Function --> Models.py')
            employees = list(self.employeeCollection.find())
            if not employees:
                logging.error(f'\t No employees found in the DB')
                return 'No employees found in the DB', 404
            for employee in employees:
                employee.pop('_id', None)
            logging.info(f'\t Employees fetched successfully')
            return employees, 200
        except Exception as e:
            logging.error(f'\t Error: {e} --> Returned 500 Internal Server Error')
            return str(e), 500


# ------------------------------ Department DB Functions -------------------------------- #
        
    def add_department_to_db(self, department_data):
        try:
            logging.info(f'\t Inside a Add Department Function --> Models.py')
            self.departmentCollection.insert_one(department_data)
            return 'Department added successfully', 201
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return e, 500
    
    def get_specific_department_from_db(self, department_id):
        try:
            logging.info(f'\t Inside a Get Department By ID Function --> Models.py')
            response = self.departmentCollection.find_one({'departmentID': department_id})
            if response is None:
                logging.error(f'\t Department not found in the DB')
                return 'Department not found in the DB', 404
            response.pop('_id', None)
            return response, 200
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return e, 500
    
    def update_department_in_db(self, department_id, department_data, remove_flag=False):
        try:
            logging.info(f'\t Inside a Update Department By ID Function --> Models.py')
            _, department_presence_status_code = self.get_specific_department_from_db(department_id)
            if department_presence_status_code != 200:
                logging.error(f'\t Department not found in the DB')
                return 'Department not found in the DB', 404
            if remove_flag:
                self.departmentCollection.update_one({'departmentID': department_id}, department_data)
                return 'Department updated successfully', 200
            self.departmentCollection.update_one({'departmentID': department_id}, {'$set': department_data})
            return 'Department updated successfully', 200
            
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return e, 500
        
    def delete_department_from_db(self, department_id):
        try:
            logging.info(f'\t Inside a Delete Department By ID Function --> Models.py')
            department_data, department_presence_status_code = self.get_specific_department_from_db(department_id)
            if department_presence_status_code != 200:
                logging.error(f'\t Department not found in the DB')
                return 'Department not found in the DB', 404
            employee_ids = department_data.get('employeeIDs', [])
            for employee_id in employee_ids:
                self.delete_employee_from_db(employee_id)
            result = self.departmentCollection.delete_one({'departmentID': department_id})
            if result.deleted_count == 1:
                logging.info(f'\t Department ID is deleted successfully from the Department DB')
                return 'Department deleted successfully', 204
        except Exception as e:
            logger.error(f'\t Error: {e} -->  Returned 500 Internal Server Error')
            return str(e), 500
       
    def get_all_departments_from_db(self):
        try:
            logging.info(f'\t Inside Get All Departments Function --> Models.py')
            departments = list(self.departmentCollection.find())
            if not departments:
                logging.error(f'\t No employees found in the DB')
                return 'No employees found in the DB', 404
            for department in departments:
                department.pop('_id', None)
            logging.info(f'\t Employees fetched successfully')
            return departments, 200
        except Exception as e:
            logging.error(f'\t Error: {e} --> Returned 500 Internal Server Error')
            return str(e), 500
        

# Initialize the DB class
mongo_db = DB()