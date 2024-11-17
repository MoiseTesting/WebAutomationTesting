# pages/base_page.py
"""
Base page object class containing common methods and utilities
used across all page objects. Implements common web interactions.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utilities.config import Config
import logging
import time
logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all page objects.
    Contains common methods and wait strategies.
    """
    def wait_for_element_clickable(self, locator, timeout=None):
        """
        Wait for element to be clickable
        
        Args:
            locator: tuple of (By.XXX, "locator string")
            timeout: optional timeout in seconds
        """
        try:
            timeout = timeout or self.default_timeout
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except Exception as e:
            logger.error(f"Element not clickable: {locator}")
            self.take_screenshot(f"element_not_clickable_{locator[1]}")
            raise

    def safe_click(self, element):
        """
        Attempt to click an element safely using different methods
        
        Args:
            element: WebElement to click
        """
        try:
            # Try regular click
            element.click()
        except Exception:
            try:
                # Try JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
            except Exception as e:
                logger.error(f"Failed to click element: {str(e)}")
                raise
    def __init__(self, driver):
        self.driver = driver
        self.default_timeout = Config.DEFAULT_TIMEOUT
    
    def scroll_to_element(self, element):
        """
        Scrolls the element into view using JavaScript
        
        Args:
            element: WebElement to scroll to
        """
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # Add a small delay to allow smooth scrolling
            time.sleep(0.5)  # Small delay for the scroll to complete
            logger.debug("Scrolled to element successfully")
        except Exception as e:
            logger.error(f"Failed to scroll to element: {str(e)}")
    

    def wait_for_element_visible(self, locator, timeout=None):
        """
        Wait for element to be visible on page
        
        Args:
            locator: tuple of (By.XXX, "locator string")
            timeout: optional timeout in seconds
            
        Returns:
            WebElement: The visible element
            
        Raises:
            TimeoutException: If element is not visible within timeout
        """
        try:
            timeout = timeout or self.default_timeout
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible: {locator}")
            # Take screenshot for debugging
            self.take_screenshot(f"element_not_found_{locator[1]}")
            raise
    
    def take_screenshot(self, name):
        """
        Take a screenshot for debugging purposes
        
        Args:
            name: Name for the screenshot file
        """
        try:
            screenshot_path = f"screenshots/{name}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")

    def wait_for_element_present(self, locator, timeout=None):
        """
        Wait for element to be present in the DOM.
        
        Args:
            locator: Tuple of (By.XXX, 'locator string')
            timeout: Optional timeout override in seconds
        
        Returns:
            WebElement: The found element
        """
        try:
            timeout = timeout or self.default_timeout
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not present after {timeout} seconds"
            )