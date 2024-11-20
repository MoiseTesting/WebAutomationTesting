
"""
Behave environment configuration
"""
from utilities.driver_factory import DriverFactory
from utilities.config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def before_all(context):
    """
    Setup before all tests
    """
    logger.info(f"Starting tests in {Config.TEST_ENV} environment")
    logger.info(f"Base URL: {Config.BASE_URL}")

def before_scenario(context, scenario):
    """
    Setup before each scenario
    """
    try:
        context.driver = DriverFactory.get_driver()
    except Exception as e:
        logger.error(f"Failed to start browser: {str(e)}")
        raise

def after_scenario(context, scenario):
    """
    Cleanup after each scenario
    """
    try:
        if hasattr(context, 'driver'):
            context.driver.quit()
    except Exception as e:
        logger.error(f"Error closing browser: {str(e)}")
