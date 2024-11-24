from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class FormsPage(BasePage):
    """
    Page object for interacting with the Forms page.
    """

    # Define locators for all form elements
    LOCATORS = {
        'years_of_experience': (By.ID, 'exp'),
        'checkbox_python': (By.ID, 'check_python'),
        'checkbox_javascript': (By.ID, 'check_javascript'),
        'radio_selenium': (By.ID, 'rad_selenium'),
        'radio_protractor': (By.ID, 'rad_protractor'),
        'primary_skill_dropdown': (By.ID, 'select_tool'),
        'choose_language_multiselect': (By.ID, 'select_lang'),
        'notes_textarea': (By.ID, 'notes'),
        'upload_cv': (By.ID, 'upload_cv'),
        'upload_certificates': (By.ID, 'upload_files'),
        'german_switch': (By.XPATH, '/html/body/div/div[1]/div[2]/form/div[3]/div[2]/div/label'),
        'german_fluency_slider': (By.ID, 'fluency'),
        'submit_button': (By.XPATH, "//button[@type='submit']")
    }

    def navigate_to_forms_page(self):
        """
        Navigate to the Forms page by directly opening the URL.
        """
        try:
            self.driver.get("https://play1.automationcamp.ir/forms.html")
            logger.info("Navigated directly to the Forms page.")
        except Exception as e:
            logger.error(f"Failed to navigate to the Forms page: {e}")
            self.take_screenshot("navigation_error")
            raise

    def verify_page_loaded(self):
        """
        Verify the Forms page is loaded by checking for the presence of the page heading.
        """
        try:
            heading_locator = (By.XPATH, "//h3[text()='Basic Form Controls']")
            element = self.wait_for_element_visible(heading_locator)
            logger.info("Forms page loaded successfully.")
            return element is not None
        except Exception as e:
            self.take_screenshot("forms_page_not_loaded")
            logger.error(f"Failed to load Forms page: {e}")
            return False
    def click_download_file(self):
        """
        Click the Download File link.
        """
        download_link_locator = (By.ID, "download_file")
        try:
            download_link = self.wait_for_element_clickable(download_link_locator)
            self.safe_click(download_link)
            logger.info("Clicked on the Download File link.")
        except Exception as e:
            logger.error(f"Failed to click the Download File link: {e}")
            self.take_screenshot("download_file_click_error")
            raise
    def fill_years_of_experience(self, years):
        """
        Fill out the 'Years of Automation Experience' field.
        """
        input_field = self.wait_for_element_visible(self.LOCATORS['years_of_experience'])
        input_field.clear()
        input_field.send_keys(years)
        logger.info(f"Entered years of experience: {years}")

    def select_checkboxes(self, checkboxes):
        """
        Select one or more checkboxes.
        """
        for checkbox in checkboxes:
            locator = self.LOCATORS.get(f'checkbox_{checkbox.lower()}')
            if locator:
                checkbox_element = self.wait_for_element_clickable(locator)
                if not checkbox_element.is_selected():
                    checkbox_element.click()
                    logger.info(f"Selected checkbox: {checkbox}")
                else:
                    logger.info(f"Checkbox already selected: {checkbox}")

    def select_radio_button(self, button):
        """
        Select a radio button (e.g., Selenium, Protractor).
        """
        locator = self.LOCATORS.get(f'radio_{button.lower()}')
        if locator:
            radio_button = self.wait_for_element_clickable(locator)
            if not radio_button.is_selected():
                radio_button.click()
                logger.info(f"Selected radio button: {button}")

    def select_primary_skill(self, skill):
        """
        Select a primary skill from the dropdown.
        """
        dropdown = Select(self.wait_for_element_visible(self.LOCATORS['primary_skill_dropdown']))
        dropdown.select_by_visible_text(skill)
        logger.info(f"Selected primary skill: {skill}")

    def choose_languages(self, languages):
        """
        Select multiple languages from the multi-select dropdown.
        """
        multiselect = self.wait_for_element_visible(self.LOCATORS['choose_language_multiselect'])
        for language in languages:
            option = multiselect.find_element(By.XPATH, f"//option[@value='{language.lower()}']")
            option.click()
            logger.info(f"Selected language: {language}")

    def fill_notes(self, notes):
        """
        Fill out the 'Notes' textarea.
        """
        textarea = self.wait_for_element_visible(self.LOCATORS['notes_textarea'])
        textarea.clear()
        textarea.send_keys(notes)
        logger.info("Filled in the notes section.")

    def upload_file(self, file_path, is_cv=True):
        """
        Upload a file (CV or Certificates).
        """
        upload_field = self.LOCATORS['upload_cv'] if is_cv else self.LOCATORS['upload_certificates']
        element = self.wait_for_element_visible(upload_field)
        element.send_keys(file_path)
        logger.info(f"Uploaded file: {file_path}")

    def toggle_german_switch(self, state):
        """
        Toggle the 'Speaks German?' switch.
        """
        switch = self.wait_for_element_clickable(self.LOCATORS['german_switch'])
        current_state = switch.is_selected()
        if state and not current_state:
            switch.click()
        elif not state and current_state:
            switch.click()
        logger.info(f"Set 'Speaks German?' switch to: {state}")

    def set_german_fluency(self, level):
        """
        Set the German fluency slider to a specific level.
        """
        slider = self.wait_for_element_visible(self.LOCATORS['german_fluency_slider'])
        self.driver.execute_script("arguments[0].value = arguments[1]", slider, level)
        logger.info(f"Set German fluency level to: {level}")

    def fill_non_english_text_field(self, text):
        """
        Fill out the non-English text field.
        """
        text_field_locator = (By.ID, "नाव")  # The ID of the non-English text field
        text_field = self.wait_for_element_visible(text_field_locator)
        text_field.clear()
        text_field.send_keys(text)
        logger.info(f"Filled non-English text field with: {text}")

    def select_non_english_checkboxes(self, languages):
        """
        Select non-English checkboxes based on the provided language list.
        """
        for language in languages:
            checkbox_locator = (By.ID, language)  # The ID of the checkbox matches the language
            checkbox = self.wait_for_element_clickable(checkbox_locator)
            if not checkbox.is_selected():
                self.safe_click(checkbox)
                logger.info(f"Selected checkbox: {language}")

    def verify_non_english_elements(self):
        """
        Verify that the non-English elements reflect the changes made.
        """
        # Verify the text field
        text_field_locator = (By.ID, "नाव")
        text_field = self.wait_for_element_visible(text_field_locator)
        entered_text = text_field.get_attribute("value")
        if entered_text != "आपला नांव लिहा":
            logger.error(f"Non-English text field value mismatch: {entered_text}")
            return False

        # Verify the checkboxes
        checkboxes = ["मराठी", "ગુજરાતી", "ਪੰਜਾਬੀ"]
        for checkbox_id in checkboxes:
            checkbox_locator = (By.ID, checkbox_id)
            checkbox = self.wait_for_element_visible(checkbox_locator)
            if not checkbox.is_selected():
                logger.error(f"Checkbox {checkbox_id} is not selected.")
                return False

        logger.info("Non-English elements reflected the changes correctly.")
        return True

    def submit_form(self):
        """
        Click the Submit button.
        """
        submit_button = self.wait_for_element_clickable(self.LOCATORS['submit_button'])
        self.safe_click(submit_button)
        logger.info("Submitted the form.")
