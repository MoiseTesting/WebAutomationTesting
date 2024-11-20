"""
Factory class for WebDriver creation and management.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib.request
import zipfile
import os
import logging
import tempfile
import shutil

logger = logging.getLogger(__name__)

class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def download_chromedriver():
        """Download the correct ChromeDriver version"""
        try:
            # Get Chrome version
            chrome_process = os.popen('google-chrome --version')
            chrome_version = chrome_process.read().strip('Google Chrome ').strip().split('.')[0]
            chrome_process.close()
            
            # Construct download URL
            download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}/linux64/chromedriver-linux64.zip"
            
            # Create temp directory
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "chromedriver.zip")
            
            # Download file
            logger.info(f"Downloading ChromeDriver from: {download_url}")
            urllib.request.urlretrieve(download_url, zip_path)
            
            # Extract file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find chromedriver path
            chromedriver_path = os.path.join(temp_dir, 'chromedriver-linux64', 'chromedriver')
            
            # Make executable
            os.chmod(chromedriver_path, 0o755)
            
            return chromedriver_path
            
        except Exception as e:
            logger.error(f"Failed to download ChromeDriver: {str(e)}")
            raise
    
    @staticmethod
    def get_driver():
        """Create and return a WebDriver instance"""
        try:
            # Get browser options from config
            options = Options()
            
            # Add CI/CD specific options when running in GitHub Actions
            if os.getenv('GITHUB_ACTIONS'):
                logger.info("Running in GitHub Actions - configuring for CI/CD")
                options.add_argument('--no-sandbox')
                options.add_argument('--headless=new')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
            
            if os.getenv('GITHUB_ACTIONS'):
                # Use custom ChromeDriver download in CI/CD
                chromedriver_path = DriverFactory.download_chromedriver()
                service = Service(executable_path=chromedriver_path)
            else:
                # Use webdriver-manager locally
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
            
            # Create and return the driver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            logger.info(f"Created Chrome driver in {'headless' if os.getenv('GITHUB_ACTIONS') else 'normal'} mode")
            return driver
            
        except Exception as e:
            logger.error(f"Failed to create driver: {str(e)}")
            raise
