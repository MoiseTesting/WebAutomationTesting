
"""
Configuration management for the test framework
"""
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration management class"""
    
    # Initialize configuration
    @classmethod
    def init(cls):
        # Load environment variables
        load_dotenv()
        
        # Environment settings
        cls.TEST_ENV = os.getenv('TEST_ENV', 'qa')
        cls.BASE_URL = os.getenv('BASE_URL', 'https://play1.automationcamp.ir/index.html')
        cls.HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
        
        # Browser settings
        cls.BROWSER = os.getenv('BROWSER', 'chrome')
        
        # Timeouts
        cls.DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', 10))
        cls.EXPLICIT_TIMEOUT = int(os.getenv('EXPLICIT_TIMEOUT', 20))
        
        logger.info(f"Initialized configuration for {cls.TEST_ENV} environment")
    
    @classmethod
    def get_browser_options(cls):
        """
        Get Chrome options based on configuration
        
        Returns:
            Options: Configured Chrome options
        """
        options = Options()
        
        # Basic options
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        
        # Add headless mode if configured
        if cls.HEADLESS:
            options.add_argument('--headless=new')
        
        return options
    
    @classmethod
    def get_environment_url(cls):
        """
        Get the base URL for the current environment
        
        Returns:
            str: Base URL for current environment
        """
        logger.info(f"Using URL for {cls.TEST_ENV} environment: {cls.BASE_URL}")
        return cls.BASE_URL

# Initialize configuration when module is loaded
Config.init()
