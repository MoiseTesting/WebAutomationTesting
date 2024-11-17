"""
Configuration management for the test framework.
Handles environment variables, test settings, and provides
configuration access to other framework components.
"""
import os
from dotenv import load_dotenv
import logging
from selenium.webdriver.chrome.options import Options
load_dotenv()
# Set up logging
logger = logging.getLogger(__name__)
class Config:
    """
    Configuration class to manage test environment settings and provide
    environment-specific configurations.
    """
    

    # Environment settings
    ENV = os.getenv('TEST_ENV', 'qa').lower()
    
    # Base URLs for different environments
    BASE_URLS = {
        'dev': 'https://dev.practice-automation.com',
        'qa': 'https://play1.automationcamp.ir/index.html',
        'prod': 'https://prod.practice-automation.com'
    }
    
    # Browser configurations
    BROWSER = os.getenv('BROWSER', 'chrome').lower()
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    
    # Timeouts
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10'))
    EXPLICIT_TIMEOUT = int(os.getenv('EXPLICIT_TIMEOUT', '20'))
    
    @classmethod
    def get_base_url(cls):
        """
        Get the base URL for the current environment.
        
        Returns:
            str: The base URL for the current environment
        """
        url = cls.BASE_URLS.get(cls.ENV, cls.BASE_URLS['qa'])
        logger.info(f"Using URL for {cls.ENV} environment: {url}")
        return url
    @classmethod
    def get_browser_options(cls):
        """
        Get browser options based on configuration
        
        Returns:
            Options: Configured Chrome options object
        """
        options = Options()
        
        # Add headless mode if configured
        if cls.HEADLESS:
            options.add_argument('--headless')
            
        # Add standard Chrome arguments
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-infobars')
        
        return options

    @staticmethod
    def get_env_name():
        """Get a formatted string of the current environment name"""
        return Config.ENV.upper()