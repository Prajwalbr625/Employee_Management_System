from pymongo import MongoClient
import app.config as config

class DB:

    def __init__(self):
        self.db = self.setup_db()
        self.employeeCollection = self.db[config.MONGO_EMPLOYEE_COLLECTION_NAME]
        self.departmentCollection = self.db[config.MONGO_DEPARTMENT_COLLECTION_NAME]


    def setup_db(self):
        print(f'\t Inside a Setup DB Function')
        client = MongoClient(config.MONGO_URI)
        self.db = client[config.MONGO_DB_NAME]
        return self.db
        

# ----------------------------------- Employee DB Functions --------------------------------- #

    def add_employee_to_db(self, employee_data):
        result = self.employeeCollection.find_one({"name": employee_data.get('name')})
        if result:
            return 'Employee with the same name already exists, Please provide Different Name', 409
        self.employeeCollection.insert_one(employee_data)
        self.departmentCollection.update_one({'departmentID': employee_data.get('departmentID')}, {'$push': {'employeeIDs': employee_data.get('employeeID')}})
        return 'Employee added successfully', 201

    def get_specific_employee_from_db(self, employee_id):
        response = self.employeeCollection.find_one({"employeeID":employee_id})
        if response is None:
            return 'Employee not found in the DB', 404
        response.pop('_id', None)
        return response, 200
    
    def update_employee_in_db(self, employee_id, employee_data):
        employee_data, employee_presence_status_code = self.get_specific_employee_from_db(employee_id)
        if employee_presence_status_code != 200:
            return 'Employee not found in the DB', 404
        self.employeeCollection.update_one({'employeeID': employee_id}, {'$set': employee_data})
        return 'Employee updated successfully', 200
        
    def delete_employee_from_db(self, employee_id):
        employee_data, employee_presence_status_code = self.get_specific_employee_from_db(employee_id)
        if employee_presence_status_code != 200:
            return 'Employee not found in the DB', 404
        result = self.employeeCollection.delete_one({'employeeID': employee_id})
        if result.deleted_count == 1:
            return 'Employee deleted successfully', 204     

    def get_all_employees_from_db(self):
        employees = list(self.employeeCollection.find())
        if not employees:
            return 'No employees found in the DB', 404
        for employee in employees:
            employee.pop('_id', None)
        return employees, 200


# ------------------------------ Department DB Functions -------------------------------- #
        
    def add_department_to_db(self, department_data):
        response = self.departmentCollection.find_one({'name': department_data.get('name')})
        if response:
            return 'Department with the same name already exists, Please provide Different Name', 409
        self.departmentCollection.insert_one(department_data)
        return 'Department added successfully', 201

    
    def get_specific_department_from_db(self, department_id):
        response = self.departmentCollection.find_one({'departmentID': department_id})
        if response is None:
            return 'Department not found in the DB', 404
        response.pop('_id', None)
        return response, 200

    
    def update_department_in_db(self, department_id, department_data):
        _, department_presence_status_code = self.get_specific_department_from_db(department_id)
        if department_presence_status_code != 200:
            return 'Department not found in the DB', 404
        self.departmentCollection.update_one({'departmentID': department_id}, {'$set': department_data})
        return 'Department updated successfully', 200

        
    def delete_department_from_db(self, department_id):
        message, department_presence_status_code = self.get_specific_department_from_db(department_id)
        if department_presence_status_code != 200:
            return {'message': message}, 404
        result = self.departmentCollection.delete_one({'departmentID': department_id})
        if result.deleted_count == 1:
            return 'Department deleted successfully', 204


    def get_all_departments_from_db(self):
        departments = list(self.departmentCollection.find())
        if not departments:
            return 'Department is not found in the DB', 404
        for department in departments:
            department.pop('_id', None)
        return departments, 200

# Initialize the DB class
mongo_db = DB()