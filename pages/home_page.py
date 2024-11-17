# pages/home_page.py
"""
Page object for the homepage containing element locators and
methods specific to homepage functionality.
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import logging
logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """
    Page object for the Practice Automation homepage.
    Contains all elements and methods specific to the homepage.
    """
    
    # Define multiple locators for redundancy
    LOCATORS = {
        #'title': (By.CSS_SELECTOR, "h1.page-title, h1.site-title"),
        'main_heading': (By.TAG_NAME, "h1"),
        'content_area': (By.ID, "main"),
        'site_content': (By.CLASS_NAME, "site-content")
    }
    
    def verify_page_loaded(self):
        """
        Verify that the homepage has loaded successfully.
        Tries multiple locators for better reliability.
        
        Returns:
            bool: True if the page is loaded successfully
        """
        try:
            # Try each locator until one works
            for name, locator in self.LOCATORS.items():
                try:
                    element = self.wait_for_element_visible(locator)
                    if element.is_displayed():
                        logger.info(f"Homepage verified using {name} locator")
                        return True
                except TimeoutException:
                    logger.debug(f"Could not find element using {name} locator")
                    continue
            
            # If we get here, none of the locators worked
            logger.error("Could not verify homepage using any locators")
            return False
            
        except Exception as e:
            logger.error(f"Error verifying homepage: {str(e)}")
            return False

    def get_page_title(self):
        """
        Get the visible page title text
        
        Returns:
            str: The text content of the page title
        """
        try:
            for name, locator in self.LOCATORS.items():
                try:
                    element = self.wait_for_element_visible(locator)
                    if element.is_displayed():
                        title_text = element.text
                        logger.info(f"Found page title: {title_text}")
                        return title_text
                except TimeoutException:
                    continue
            
            logger.error("Could not find page title")
            return None
            
        except Exception as e:
            logger.error(f"Error getting page title: {str(e)}")
            return None