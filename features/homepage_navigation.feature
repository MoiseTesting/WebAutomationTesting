# Feature files use Gherkin syntax to describe the behavior we want to test
# They should be written in a way that non-technical stakeholders can understand
# The following three lines describe the business value of this feature
Feature: Homepage Navigation
    As a user
    I want to access the practice automation website
    So that I can interact with the testing playground

    # A scenario describes a specific test case
    # Each scenario should be independent and able to run on its own
    Scenario: Successfully accessing the homepage
        # Given steps set up the initial state
        Given I launch the browser
        # When steps describe the action being taken
        When I navigate to the practice automation website
        # Then steps verify the expected outcome
        Then I should see the homepage successfully loaded
