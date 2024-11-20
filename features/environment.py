"""
Behave environment configuration file
Handles test setup and teardown at different levels
"""
from utilities.driver_factory import DriverFactory
from utilities.config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def before_all(context):  # type: ignore
    """
    Setup before all tests
    Args:
        context: Behave context object, carries data between steps
    """
    logger.info(f"Starting tests in {Config.TEST_ENV} environment")
    logger.info(f"Base URL: {Config.BASE_URL}")

def before_scenario(context, scenario):  # type: ignore
    """
    Setup before each scenario
    Args:
        context: Behave context object, carries data between steps
        scenario: Current scenario being executed
    """
    try:
        context.driver = DriverFactory.get_driver()
        
        # Double-check window size
        if not Config.HEADLESS:
            # Try to maximize again
            context.driver.maximize_window()
            
            # Get and log window size
            window_size = context.driver.get_window_size()
            logger.info(f"Scenario window size: {window_size['width']}x{window_size['height']}")
            
            # If window is still not full size, set it explicitly
            if window_size['width'] < 1920:
                context.driver.set_window_size(1920, 1080)
                logger.info("Window size adjusted to 1920x1080")
    
    except Exception as e:
        logger.error(f"Failed to start browser: {str(e)}")
        raise

def after_scenario(context, scenario):  # type: ignore
    """
    Cleanup after each scenario
    Args:
        context: Behave context object, carries data between steps
        scenario: Current scenario that was executed
    """
    try:
        if hasattr(context, 'driver'):
            context.driver.quit()
    except Exception as e:
        logger.error(f"Error closing browser: {str(e)}")
