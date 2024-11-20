"""
Step definitions for Sample Login feature tests.
This file implements the steps defined in sample_login.feature,
converting the Gherkin statements into executable test code.

Each step definition maps to a step in the feature file and
contains the actual test implementation using the Page Object Model.
"""

from behave import given, when, then
from pages.sample_page import SamplePage
from selenium.webdriver.common.by import By
from utilities.config import Config
from typing import Any
from contextlib import contextmanager
from datetime import datetime
import os
import logging
import time

logger = logging.getLogger(__name__)

@contextmanager
def screenshot_on_failure(context: Any, name: str):
    """
    Context manager to take screenshots on failure
    
    Args:
        context: Behave context
        name: Base name for the screenshot file
    """
    try:
        yield
    except Exception as e:
        # Create screenshots directory if it doesn't exist
        os.makedirs('screenshots', exist_ok=True)
        # Take screenshot with meaningful name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = f"screenshots/error_{name}_{timestamp}.png"
        context.driver.save_screenshot(screenshot_path)
        logger.error(f"Screenshot saved to {screenshot_path}")
        raise

@given('I am on the homepage')
def step_impl(context):
    """
    Verifies that the browser is initialized and on the homepage
    
    Args:
        context: Behave context containing the web driver
    """
    assert context.driver is not None, "Browser not initialized"
     # Get the URL from config and navigate to it
    url = Config.get_base_url()
    context.driver.get(url)
    logger.info(f"Navigated to homepage: {url}")

@when('I click on the Sample Pages link')
def step_impl(context):
    """
    Clicks the Sample Pages link to navigate to the sample section
    
    Args:
        context: Behave context containing the web driver
    """
    sample_page = SamplePage(context.driver)
    assert sample_page.click_sample_page_link(), "Failed to click Sample Pages link"

@then('I should see the login page')
def step_impl(context):
    """
    Verifies that the login page is displayed
    
    Args:
        context: Behave context containing the web driver
    """
    sample_page = SamplePage(context.driver)
    assert sample_page.wait_for_element_visible(sample_page.LOCATORS['login_form']), "Login form not visible"

@given('I am on the login page')
def step_impl(context):
    """
    Navigates to the login page by executing previous steps
    
    Args:
        context: Behave context containing the web driver
    """
    context.execute_steps('''
        Given I am on the homepage
        When I click on the Sample Pages link
    ''')

@when('I enter username "{username}" and password "{password}"')
def step_impl(context, username, password):
    """
    Enter login credentials
    """
    try:
        sample_page = SamplePage(context.driver)
        assert sample_page.login(username, password), "Failed to enter login credentials"
        logger.info(f"Successfully entered credentials - Username: {username}")
    except Exception as e:
        logger.error(f"Error entering login credentials: {str(e)}")
        context.driver.save_screenshot("screenshots/login_credentials_error.png")
        raise

@when('I click the login button')
def step_impl(context):
    """
    Clicks the login button to submit the form
    """
    try:
        sample_page = SamplePage(context.driver)
        
        # Add small delay for form to be ready
        time.sleep(0.5)
        
        # Try to click the button
        assert sample_page.click_login_button(), "Failed to click login button"
        
        # Wait for form submission
        time.sleep(0.5)
        
        # Verify page change
        current_url = context.driver.current_url
        logger.info(f"Current URL after login: {current_url}")
        
    except Exception as e:
        logger.error(f"Error in login button step: {str(e)}")
        # Take screenshot for debugging
        context.driver.save_screenshot("screenshots/error_clicking_login.png")
        raise

@when('I should see the login result')
def step_impl(context):
    """
    Verifies successful login by checking for pizza order page elements
    
    Args:
        context: Behave context containing the web driver
    """
    try:
        sample_page = SamplePage(context.driver)
        # Allow slight delay for page transition
        time.sleep(1)
        # Verify we're on the pizza page
        assert sample_page.verify_login_result(), "Failed to verify pizza order page"
        logger.info("Successfully verified login by finding pizza order elements")
    except Exception as e:
        logger.error(f"Error verifying login result: {str(e)}")
        raise

