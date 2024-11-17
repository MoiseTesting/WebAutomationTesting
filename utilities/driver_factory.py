# utilities/driver_factory.py
"""
Factory class for WebDriver creation and management.
Handles browser driver setup, configuration, and cleanup.
Supports both local and CI/CD environments.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
            # Get browser options from config.
            options = Config.get_browser_options()
            
            # Add CI/CD specific options when running in GitHub Actions
            if os.getenv('GITHUB_ACTIONS'):
                logger.info("Running in GitHub Actions - adding CI/CD specific options")
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
            
            # Setup ChromeDriver with automatic version management
            service = Service(ChromeDriverManager().install())
            
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
            
            # Set window size for consistency if not headless
            if not Config.HEADLESS:
                driver.set_window_size(1920, 1080)
            
            return driver
            
        except Exception as e:
            # Log detailed error information
            logger.error(f"Failed to create driver: {str(e)}")
            raise

    # Future enhancements:
    # - Support for other browsers (Firefox, Edge, etc.)
    # - Custom driver configurations per environment
    # - Remote WebDriver support
    # - Container-based browser support
    # - Proxy configuration support
    # - Custom capabilities configuration