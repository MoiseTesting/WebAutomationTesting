# utilities/driver_factory.py
"""
Factory class for WebDriver creation and management.
Handles browser driver setup, configuration, and cleanup.
Supports both local and CI/CD environments.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
import os
import tempfile
import urllib.request
import zipfile
import stat

# Set up logging for this module
logger = logging.getLogger(__name__)

class DriverFactory:
    """
    Factory class for creating WebDriver instances
    Handles different environments (local and CI/CD) and configurations
    """
    
    @staticmethod
    def download_chromedriver():
        """
        Download and setup ChromeDriver manually
        
        Returns:
            str: Path to the ChromeDriver executable
        
        Raises:
            Exception: If download or setup fails
        """
        try:
            # Define ChromeDriver URL for latest stable version
            driver_url = "https://storage.googleapis.com/chrome-for-testing-public/stable/linux64/chromedriver-linux64.zip"
            
            # Create a temporary directory for ChromeDriver
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            # Download ChromeDriver zip file
            logger.info(f"Downloading ChromeDriver from {driver_url}")
            urllib.request.urlretrieve(driver_url, zip_path)
            
            # Extract the ChromeDriver from zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Get path to ChromeDriver executable
            chromedriver_path = os.path.join(temp_dir, "chromedriver-linux64", "chromedriver")
            
            # Set executable permissions (Unix/Linux only)
            os.chmod(chromedriver_path, stat.S_IRWXU)
            
            logger.info(f"ChromeDriver installed at: {chromedriver_path}")
            return chromedriver_path
            
        except Exception as e:
            logger.error(f"Failed to download ChromeDriver: {str(e)}")
            raise
    
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
            
            # Configure options based on environment
            if os.getenv('GITHUB_ACTIONS'):
                logger.info("Running in GitHub Actions - adding CI/CD specific options")
                options.add_argument('--no-sandbox')
                options.add_argument('--headless=new')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
            
            # Download and setup ChromeDriver
            chromedriver_path = DriverFactory.download_chromedriver()
            
            # Create service object with ChromeDriver path
            service = Service(executable_path=chromedriver_path)
            
            # Create and configure the Chrome WebDriver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            # Log successful driver creation
            logger.info(
                f"Created Chrome driver in "
                f"{'headless' if os.getenv('GITHUB_ACTIONS') else 'normal'} mode"
            )
            
            return driver
            
        except Exception as e:
            # Log any errors during driver creation
            logger.error(f"Failed to create driver: {str(e)}")
            raise