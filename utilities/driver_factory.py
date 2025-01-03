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
            from webdriver_manager.chrome import ChromeDriverManager
        
        # Use WebDriver Manager to dynamically install the correct ChromeDriver
            chromedriver_path = ChromeDriverManager().install()
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

            # Determine the dynamic downloads directory
            project_root = os.getcwd()
            download_directory = os.path.join(project_root, "downloads")
            os.makedirs(download_directory, exist_ok=True)  # Ensure the directory exists
            logger.info(f"Download directory being set to: {download_directory}")

            # Add download preferences
            prefs = {
                "download.default_directory": download_directory,  # Platform-independent path
                "download.prompt_for_download": False,  # Disable download prompts
                "safebrowsing.enabled": True,  # Enable Safe Browsing
                "profile.default_content_settings.popups": 0,  # Disable popups for file downloads
                "profile.default_content_setting_values.automatic_downloads": 1,  # Allow multiple downloads
            }

            options.add_experimental_option("prefs", prefs)

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
            logger.info(f"Download directory set to: {download_directory}")

            return driver

        except Exception as e:
            logger.error(f"Failed to create driver: {str(e)}")
            raise
    
    @staticmethod
    def is_running_in_ci():
        """Check if running in CI environment"""
        return bool(os.getenv('GITHUB_ACTIONS'))
