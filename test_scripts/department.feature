Feature: Department management

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
  
  Scenario: Deleting a Department details
    Given the user is logged in
    When the user makes a delete request to remove the Department details
    Then the Department details should be deleted and should return 204 status code 