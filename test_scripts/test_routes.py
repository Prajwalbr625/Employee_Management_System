import pytest
from pytest_bdd import scenarios, given, when, then
import requests
import faker
import random

fake = faker.Faker()

# Define the scenarios
scenarios('Employee.feature')
# scenarios('department.feature')

url = 'http://localhost:8080'
employee_route = '/employees'
department_route = '/departments'

# departmentID = "76cc9481-b4cd-47af-841b-ee0f4cb07b57"

def get_request(route):
    return requests.get(route)

def post_request(route, data):
    return requests.post(route, json=data)

def put_request(route, data):
    return requests.put(route, json=data)

def delete_request(route):
    return requests.delete(route)


# User post feature steps
@given('the user is logged in')
def user_is_logged_in():
    pass


# Adding a Employee to the DB
@when('the user makes a post request to add the Employee details to DB')
def add_employee():
    department_payload={
        "name": fake.company(),
        "location": fake.city()
    }
    response = post_request(route=url + department_route, data=department_payload)
    if response.status_code == 201:
        pytest.department_ID = response.json().get("departmentID")
    else:
        pytest.error("department is not created")

    pytest.employee_name = fake.name()
    payload = {
            "name": pytest.employee_name,
            "age": 22,
            "sex": "Male",
            "departmentID": pytest.department_ID,
            "position": "SDE-1 Validation",
            "salary": 100000
        }
    response = post_request(route=url + employee_route, data=payload)
    pytest.employee_creation_response = response

@then('the Employee details should be added to the Employee Collection and should return 201 Created status code')
def check_employee_added():
    assert pytest.employee_creation_response.status_code == 201, pytest.employee_creation_response.text
    assert pytest.employee_creation_response.json().get('message') == 'Employee added successfully', pytest.employee_creation_response.text


# Getting a Employee details from the DB
@when('the user makes a get request to Employee routes')
def get_employee_by_id():
    response = get_request(route=url + employee_route + "?employeeID=" + pytest.employee_creation_response.json().get('employeeID'))
    pytest.employee_details_response = response

@then('the Employee details should be displayed and should return 200 status code')
def check_employee_details():
    assert pytest.employee_details_response.status_code == 200, pytest.employee_details_response.text
    assert pytest.employee_details_response.json().get('name') == pytest.employee_name


# Deleting a Employee details from the DB
@when('the user makes a delete request to remove the employee details')
def delete_user():
    response = delete_request(route=url + employee_route +'/'+ pytest.employee_creation_response.json().get('employeeID'))
    pytest.employee_details_response = response

@then('the Employee details should be deleted and should return 204 status code')
def check_deleted_user_details():
    assert pytest.employee_details_response.status_code == 204, pytest.employee_details_response.text

# Adding a Department to the DB
@when('the user makes a post request to add the Department details to DB')
def add_department():
    payload = {
            "name" : fake.company(),
            "location" : fake.city()
    }
    pytest.dept_name = payload.get('name')
    response = post_request(route=url + department_route, data=payload) 
    if response.status_code == 201:
        pytest.department_ID = response.json().get("departmentID")
    else:
        pytest.fail("department is not created")
    pytest.department_creation_response = response

@then('the Department details should be added to the Department Collection and should return 201 Created status code')
def check_department_details():
    assert pytest.department_creation_response.status_code == 201, pytest.department_creation_response.text


# Getting a Department details from the DB
@when('the user makes a get request to Department routes')
def get_department_by_id():
    response = get_request(route=url + department_route + "?departmentID=" + pytest.department_creation_response.json().get('departmentID'))
    pytest.department_details_response = response

@then('the Department details should be displayed and should return 200 status code')
def check_department_details():
    assert pytest.department_details_response.status_code == 200, pytest.department_details_response.text
    assert pytest.department_details_response.json().get('name') == pytest.dept_name

# Updating a Department details in the DB
@when('the user makes a put request to update the Department details')
def update_department():
    payload = {
            "location" : fake.city()
    }
    response = put_request(route=url + department_route + '/' + pytest.department_creation_response.json().get('departmentID'), data=payload)
    pytest.department_update_response = response

@then('the Department details should be updated in the Department Collection and should return 200 Updated status code')
def check_department_details():
    assert pytest.department_update_response.status_code == 200, pytest.department_update_response.text
    assert pytest.department_update_response.json().get('message') == 'Department updated successfully', pytest.department_update_response.text

# Deleting a Department details from the DB
@when('the user makes a delete request to remove the Department details')
def delete_department():
    response = delete_request(route=url + department_route + '/'+ pytest.department_creation_response.json().get('departmentID'))
    pytest.department_details_response = response

@then('the Department details should be deleted and should return 204 status code')
def check_deleted_department_details():
    assert pytest.department_details_response.status_code == 204, pytest.department_details_response.text
