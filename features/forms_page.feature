Feature: Forms Page Functionality

  Scenario: Successfully navigating to forms page
    When I navigate to the practice automation website
    Then I should see the homepage successfully loaded
    When I navigate to the forms page
    Then I should see the forms page successfully loaded

  Scenario: Fill out and submit the form
    Given I am on the forms page
    When I fill out the basic form controls
    Then I submit the form

Scenario: Verify file download functionality
    Given I am on the forms page
    When I click on the Download File link
    Then the file should be downloaded successfully

Scenario: Fill out non-English labels and locators
    Given I am on the forms page
    When I fill out the non-English text field
    And I select the non-English checkboxes
    Then the non-English elements should reflect the changes
     
