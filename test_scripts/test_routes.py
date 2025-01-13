import pytest
from pytest_bdd import scenarios, given, when, then
import requests
import faker
import random

fake = faker.Faker()

# Define the scenarios
scenarios('user.feature')
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


#User get request feature
@when('the user makes a get request to Employee routes')
def get_employee_by_id():
    response = get_request(route=url + employee_route + "?employeeID=" + pytest.employee_creation_response.json().get('employeeID'))
    pytest.employee_details_response = response

@then('the Employee details should be displayed and should return 200 status code')
def check_employee_details():
    assert pytest.employee_details_response.status_code == 200, pytest.employee_details_response.text
    assert pytest.employee_details_response.json().get('name') == pytest.employee_name


#User update request feature
@when('the user makes a put request to update the Employee details')
def update_employee():
    payload = {
            "salary": random.randint(20000, 100000)
        }
    response = put_request(route=url + employee_route +'/'+ pytest.employee_creation_response.json().get('employeeID'), data=payload)
    pytest.employee_update_response = response

@then('the Employee details should be updated in the Employee Collection and should return 200 Updated status code')
def check_updated_employee_details():
    assert pytest.employee_update_response.status_code == 200, pytest.employee_update_response.text
    assert pytest.employee_update_response.json().get('message') == 'Employee updated successfully', pytest.employee_update_response.text


#User delete request feature
@when('the user makes a delete request to remove the employee details')
def delete_user():
    response = delete_request(route=url + employee_route +'/'+ pytest.employee_creation_response.json().get('employeeID'))
    pytest.employee_details_response = response

@then('the Employee details should be deleted and should return 204 status code')
def check_deleted_user_details():
    assert pytest.employee_details_response.status_code == 204, pytest.employee_details_response.text


#DEPARTMENT POST REQUEST FEATURE
#@given('the user is logged in')
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
    # assert pytest.department_creation_response.json().get('departmentID') == pytest.department_ID


#DEPARTMENT GET REQUEST FEATURE
@when('the user makes a get request to Department routes')
def get_department_by_id():
    response = get_request(route=url + department_route + "?departmentID=" + pytest.department_creation_response.json().get('departmentID'))
    pytest.department_details_response = response

@then('the Department details should be displayed and should return 200 status code')
def check_department_details():
    assert pytest.department_details_response.status_code == 200, pytest.department_details_response.text
    assert pytest.department_details_response.json().get('name') == pytest.dept_name

#DEPARTMENT UPDATE REQUEST FEATURE
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

#DEPARTMENT DELETE REQUEST FEATURE
@when('the user makes a delete request to remove the Department details')
def delete_department():
    response = delete_request(route=url + department_route + '/'+ pytest.department_creation_response.json().get('departmentID'))
    pytest.department_details_response = response

@then('the Department details should be deleted and should return 204 status code')
def check_deleted_deoartment_details():
    assert pytest.department_details_response.status_code == 204, pytest.department_details_response.text

#--------------------    negative scenarios ------------------------------

@when('the user makes a post request to the employee details having missing details')
def missing_field():
    payload = {
            "name": fake.name()
    }
    response = post_request(route=url + employee_route, data=payload)
    pytest.missing_employee_details = response

@then('the Employee details should have error and return 400 Bad request')
def check_missing_fields():
    assert pytest.missing_employee_details.status_code == 400, pytest.missing_employee_details.text


@when('the user makes a post request to the employee details having wrong datatypes in the fields')
def wrong_type():
    payload = {
        "name": 37378
    }
    response = post_request(route=url + employee_route, data=payload)
    pytest.wrong_data_type = response

@then('the user fields having a wrong datatypes and return 400 Bad request')
def check_data_type():
    assert pytest.wrong_data_type.status_code == 400, pytest.wrong_data_type.text


@when('the user makes a post request having a additional field in the employee details')
def additional_field():
    payload = {
        "phoneNo": 79798989837
    }
    response = post_request(route=url + employee_route, data=payload)
    pytest.additional_employee_field = response

@then('the employee details having a additional/excess field should return 400 Bad request')
def check_for_additional_field():
    assert pytest.additional_employee_field.status_code == 400, pytest.additional_employee_field.text


@when('the user makes a get request having a wrong employeeID')
def wrong_request():
    response = get_request(route=url + employee_route + "?employeeID=" + pytest.employee_creation_response.json().get('employeeID')+"ade")
    pytest.employee_details_response = response

@then('if the EmployeeID is wrong then return 404 not found error')
def check_employee_details():
    assert pytest.employee_details_response.status_code == 404, pytest.employee_details_response.text
   # assert pytest.employee_details_response.json().get('name') == pytest.dept_name
    

@when('the user makes a put request having a additional fields') 
def update_additional_field():
    payload = {
            "phoneNO" : 8787989283
    }
    response = put_request(route=url + employee_route + '/' + pytest.employee_creation_response.json().get('employeeID'), data=payload)
    pytest.employee_update_response = response

@then('if the employee details having an excess field than required then return 400 bad request')
def check_updated_details():
    assert pytest.employee_update_response.status_code == 400, pytest.employee_update_response.text


@when('the user makes a delete request for the employeeID which doesnt exist')
def delete_non_exist_id():
    response = delete_request(route=url + employee_route + '/'+ pytest.employee_creation_response.json().get('employeeID')+"67")
    pytest.employee_non_exist_data = response

@then('if the employee details doesnt exist return 404 not found')
def check_deleted_employee_details():
    assert pytest.employee_non_exist_data.status_code == 404, pytest.employee_non_exist_data.text

@when('the user makes a put request but no department details found')
def no_department_found():
    payload ={
        "location": fake.city()
    }
    response = put_request(route=url + department_route + '/' + pytest.department_creation_response.json().get('departmentID') + '456', data=payload)
    pytest.department_not_found = response

@then('the department details should not match with the department collection and should return 404 not found error')
def check_department_updation():
    assert pytest.department_not_found.status_code == 404, pytest.department_not_found.text
    #assert pytest.department_not_found.json().get('message')

@when('the user makes a delete request to remove the Department details which is not found')
def delete_non_exist_dept_id():
    response = delete_request(route=url + department_route + '/'+ pytest.department_creation_response.json().get('departmentID')+ "sc374")
    pytest.department_non_exist_data = response

@then('the Department details doesnt exist and should return 404 status code')
def check_deleted_department_details():
    assert pytest.department_non_exist_data.status_code == 404, pytest.department_non_exist_data.text