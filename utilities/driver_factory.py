# utilities/driver_factory.py
"""
Factory class for WebDriver creation and management.
Handles browser driver setup, configuration, and cleanup.
Supports both local and CI/CD environments.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from utilities.config import Config
import logging
import os

# Set up logging for this module
logger = logging.getLogger(__name__)

class DriverFactory:
    """
    Factory class for creating WebDriver instances
    Handles different environments (local and CI/CD) and configurations
    """
    
    @staticmethod
    def get_driver():
        """
        Create and return a WebDriver instance based on configuration
        
        Returns:
            WebDriver: Configured WebDriver instance for Chrome
            
        Raises:
            Exception: If driver creation fails
        """
        try:
            # Create Chrome options
            options = Options()
            
            # Add required CI/CD specific options
            if os.getenv('GITHUB_ACTIONS'):
                logger.info("Running in GitHub Actions - adding CI/CD specific options")
                options.add_argument('--no-sandbox')
                options.add_argument('--headless')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
            elif Config.HEADLESS:
                options.add_argument('--headless')
            
            # Setup ChromeDriver with specific version manager
            driver_manager = ChromeDriverManager()
            driver_path = driver_manager.install()
            
            logger.info(f"ChromeDriver path: {driver_path}")
            
            # Create service object
            service = Service(executable_path=driver_path)
            
            # Create and configure the driver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            # Log driver creation success
            logger.info(
                f"Created Chrome driver in "
                f"{'headless' if Config.HEADLESS else 'normal'} mode"
            )
            
            return driver
            
        except Exception as e:
            # Log detailed error information
            logger.error(f"Failed to create driver: {str(e)}")
            raise