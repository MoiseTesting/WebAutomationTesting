"""
Factory class for WebDriver creation and management.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utilities.config import Config
import urllib.request
import zipfile
import os
import logging
import tempfile


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
        """
        Create and return a WebDriver instance
        Handles both local and CI/CD environments
        
        Returns:
            WebDriver: Configured WebDriver instance
        """
        try:
            # Get browser options from config
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
                # For local runs, add window management
                options.add_argument('--start-maximized')
                options.add_argument('--window-size=1920,1080')
            
            # Setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # Create the driver
            driver = webdriver.Chrome(
                service=service,
                options=options
            )
            
            # Additional window management for local runs
            if not os.getenv('GITHUB_ACTIONS') and not Config.HEADLESS:
                # Try to maximize window
                driver.maximize_window()
                
                # Get and log window size
                window_size = driver.get_window_size()
                logger.info(f"Window size: {window_size['width']}x{window_size['height']}")
                
                # If window is still not full size, set it explicitly
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

    # Future enhancements could include:
    # - Support for other browsers (Firefox, Edge, etc.)
    # - Custom driver configurations
    # - Remote WebDriver support
    # - Container-based browser support
    # - Proxy configuration support
    # - Custom capabilities configuration