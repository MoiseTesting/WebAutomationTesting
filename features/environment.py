"""
Behave environment configuration file
Handles test setup and teardown at different levels
"""
from utilities.driver_factory import DriverFactory
from utilities.config import Config
import logging
import os
from datetime import datetime
logger = logging.getLogger(__name__)

# Ensure the logs directory exists
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/test_run.log", mode="w"),
        logging.StreamHandler()
    ]
)


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
        
        # Maximize the window size for better visibility
        if not Config.HEADLESS:
            context.driver.maximize_window()
            window_size = context.driver.get_window_size()
            logger.info(f"Scenario window size: {window_size['width']}x{window_size['height']}")
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
        if scenario.status == "failed" and hasattr(context, "driver"):
            # Save screenshot for failed scenarios
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            screenshot_name = f"{scenario.name.replace(' ', '_')}_{timestamp}.png"
            screenshots_dir = "WAT/screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)
            context.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot for failed scenario saved at: {screenshot_path}")
        
        if hasattr(context, 'driver'):
            context.driver.quit()
    except Exception as e:
        logger.error(f"Error closing browser: {str(e)}")
