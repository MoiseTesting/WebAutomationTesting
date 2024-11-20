"""
Factory class for WebDriver creation and management.
Handles browser driver setup, configuration, and cleanup.
Supports both local and CI/CD environments.
"""
# Standard library imports
import logging
import os
import urllib.request
import zipfile
import tempfile
import shutil
import subprocess

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# WebDriver manager imports
from webdriver_manager.chrome import ChromeDriverManager

# Local imports
from utilities.config import Config

# Set up logging
logger = logging.getLogger(__name__)

class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def download_chromedriver_for_ci():
        """
        Download ChromeDriver specifically for CI environment
        
        Returns:
            str: Path to ChromeDriver executable
        """
        try:
            # Get Chrome version
            chrome_version = subprocess.check_output(['google-chrome', '--version'])
            chrome_version = chrome_version.decode('utf-8').strip().split()[-1].split('.')[0]
            logger.info(f"Detected Chrome version: {chrome_version}")
            
            # Create temp directory
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            # Construct download URL
            download_url = f"https://storage.googleapis.com/chrome-for-testing-public/stable/linux64/chromedriver-linux64.zip"
            logger.info(f"Downloading ChromeDriver from: {download_url}")
            
            # Download ChromeDriver
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extract the zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find chromedriver path
            chromedriver_path = os.path.join(temp_dir, 'chromedriver-linux64', 'chromedriver')
            
            # Make executable
            os.chmod(chromedriver_path, 0o755)
            logger.info(f"ChromeDriver installed at: {chromedriver_path}")
            
            return chromedriver_path
            
        except Exception as e:
            logger.error(f"Error downloading ChromeDriver: {str(e)}")
            raise
    
    @staticmethod
    def get_driver():
        """
        Create and return a WebDriver instance
        Handles both local and CI/CD environments
        
        Returns:
            WebDriver: Configured WebDriver instance
        """
        try:
            # Get browser options from config
            options = Config.get_browser_options()
            
            # Handle CI/CD environment
            if os.getenv('GITHUB_ACTIONS'):
                logger.info("Running in GitHub Actions - configuring for CI/CD")
                options.add_argument('--no-sandbox')
                options.add_argument('--headless=new')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                
                # Use custom ChromeDriver download for CI
                chromedriver_path = DriverFactory.download_chromedriver_for_ci()
                service = Service(executable_path=chromedriver_path)
            else:
                logger.info("Running in local environment")
                options.add_argument('--start-maximized')
                options.add_argument('--window-size=1920,1080')
                
                # Use webdriver-manager for local environment
                service = Service(ChromeDriverManager().install())
            
            # Create the driver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            # Handle window management for local runs
            if not os.getenv('GITHUB_ACTIONS') and not Config.HEADLESS:
                driver.maximize_window()
                window_size = driver.get_window_size()
                logger.info(f"Window size: {window_size['width']}x{window_size['height']}")
                
                if window_size['width'] < 1920:
                    driver.set_window_size(1920, 1080)
                    logger.info("Window size adjusted to 1920x1080")
            
            logger.info(
                f"Created Chrome driver in "
                f"{'headless' if Config.HEADLESS or os.getenv('GITHUB_ACTIONS') else 'normal'} mode"
            )
            
            return driver
            
        except Exception as e:
            logger.error(f"Failed to create driver: {str(e)}")
            raise
    
    @staticmethod
    def is_running_in_ci():
        """Check if running in CI environment"""
        return bool(os.getenv('GITHUB_ACTIONS'))
