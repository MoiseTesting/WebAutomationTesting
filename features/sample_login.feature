Feature: Sample Login Page
    As a user
    I want to test the login functionality
    So that I can verify user authentication works correctly

    Scenario: Successfully navigating to login page
        Given I am on the homepage
        When I click on the Sample Pages link
        Then I should see the login page

    Scenario:  Successful login with valid credentials
        Given I am on the login page
        When I enter username "admin" and password "admin"
        And I click the login button
        And I should see the login result
        Then I should see "Dinesh's Pizza House" heading
        Then I should see the pizza order form

    Scenario: Order a pizza after login
        Given I am logged in successfully
        Then I should see the pizza order form
        When I select "Medium" as pizza size
        And I select "Pepperoni" as pizza flavor
        And I select "Barbeque" as sauce
        And I select the following toppings
        | topping      |
        | Onions    |
        And I enter "6" as quantity
        And I click Add to Cart
        Then I should see the order confirmation

    Scenario: Attempt to order without quantity
        Given I am logged in successfully
        Then I should see the pizza order form
        When I select "Medium" as pizza size
        And I select "Pepperoni" as pizza flavor
        And I select "Barbeque" as sauce
        And I click Add to Cart
        Then I should see the quantity validation message
    
    Scenario: Invalid login attempt
        Given I am on the login page
        When I enter username "wrong" and password "wrong"
        And I click the login button
        Then I should see the error message
    
     Scenario: Complete registration process
        Given I am on the login page
        Then I should see the register link
        When I click the register link
        Then I should be redirected to the registration page
        When I fill in the registration form with test data
            | field      | value           |
            | first_name | John            |
            | last_name  | Doe             |
            | email      | test@email.com  |
            | password   | Test123!        |
        And I accept the terms and conditions
        And I click the register now button
        Then I should see the registration success message