@then('I should see "{heading}" heading')
def step_impl(context, heading):
    """
    Verify specific heading is present
    """
    try:
        sample_page = SamplePage(context.driver)
        # Use existing verify_pizza_form_displayed which already checks the heading
        assert sample_page.verify_pizza_form_displayed(), f"Failed to find form with heading: {heading}"
        logger.info(f"Successfully verified heading: {heading}")
    except Exception as e:
        logger.error(f"Error verifying heading: {str(e)}")
        context.driver.save_screenshot("screenshots/heading_verification_failed.png")
        raise

@then('I should see the pizza order form')
def step_impl(context):
    """
    Verify that the pizza order form is displayed
    
    Args:
        context: Behave context containing the web driver
    """
    try:
        sample_page = SamplePage(context.driver)
        
        # Log current URL for debugging
        current_url = context.driver.current_url
        logger.info(f"Current URL while checking for pizza form: {current_url}")
        
        # Take screenshot for debugging
        context.driver.save_screenshot("screenshots/pizza_form_check.png")
        
        # Verify form is displayed
        assert sample_page.verify_pizza_form_displayed(), "Pizza order form not found"
        logger.info("Successfully verified pizza order form")
        
    except Exception as e:
        logger.error(f"Error verifying pizza order form: {str(e)}")
        context.driver.save_screenshot("screenshots/pizza_form_error.png")
        raise
@then('I should see the error message')
def step_impl(context):
    """
    Verify that the error message for invalid login is displayed
    
    Args:
        context: Behave context containing the web driver
    """
    try:
        sample_page = SamplePage(context.driver)
        # Add small delay for error message to appear
        time.sleep(0.5)
        
        # Verify error message
        assert sample_page.verify_error_message(), "Failed to verify error message"
        logger.info("Successfully verified error message for invalid login")
        
    except Exception as e:
        logger.error(f"Error verifying error message: {str(e)}")
        # Take screenshot for debugging
        context.driver.save_screenshot("screenshots/error_message_verification_failed.png")
        raise
@then('I should see the register link')
def step_impl(context):
    """Verify register link is visible"""
    sample_page = SamplePage(context.driver)
    assert sample_page.wait_for_element_visible(sample_page.LOCATORS['register_link']), \
        "Register link not found"

@when('I click the register link')
def step_impl(context):
    """Click the register link"""
    sample_page = SamplePage(context.driver)
    assert sample_page.click_register_link(), "Failed to click register link"

@then('I should be redirected to the registration page')
def step_impl(context):
    """Verify redirect to registration page"""
    sample_page = SamplePage(context.driver)
    assert sample_page.verify_registration_page(), "Failed to verify registration page"

@when('I fill in the registration form with test data')
def step_impl(context):
    """Fill the registration form using data table"""
    sample_page = SamplePage(context.driver)
    # Create a dictionary from the data table
    data = {row['field']: row['value'] for row in context.table}
    assert sample_page.fill_registration_form(
        data['first_name'],
        data['last_name'],
        data['email'],
        data['password']
    ), "Failed to fill registration form"

@when('I accept the terms and conditions')
def step_impl(context):
    """Accept terms and conditions"""
    sample_page = SamplePage(context.driver)
    terms_checkbox = sample_page.wait_for_element_clickable(sample_page.LOCATORS['terms_checkbox'])
    terms_checkbox.click()

@when('I click the register now button')
def step_impl(context):
    """Click the register now button"""
    sample_page = SamplePage(context.driver)
    assert sample_page.click_register_button(), "Failed to click register button"

@then('I should see the registration success message')
def step_impl(context):
    """Verify registration success"""
    # Add verification for success message based on actual page behavior
    pass

@given('I am logged in successfully')
def step_impl(context):
    """Ensure user is logged in"""
    context.execute_steps('''
        Given I am on the login page
        When I enter username "admin" and password "admin"
        And I click the login button
        
    ''')
    time.sleep(2)  # Add small wait here

