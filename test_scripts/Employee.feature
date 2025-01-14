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

  Scenario: Deleting a Employee details
    Given the user is logged in
    When the user makes a delete request to remove the employee details
    Then the Employee details should be deleted and should return 204 status code 

  Scenario: Deleting a Department details
    Given the user is logged in
    When the user makes a delete request to remove the Department details
    Then the Department details should be deleted and should return 204 status code 
