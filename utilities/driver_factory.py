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
import json
import re

# Set up logging for this module
logger = logging.getLogger(__name__)

class DriverFactory:
    """
    Factory class for creating WebDriver instances
    Handles different environments (local and CI/CD) and configurations
    """
    
    @staticmethod
    def get_chrome_version():
        """
        Get the installed Chrome version
        
        Returns:
            str: Chrome version (major.minor.build.patch)
        """
        try:
            # Execute chrome --version command
            with os.popen('google-chrome --version') as stream:
                chrome_version = stream.read()
            
            # Extract version number using regex
            version_match = re.search(r'[\d.]+', chrome_version)
            if version_match:
                return version_match.group(0)
            return None
        except Exception as e:
            logger.error(f"Failed to get Chrome version: {str(e)}")
            return None
    
    @staticmethod
    def download_chromedriver():
        """
        Download and setup ChromeDriver matching the installed Chrome version
        
        Returns:
            str: Path to the ChromeDriver executable
        
        Raises:
            Exception: If download or setup fails
        """
        try:
            # Get Chrome version
            chrome_version = DriverFactory.get_chrome_version()
            if not chrome_version:
                raise Exception("Could not determine Chrome version")
            
            # Get major version
            major_version = chrome_version.split('.')[0]
            
            # Construct the version-specific download URL
            version_url = f"https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
            
            # Get versions JSON
            logger.info("Fetching ChromeDriver versions list")
            with urllib.request.urlopen(version_url) as response:
                versions_data = json.loads(response.read())
            
            # Find matching version
            matching_version = None
            for version in versions_data['versions']:
                if version['version'].startswith(major_version):
                    matching_version = version
                    break
            
            if not matching_version:
                raise Exception(f"No matching ChromeDriver version found for Chrome {chrome_version}")
            
            # Find Linux64 ChromeDriver download URL
            chromedriver_url = None
            for download in matching_version['downloads'].get('chromedriver', []):
                if download['platform'] == 'linux64':
                    chromedriver_url = download['url']
                    break
            
            if not chromedriver_url:
                raise Exception("Could not find Linux64 ChromeDriver download URL")
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            # Download ChromeDriver
            logger.info(f"Downloading ChromeDriver from {chromedriver_url}")
            urllib.request.urlretrieve(chromedriver_url, zip_path)
            
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the chromedriver binary
            chromedriver_path = os.path.join(temp_dir, "chromedriver-linux64", "chromedriver")
            
            # Make it executable
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