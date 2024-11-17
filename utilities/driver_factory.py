# utilities/driver_factory.py
"""
Factory class for WebDriver creation and management.
Handles browser driver setup, configuration, and cleanup.
"""
# Import necessary selenium modules
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utilities.config import Config
import logging

logger = logging.getLogger(__name__)

class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def get_driver():
        """
        Create and return a WebDriver instance
        
        Returns:
            WebDriver: Configured WebDriver instance
        """
        try:
            # Get browser options from config
            options = Config.get_browser_options()
            
            # Setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # Create and return the driver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            logger.info(f"Created Chrome driver in {'headless' if Config.HEADLESS else 'normal'} mode")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to create driver: {str(e)}")
            raise

    # Future enhancements could include:
    # - Support for other browsers (Firefox, Edge, etc.)
    # - Custom driver configurations
    # - Remote WebDriver support
    # - Container-based browser support