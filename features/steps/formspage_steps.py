# features/steps/formspage_steps.py
from behave import given, when, then
from pages.forms_page import FormsPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
'''''
@given('I am on the homepage')
def step_impl(context):
    """
    Navigate to the homepage.
    """
    homepage_url = "https://play1.automationcamp.ir/"
    context.driver.get(homepage_url)
    logger.info("Navigated to the homepage.")
    '''

from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

@when('I navigate to the forms page')
def step_impl(context):
    """
    Navigate to the Forms page by clicking the "View Page" button for the "Forms" card.
    """
    # XPath targeting the "View Page" button for the Forms card
    forms_page_button_locator = (
        By.XPATH,
        "/html/body/div[2]/div[2]/div[3]/div/div[2]/a"
    )

    home_page = FormsPage(context.driver)

    try:
        # Scroll to the element to ensure visibility
        forms_button = home_page.wait_for_element_visible(forms_page_button_locator)
        ActionChains(context.driver).move_to_element(forms_button).perform()

        # Wait until it's clickable and then click
        forms_button = home_page.wait_for_element_clickable(forms_page_button_locator)
        home_page.safe_click(forms_button)

        logger.info("Successfully navigated to the Forms page.")
    except Exception as e:
        logger.error(f"Failed to navigate to the Forms page: {e}")
        raise


@then('I should see the forms page successfully loaded')
def step_impl(context):
    """
    Verify that the Forms page has successfully loaded.
    """
    forms_page = FormsPage(context.driver)
    assert forms_page.verify_page_loaded(), "Forms page failed to load."

@given('I am on the forms page')
def step_impl(context):
    """
    Navigate directly to the Forms page.
    """
    forms_page = FormsPage(context.driver)
    forms_page.navigate_to_forms_page()
    assert forms_page.verify_page_loaded(), "Failed to load the Forms page"

@when('I fill out the basic form controls')
def step_impl(context):
    """
    Fill out the basic form controls with sample data and capture a screenshot after filling.
    """
    forms_page = FormsPage(context.driver)

    # Dynamically determine the project root
    project_root = os.getcwd()

    # Construct file paths relative to the project root
    cv_path = os.path.join(project_root, "CV_ZIP", "index.html")
    zip_path = os.path.join(project_root, "CV_ZIP", "github-pages.zip")
    
    # Fill out the form fields
    forms_page.fill_years_of_experience("5")
    forms_page.select_checkboxes(["Python", "JavaScript"])
    forms_page.select_radio_button("Selenium")
    forms_page.select_primary_skill("Selenium")
    forms_page.choose_languages(["JavaScript", "Python"])
    forms_page.fill_notes("This is a sample note for testing.")
    forms_page.upload_file(cv_path, is_cv=True) 
    forms_page.upload_file(zip_path, is_cv=False)  
    forms_page.toggle_german_switch(True)
    forms_page.set_german_fluency(3)
    
    # Take a screenshot after filling out the form
    logger.debug("Calling take_screenshot in the test step.")
    forms_page.take_screenshot("filled_form")
    logger.info("Screenshot of filled form captured.")

@when('I fill out the non-English text field')
def step_impl(context):
    """
    Fill out the non-English text field.
    """
    forms_page = FormsPage(context.driver)
    forms_page.fill_non_english_text_field("आपला नांव लिहा")
    logger.info("Filled the non-English text field.")

@when('I select the non-English checkboxes')
def step_impl(context):
    """
    Select all non-English checkboxes.
    """
    forms_page = FormsPage(context.driver)
    forms_page.select_non_english_checkboxes(["मराठी", "ગુજરાતી", "ਪੰਜਾਬੀ"])
    logger.info("Selected non-English checkboxes.")

@then('the non-English elements should reflect the changes')
def step_impl(context):
    """
    Verify the non-English elements reflect the changes made.
    """
    forms_page = FormsPage(context.driver)
    assert forms_page.verify_non_english_elements(), "Non-English elements did not reflect the changes."
    forms_page.take_screenshot("non_english_elements_verification")
    logger.info("Verified the non-English elements reflected the changes.")

@when('I click on the Download File link')
def step_impl(context):
    """
    Click the Download File link on the Forms page.
    """
    forms_page = FormsPage(context.driver)
    forms_page.click_download_file()
    logger.info("Clicked on the Download File link.")

@then('the file should be downloaded successfully')
def step_impl(context):
    """
    Verify the file was downloaded successfully in the dynamic downloads folder.
    """
    import os
    import time

    # Get the dynamic downloads folder
    project_root = os.getcwd()
    downloads_folder = os.path.join(project_root, "downloads")
    expected_file = "sample_text.txt"
    file_path = os.path.join(downloads_folder, expected_file)

    # Wait for the file to be downloaded
    timeout = 10
    for _ in range(timeout):
        if os.path.exists(file_path):
            logger.info(f"File downloaded successfully: {file_path}")
            break
        time.sleep(1)
    else:
        logger.error(f"File not found in downloads folder after {timeout} seconds.")
        raise AssertionError("Download failed or file not found.")
    
    # Clean up the downloaded file after verification (optional)
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Downloaded file removed after verification.")
    

@then('I submit the form')
def step_impl(context):
    """
    Submit the form and verify submission.
    """
    forms_page = FormsPage(context.driver)
    forms_page.submit_form()
    logger.info("Form submitted successfully.")
