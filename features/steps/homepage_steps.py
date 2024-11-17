"""
Step definitions for homepage-related test scenarios.
Implements the steps defined in homepage_navigation.feature.
"""
from behave import given, when, then
from pages.home_page import HomePage
from utilities.config import Config
import logging

# Set up logging
logger = logging.getLogger(__name__)

@given('I launch the browser')
def step_impl(context):
    """
    Verify that the browser has launched successfully.
    
    Args:
        context: Behave context object containing WebDriver instance
    """
    assert context.driver is not None, "Browser failed to launch"
    logger.info("Browser launched successfully")

@when('I navigate to the practice automation website')
def step_impl(context):
    """
    Navigate to the website using the configured URL from Config.
    
    Args:
        context: Behave context object containing WebDriver instance
    """
    # Use get_base_url() method instead of directly accessing BASE_URL
    url = Config.get_base_url()
    context.driver.get(url)
    logger.info(f"Navigated to URL: {url}")

@then('I should see the homepage successfully loaded')
def step_impl(context):
    """
    Verify that the homepage has loaded successfully.
    Includes detailed error logging for troubleshooting.
    
    Args:
        context: Behave context object containing WebDriver instance
    """
    home_page = HomePage(context.driver)
    
    try:
        # Try to verify the page
        if home_page.verify_page_loaded():
            logger.info("Homepage loaded successfully")
            
            # Get and log the page title for verification
            title = home_page.get_page_title()
            if title:
                logger.info(f"Found page title: {title}")
            
            return True
        else:
            raise AssertionError("Homepage verification failed")
            
    except Exception as e:
        logger.error(f"Error verifying homepage: {str(e)}")
        # Log current URL for debugging
        logger.error(f"Current URL: {context.driver.current_url}")
        raise AssertionError("Homepage failed to load")