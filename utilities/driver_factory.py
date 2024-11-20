"""
Factory class for WebDriver creation and management.
Handles browser driver setup, configuration, and cleanup.
Supports both local and CI/CD environments.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utilities.config import Config
import logging
import os

logger = logging.getLogger(__name__)

class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def get_driver():
        """
        Create and return a WebDriver instance
        Handles both local and CI/CD environments
        
        Returns:
            WebDriver: Configured WebDriver instance
        """
        try:
            # Get base browser options from config
            options = Config.get_browser_options()
            
            # Add CI/CD specific options when running in GitHub Actions
            if os.getenv('GITHUB_ACTIONS'):
                logger.info("Running in GitHub Actions - configuring for CI/CD")
                options.add_argument('--no-sandbox')
                options.add_argument('--headless=new')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
            else:
                logger.info("Running in local environment")
                if Config.HEADLESS:
                    options.add_argument('--headless=new')
                    logger.info("Running in headless mode")
                else:
                    logger.info("Running in normal mode")
            
            # Setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # Create and return the driver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            # Set window size for non-headless mode
            if not Config.HEADLESS and not os.getenv('GITHUB_ACTIONS'):
                driver.set_window_size(1920, 1080)
            
            logger.info(f"Created Chrome driver in {'headless' if Config.HEADLESS or os.getenv('GITHUB_ACTIONS') else 'normal'} mode")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to create driver: {str(e)}")
            raise

    @staticmethod
    def is_running_in_ci():
        """Check if running in CI environment"""
        return bool(os.getenv('GITHUB_ACTIONS'))

    # Future enhancements could include:
    # - Support for other browsers (Firefox, Edge, etc.)
    # - Custom driver configurations
    # - Remote WebDriver support
    # - Container-based browser support
