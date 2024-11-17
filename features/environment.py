# features/environment.py
from utilities.driver_factory import DriverFactory
from utilities.config import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def before_all(context):
    """Initialize test configuration"""
    context.config = Config
    logger.info(f"Starting tests in {Config.ENV} environment")
    logger.info(f"Base URL: {Config.get_base_url()}")

def before_scenario(context, scenario):
    """
    Set up WebDriver before each scenario
    
    Args:
        context: Behave context object
        scenario: Current scenario being executed
    """
    try:
        context.driver = DriverFactory.get_driver()
        context.driver.implicitly_wait(Config.DEFAULT_TIMEOUT)
        logger.info(f"Started {Config.BROWSER} browser")
    except Exception as e:
        logger.error(f"Failed to start browser: {str(e)}")
        raise

def after_scenario(context, scenario):
    """
    Clean up after each scenario
    
    Args:
        context: Behave context object
        scenario: Current scenario being executed
    """
    try:
        if hasattr(context, 'driver'):
            context.driver.quit()
            logger.info("Browser closed")
    except Exception as e:
        logger.error(f"Failed to close browser: {str(e)}")