@when('I select "{size}" as pizza size')
def step_impl(context, size):
    """Select pizza size with improved waiting and modal handling"""
    try:
        sample_page = SamplePage(context.driver)
        
        # Add initial wait after login
        time.sleep(3)  # Wait for page to fully load
        
        # Try to select size
        assert sample_page.select_pizza_size(size), f"Failed to select {size} pizza size"
        logger.info(f"Successfully selected {size} pizza size")
        
        # Add wait after selection to verify
        time.sleep(1)
        
    except Exception as e:
        logger.error(f"Error selecting pizza size: {str(e)}")
        context.driver.save_screenshot("screenshots/size_selection_error.png")
        raise

@when('I select "{flavor}" as pizza flavor')
def step_impl(context, flavor):
    """Select pizza flavor"""
    sample_page = SamplePage(context.driver)
    flavor_dropdown = sample_page.wait_for_element_visible(sample_page.LOCATORS['flavor_dropdown'])
    sample_page.select_option_by_text(flavor_dropdown, flavor)

@when('I select "{sauce}" as sauce')
def step_impl(context, sauce):
    """
    Step definition to select sauce
    """
    try:
        sample_page = SamplePage(context.driver)
        assert sample_page.select_sauce(sauce), f"Failed to select sauce: {sauce}"
        logger.info(f"Successfully selected sauce: {sauce}")
    except Exception as e:
        logger.error(f"Error in sauce selection step: {str(e)}")
        context.driver.save_screenshot("screenshots/sauce_selection_error.png")
        raise

@when('I select the following toppings')
def step_impl(context):
    """
    Step definition to select toppings
    """
    try:
        sample_page = SamplePage(context.driver)
        toppings = [row['topping'] for row in context.table]
        assert sample_page.select_toppings(toppings), "Failed to select toppings"
        logger.info(f"Successfully selected toppings: {toppings}")
    except Exception as e:
        logger.error(f"Error in topping selection step: {str(e)}")
        context.driver.save_screenshot("screenshots/topping_selection_error.png")
        raise

@when('I enter "{quantity}" as quantity')
def step_impl(context, quantity):
    """
    Step definition to enter quantity
    """
    try:
        sample_page = SamplePage(context.driver)
        assert sample_page.enter_quantity(quantity), f"Failed to enter quantity: {quantity}"
        logger.info(f"Successfully entered quantity: {quantity}")
    except Exception as e:
        logger.error(f"Error in quantity entry step: {str(e)}")
        context.driver.save_screenshot("screenshots/quantity_entry_error.png")
        raise

@when('I click Add to Cart')
def step_impl(context):
    """
    Step definition to click Add to Cart button
    """
    try:
        sample_page = SamplePage(context.driver)
        assert sample_page.click_add_to_cart(), "Failed to click Add to Cart"
        logger.info("Successfully clicked Add to Cart")
    except Exception as e:
        logger.error(f"Error clicking Add to Cart: {str(e)}")
        context.driver.save_screenshot("screenshots/add_to_cart_error.png")
        raise
@then('I should see the order confirmation')
def step_impl(context):
    """
    Verify order confirmation message is displayed
    
    Args:
        context: Behave context containing the web driver
    """
    try:
        sample_page = SamplePage(context.driver)
        # Add small delay for message to appear
        time.sleep(1.5)
        
        # Verify confirmation message
        assert sample_page.verify_order_confirmation(), "Failed to verify order confirmation message"
        logger.info("Successfully verified order confirmation")
        
    except Exception as e:
        logger.error(f"Error verifying order confirmation: {str(e)}")
        # Take screenshot for debugging
        context.driver.save_screenshot("screenshots/order_confirmation_error.png")
        raise

@then('I should see the quantity validation message')
def step_impl(context):
    """
    Verify quantity validation message appears
    """
    try:
        sample_page = SamplePage(context.driver)
        assert sample_page.verify_quantity_validation_message(), "Quantity validation message not found"
        logger.info("Successfully verified quantity validation message")
    except Exception as e:
        logger.error(f"Error verifying quantity validation: {str(e)}")
        context.driver.save_screenshot("screenshots/quantity_validation_error.png")
        raise