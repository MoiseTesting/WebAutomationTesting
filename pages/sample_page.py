"""
Page Object for the Sample Pages section of the automation practice website.
This class contains all element locators and methods needed to interact with
the sample pages, including the login functionality.

The Page Object Model (POM) design pattern is used here to:
- Encapsulate page-specific locators and methods
- Provide reusable methods for test steps
- Handle page-specific error scenarios and logging
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import logging
import time


logger = logging.getLogger(__name__)

class SamplePage(BasePage):
    """
    Page object for the Sample Pages section
    Provides methods to interact with login form and related elements
    """
    
    # Dictionary of element locators used in the Sample Pages section
    # Each locator is a tuple of (locator_type, locator_value)
    LOCATORS = {
        'sample_page_link': (By.XPATH, "//h5[contains(text(), 'Sample Pages')]"),
        'view_page_button': (By.CSS_SELECTOR, "a[href='login.html'].btn-success"),
        'login_form': (By.XPATH, "//h2[contains(text(), 'Log in')]"),  
        'username_field': (By.ID, "user"),  
        'password_field': (By.ID, "password"),  
        'login_button': (By.ID, "login"),  
        'login_result': (By.ID, "pizza_order_form"),
        'success_message': (By.ID, "pizza_order_form"),
        'pizza_heading': (By.XPATH, "//h3[text()=\"Dinesh's Pizza House\"]"),
        'pizza_order_form': (By.ID, "pizza_order_form"),
        'pizza_description': (By.XPATH, "//div[contains(text(), 'Customize your pizza by choosing')]"),
        'pizza_order_form_alt': (By.XPATH, "//form[contains(@class, 'card shadow')]"),
        'login_button_alt1': (By.CSS_SELECTOR, "button.btn.btn-primary.btn-block"),
        #'login_button_alt2': (By.XPATH, "//button[@type='submit']"),
        #'login_button_alt3': (By.XPATH, "//button[contains(text(),'Log In')]"),  
        'error_message': (By.ID, "message"),
        'error_message_alt': (By.XPATH, "//div[@class='text-danger text-center']"),
        'register_link': (By.XPATH, "//a[contains(text(), 'Register')]"),
        'registration_heading': (By.XPATH, "//h2[text()='Register']"),
        'first_name': (By.NAME, "first_name"),
        'last_name': (By.NAME, "last_name"),
        'email': (By.NAME, "email"),
        'reg_password': (By.NAME, "password"),
        'confirm_password': (By.NAME, "confirm_password"),
        'terms_checkbox': (By.XPATH, "//input[@type='checkbox']"),
        'register_button': (By.XPATH, "//button[text()='Register Now']"),
        'size_medium': (By.ID, "rad_medium"),
        'size_medium_alt1': (By.XPATH, "//input[@id='rad_medium' and @value='MEDIUM']"),
        'size_medium_alt2': (By.CSS_SELECTOR, "input[name='size'][value='MEDIUM']"),
        'size_medium_alt3': (By.XPATH, "//div[contains(@class, 'form-check-inline')]//input[@value='MEDIUM']"),
        'flavor_dropdown': (By.ID, "select_flavor"),
        'quantity_input': (By.ID, "qauntity"),
        'add_to_cart_button': (By.ID, "submit_button"),
        'confirmation_message': (By.ID, "added_message"),
        'quantity_modal': (By.ID, "quantity_modal"),
        'quantity_validation_message': (By.XPATH, "//div[@class='modal-body'][contains(text(), 'Quantity must be 1 or more!')]"),
        'modal_close': (By.CSS_SELECTOR, ".btn-close, .close"),
        'modal_body': (By.CLASS_NAME, "modal-body"),
        'modal_close_button': (By.XPATH, "//button[@class='btn btn-warning' and @data-dismiss='modal']"),
        'warning_icon': (By.XPATH, "//i[@class='fa fa-lg fa-info-circle text-warning']"),
        # or if there's a specific close button
        'modal_close_button_alt': (By.XPATH, "//div[@id='quantity_modal']//button[contains(@class, 'close')]")
    }

    def verify_quantity_validation_message(self):
        """
        Verify that the quantity validation message is displayed
        
        Returns:
            bool: True if validation message is found and verified, False otherwise
        """
        try:
            # Check for warning icon
            warning_icon = self.wait_for_element_visible(self.LOCATORS['warning_icon'])
            logger.info("Warning icon found in modal")

            # Check for modal body and its text
            modal_body = self.wait_for_element_visible(self.LOCATORS['modal_body'])
            message_text = modal_body.text.strip()
            logger.info(f"Found modal text: '{message_text}'")
            
            if "Quantity must be 1 or more!" in message_text:
                logger.info("Validation message verified")
                
                # Find and click close button
                close_button = self.wait_for_element_clickable(self.LOCATORS['modal_close_button'])
                close_button.click()
                logger.info("Closed validation modal")
                
                # Add small delay for modal to close
                time.sleep(0.5)
                
                return True
            else:
                logger.error(f"Unexpected validation message: '{message_text}'")
                return False
                
        except Exception as e:
            logger.error(f"Failed to verify quantity validation message: {str(e)}")
            self.take_screenshot("validation_message_error")
            return False
    def verify_pizza_form_displayed(self):
        """
    Verify that the pizza order form is displayed and ready for interaction
    
    Returns:
        bool: True if form is found and visible, False otherwise
        """
        try:
            # Logging initial page state
            logger.info("=== Starting Pizza Form Verification ===")
            logger.info(f"Current URL: {self.driver.current_url}")
            logger.info(f"Page Title: {self.driver.title}")

             # Log any JavaScript errors or console messages
            #logs = self.driver.get_log('browser')
            #for log in logs:
                #logger.info(f"Browser Log: {log}")
             # Try to clear any existing form state
            self.driver.execute_script("localStorage.clear();")
            self.driver.execute_script("sessionStorage.clear();")
            
            # Take screenshot of initial state
            self.take_screenshot("before_form_verification")
            
            # Log page source preview
            logger.info("Page Source Preview (first 500 chars):")
            logger.info(f"{self.driver.page_source[:500]}...")
            
            # Add initial wait after page load
            time.sleep(2)
            
            # Check for main heading with timing
            logger.info("Attempting to find pizza heading...")
            start_time = time.time()
            heading = self.wait_for_element_visible(self.LOCATORS['pizza_heading'])
            if not heading:
                logger.error("Pizza heading not found")
                return False
            logger.info(f"Pizza heading found in {time.time() - start_time:.2f} seconds")
            logger.info(f"Heading text: {heading.text}")

            # Check for form with timing
            logger.info("Attempting to find pizza order form...")
            start_time = time.time()
            form = self.wait_for_element_visible(self.LOCATORS['pizza_order_form'])
            if not form:
                logger.error("Pizza order form not found")
                return False
            logger.info(f"Pizza order form found in {time.time() - start_time:.2f} seconds")
            
            # Take screenshot after verification
            self.take_screenshot("after_form_verification")
            
            # Log form attributes if found
            if form:
                logger.info("Form Details:")
                logger.info(f"Form ID: {form.get_attribute('id')}")
                logger.info(f"Form Classes: {form.get_attribute('class')}")
                logger.info(f"Form is Displayed: {form.is_displayed()}")
                logger.info(f"Form is Enabled: {form.is_enabled()}")

            logger.info("Successfully verified pizza order form is displayed")
            logger.info("=== Pizza Form Verification Complete ===")
            return True

        except Exception as e:
            logger.error("=== Pizza Form Verification Failed ===")
            logger.error(f"Error verifying pizza form: {str(e)}")
            self.take_screenshot("pizza_form_verification_failed")
            
            # Log additional error context
            logger.error(f"Current URL at time of error: {self.driver.current_url}")
            logger.error(f"Page Title at time of error: {self.driver.title}")
        
        # Try to get any error messages on the page
        try:
            error_elements = self.driver.find_elements(By.CLASS_NAME, "error")
            if error_elements:
                logger.error("Found error messages on page:")
                for error in error_elements:
                    logger.error(f"Error message: {error.text}")
        except:
            pass
            
        return False
    
 
        """
        Handle the quantity warning modal if it appears
        """
        try:
            # Wait for modal with warning message
            self.wait_for_element_visible(self.LOCATORS['quantity_warning_modal'])
            
            # Find and click the Close button
            close_button = self.wait_for_element_clickable(self.LOCATORS['modal_close_button'])
            close_button.click()
            
            # Wait for modal to disappear
            time.sleep(1)
            
            logger.info("Successfully handled quantity warning modal")
            return True
        except Exception as e:
            logger.error(f"Failed to handle quantity modal: {str(e)}")
            return False


    def select_pizza_size(self, size):
        """
        Select pizza size with improved error handling
        """
        try:
            logger.info(f"Attempting to select {size} size pizza")
            
           
            
            # Log all radio buttons present for debugging
            radios = self.driver.find_elements(By.CSS_SELECTOR, "input[name='size']")
            logger.info(f"Found {len(radios)} size radio buttons")
            for radio in radios:
                logger.info(f"Radio button - ID: {radio.get_attribute('id')}, "
                        f"Value: {radio.get_attribute('value')}, "
                        f"Checked: {radio.get_attribute('checked')}")
            
            # Try to find and click the medium radio
            radio = self.wait_for_element_present(self.LOCATORS['size_medium'])
            
            # Log element state before clicking
            logger.info(f"Found medium radio button. "
                    f"Displayed: {radio.is_displayed()}, "
                    f"Enabled: {radio.is_enabled()}, "
                    f"Selected: {radio.is_selected()}")
            
            # Scroll into view
            self.scroll_to_element(radio)
            
            # Try JavaScript click first (more reliable)
            self.driver.execute_script("arguments[0].click();", radio)
            
            # Verify selection
            if radio.is_selected():
                logger.info("Successfully selected medium size")
                return True
            else:
                logger.error("Radio button click didn't change selection state")
                return False
                
        except Exception as e:
            logger.error(f"Failed to select pizza size: {str(e)}")
            self.take_screenshot("pizza_size_selection_failed")
            return False
    def verify_order_confirmation(self):
        """
        Verify that the order confirmation message is displayed
        
        Returns:
            bool: True if confirmation message is found, False otherwise
        """
        try:
            # Wait for confirmation message
            confirmation = self.wait_for_element_visible(self.LOCATORS['confirmation_message'])
            message_text = confirmation.text
            
            # Verify exact message
            if message_text == "Pizza added to the cart!":
                logger.info("Order confirmation message verified successfully")
                return True
            else:
                logger.error(f"Unexpected confirmation message: {message_text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to verify order confirmation: {str(e)}")
            return False
    def select_sauce(self, sauce):
        """
        Select sauce type dynamically
        
        Args:
            sauce (str): Type of sauce to select
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            sauce_id = f"rad_{sauce.lower()}"
            sauce_radio = self.wait_for_element_clickable((By.ID, sauce_id))
            sauce_radio.click()
            logger.info(f"Selected sauce: {sauce}")
            return True
        except Exception as e:
            logger.error(f"Failed to select sauce {sauce}: {str(e)}")
            return False

    def select_toppings(self, toppings):
        """
        Select pizza toppings
        
        Args:
            toppings (list): List of toppings to select
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            for topping in toppings:
                topping_id = topping.lower()
                checkbox = self.wait_for_element_clickable((By.ID, topping_id))
                checkbox.click()
                logger.info(f"Selected topping: {topping}")
            return True
        except Exception as e:
            logger.error(f"Failed to select toppings: {str(e)}")
            return False
    def enter_quantity(self, quantity):
        """
        Enter pizza quantity
        """
        try:
            # Try multiple locator strategies if needed
            try:
                # Try ID first
                quantity_field = self.wait_for_element_visible((By.ID, "quantity"))
            except Exception:
                # Try backup locators if ID fails
                quantity_field = self.wait_for_element_visible(
                    (By.CSS_SELECTOR, "input[aria-describedby='How many pizza you want?']")
                )

            quantity_field.clear()
            quantity_field.send_keys(quantity)
            logger.info(f"Entered quantity: {quantity}")
            return True
        except Exception as e:
            logger.error(f"Failed to enter quantity: {str(e)}")
            return False
    def click_add_to_cart(self):
        """
        Click the Add to Cart button
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            add_cart_button = self.wait_for_element_clickable(self.LOCATORS['add_to_cart_button'])
            add_cart_button.click()
            logger.info("Clicked Add to Cart button")
            return True
        except Exception as e:
            logger.error(f"Failed to click Add to Cart button: {str(e)}")
            return False

    def select_option_by_text(self, select_element, text):
        """
        Select option from dropdown by visible text
        
        Args:
            select_element: The select element
            text (str): Text of option to select
        """
        try:
            from selenium.webdriver.support.ui import Select
            select = Select(select_element)
            select.select_by_visible_text(text)
            return True
        except Exception as e:
            logger.error(f"Failed to select option {text}: {str(e)}")
            return False
    def click_register_link(self):
        """Click the register link on login page"""
        try:
            link = self.wait_for_element_clickable(self.LOCATORS['register_link'])
            link.click()
            logger.info("Clicked register link successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to click register link: {str(e)}")
            return False

    def verify_registration_page(self):
        """Verify registration page is loaded"""
        try:
            self.wait_for_element_visible(self.LOCATORS['registration_heading'])
            logger.info("Registration page verified")
            return True
        except Exception as e:
            logger.error(f"Failed to verify registration page: {str(e)}")
            return False

    def fill_registration_form(self, first_name, last_name, email, password):
        """Fill out the registration form"""
        try:
            # Fill in each field
            self.wait_for_element_visible(self.LOCATORS['first_name']).send_keys(first_name)
            self.wait_for_element_visible(self.LOCATORS['last_name']).send_keys(last_name)
            self.wait_for_element_visible(self.LOCATORS['email']).send_keys(email)
            self.wait_for_element_visible(self.LOCATORS['reg_password']).send_keys(password)
            self.wait_for_element_visible(self.LOCATORS['confirm_password']).send_keys(password)
            
            # Accept terms
            terms_checkbox = self.wait_for_element_clickable(self.LOCATORS['terms_checkbox'])
            terms_checkbox.click()
            
            logger.info("Registration form filled successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to fill registration form: {str(e)}")
            return False

    def click_register_button(self):
        """Click the register now button"""
        try:
            button = self.wait_for_element_clickable(self.LOCATORS['register_button'])
            button.click()
            logger.info("Clicked register button successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to click register button: {str(e)}")
            return False
    def verify_error_message(self):
        """
        Verify the error message is displayed for invalid login
        
        Returns:
            bool: True if error message is found and contains expected text
        """
        try:
            error_element = self.wait_for_element_visible(self.LOCATORS['error_message'])
            error_text = error_element.text
            expected_text = "Incorrect username or password. Try again!"
            
            if expected_text in error_text:
                logger.info(f"Error message verified: {error_text}")
                return True
            else:
                logger.error(f"Unexpected error message: {error_text}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to find error message: {str(e)}")
            return False
    def click_login_button(self):
        """
        Attempt to click login button using multiple strategies
        """
        try:
            # First verify we're still on the login page
            if 'login.html' not in self.driver.current_url:
                logger.info("Already logged in, skipping login button click")
                return True

            # Try primary login button first
            try:
                button = self.wait_for_element_clickable((By.ID, "login"))
                if button:
                    self.scroll_to_element(button)
                    button.click()
                    logger.info("Successfully clicked login button using ID")
                    return True
            except Exception:
                logger.debug("Could not click button using ID")

            # If we're still on login page, try alternatives
            if 'login.html' in self.driver.current_url:
                for locator_name in ['login_button_alt1']:  # Removed alt2 and alt3
                    try:
                        button = self.wait_for_element_clickable(self.LOCATORS[locator_name])
                        if button and button.is_displayed():
                            self.scroll_to_element(button)
                            button.click()
                            logger.info(f"Successfully clicked login button using {locator_name}")
                            return True
                    except Exception:
                        continue

                # Last resort - JavaScript click
                try:
                    button = self.driver.find_element(By.ID, "login")
                    self.driver.execute_script("arguments[0].click();", button)
                    logger.info("Successfully clicked login button using JavaScript")
                    return True
                except Exception:
                    logger.error("Failed to click button using JavaScript")
                    raise

            return False

        except Exception as e:
            logger.error(f"Failed to click login button: {str(e)}")
            return False

    def verify_login_result(self):
        """
        Verifies successful login by checking for pizza order page elements
        
        Returns:
            bool: True if login was successful and pizza page loaded
        """
        try:
            # Wait for main heading
            self.wait_for_element_visible(self.LOCATORS['pizza_heading'])
            
            # Wait for order form
            self.wait_for_element_visible(self.LOCATORS['pizza_order_form'])
            
            logger.info("Successfully verified pizza order page loaded")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying login result: {str(e)}")
            return False
    def click_sample_page_link(self):
        """
        Clicks the Sample Pages link to navigate to the sample pages section.
        Includes scrolling to ensure element is visible before clicking.
        
        Returns:
            bool: True if click was successful, False otherwise
        """
        try:
            # Wait for and find the Sample Pages link
            link = self.wait_for_element_visible(self.LOCATORS['sample_page_link'])
            # Wait for and find the View Page button
            button = self.wait_for_element_visible(self.LOCATORS['view_page_button'])
            
            # Scroll the button into view before clicking
            self.scroll_to_element(button)
            
            # Click the button to navigate
            button.click()
            logger.info("Clicked Sample Pages link")
            return True
        except Exception as e:
            logger.error(f"Failed to click Sample Pages link: {str(e)}")
            return False

    def login(self, username, password):
        """
        Performs login operation with provided credentials
        """
        try:
            # Find and fill username field
            username_field = self.wait_for_element_visible(self.LOCATORS['username_field'])
            username_field.clear()
            username_field.send_keys(username)
            
            # Find and fill password field
            password_field = self.wait_for_element_visible(self.LOCATORS['password_field'])
            password_field.clear()
            password_field.send_keys(password)
            
            # Get current URL before login
            current_url = self.driver.current_url
            
            # Find and click login button
            button = self.wait_for_element_clickable(self.LOCATORS['login_button'])
            self.scroll_to_element(button)
            button.click()
            
            logger.info(f"Performed login with username: {username}")
            return True
                
        except Exception as e:
            logger.error(f"Failed to perform login: {str(e)}")
            return False
    
