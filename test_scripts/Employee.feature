Feature: Employee management

 Scenario: Adding a Department
    Given the user is logged in
    When the user makes a post request to add the Department details to DB
    Then the Department details should be added to the Department Collection and should return 201 Created status code

  Scenario: Getting a Department details
    Given the user is logged in 
    When the user makes a get request to Department routes
    Then the Department details should be displayed and should return 200 status code
  
  Scenario: Updating a Department details
    Given the user is logged in 
    When the user makes a put request to update the Department details
    Then the Department details should be updated in the Department Collection and should return 200 Updated status code  
  


  Scenario: Adding a Employee to the DB
    Given the user is logged in
    When the user makes a post request to add the Employee details to DB
    Then the Employee details should be added to the Employee Collection and should return 201 Created status code
  
  Scenario: Getting a Employee details from the DB
    Given the user is logged in
    When the user makes a get request to Employee routes
    Then the Employee details should be displayed and should return 200 status code

  Scenario: Updating a Employee details
    Given the user is logged in 
    When the user makes a put request to update the Employee details
    Then the Employee details should be updated in the Employee Collection and should return 200 Updated status code
  


  Scenario: User with missing fields
    Given the user is logged in
    When the user makes a post request to the employee details having missing details
    Then the Employee details should have error and return 400 Bad request

  Scenario: User with wrong data types
    Given the user is logged in 
    When the user makes a post request to the employee details having wrong datatypes in the fields
    Then the user fields having a wrong datatypes and return 400 Bad request
  
  Scenario: User with additional fields
    Given the user is logged in
    When the user makes a post request having a additional field in the employee details
    Then the employee details having a additional/excess field should return 400 Bad request

  Scenario: Employee details having a wrong employeeID
    Given the user is logged in 
    When the user makes a get request having a wrong employeeID
    Then if the EmployeeID is wrong then return 404 not found error
  
  Scenario: updating Employee details having additional field
    Given the user is logged in 
    When the user makes a put request having a additional fields
    Then if the employee details having an excess field than required then return 400 bad request

  Scenario: Department collection has no department details found
    Given the user is logged in
    When the user makes a put request but no department details found
    Then the department details should not match with the department collection and should return 404 not found error

  Scenario: Delete employee who does not exist
    Given: the user is logged in 
    When the user makes a delete request for the employeeID which doesnt exist
    Then if the employee details doesnt exist return 404 not found

  Scenario: Deleting a Employee details
    Given the user is logged in
    When the user makes a delete request to remove the employee details
    Then the Employee details should be deleted and should return 204 status code 

  Scenario: Deleting a Department details
    Given the user is logged in
    When the user makes a delete request to remove the Department details
    Then the Department details should be deleted and should return 204 status code 
  
  Scenario: Deleting a Department details which is not found
    Given the user is logged in
    When the user makes a delete request to remove the Department details which is not found
    Then the Department details doesnt exist and should return 404 status code 
