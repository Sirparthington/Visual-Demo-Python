from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib3
from os import environ
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from saucelabs_visual.client import SauceLabsVisual
from saucelabs_visual.typing import FullPageConfig, IgnoreElementRegion

# Set the project name
environ['SAUCE_VISUAL_PROJECT'] = 'Janssen Demo'

# Instantiate the visual client
client = SauceLabsVisual()

urllib3.disable_warnings()

# Set up Chrome options
options = ChromeOptions()

# Define Sauce Labs capabilities
sauce_options = {
    'username': environ['SAUCE_USERNAME'],
    'accessKey': environ['SAUCE_ACCESS_KEY'],
    'build': 'Janssen Demo Fullpage',
    'name': 'Janssen Demo Fullpage',
    'browserVersion': 'latest',
    'platformName': 'Windows 11',
}

# Set the Sauce Labs capabilities in Chrome options
options.set_capability('sauce:options', sauce_options)

# Define the Sauce Labs URL
url = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"

# Initialize the WebDriver with the Sauce Labs remote URL
driver = webdriver.Remote(command_executor=url, options=options)

def test_website():
    try:
        # Create the visual build
        client.create_build(name='Janssen FullPage')

        # Point to the customer website
        driver.get("https://www.janssenwithme.com")

        # Get your Selenium session ID
        session_id = driver.session_id

        # Wait for the accept button to be clickable and click it
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_button.click()
        except NoSuchElementException:
            print("Accept button not found")
            # Removed the screenshot for faster execution

        # Create snapshot on the first page
        client.create_snapshot_from_webdriver(
            name="First Page",
            session_id=session_id,
            capture_dom=True,  # Keep this for DOM comparisons, or else comment out
            full_page_config=FullPageConfig()  # Keep this for running full page screenshots, or else comment out
        )

        # Find another element by its ID and click it
        try:
            aboutus_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'SubMenu.Item.2.About-us'))  # Replace with the actual ID
            )
            aboutus_element.click()
        except NoSuchElementException:
            print("About us element not found")
            # Removed the screenshot for faster execution

        # Example: Wait for a specific text element to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'SubMenu.Item.0.Diseases'))  # Replace with actual ID
        )

        # Create snapshot on the second page
        client.create_snapshot_from_webdriver(
            name="Second Page",
            session_id=session_id,
            capture_dom=True,
            full_page_config=FullPageConfig(),  # Keep this for running full page screenshots, or else comment out
            ignore_elements=[  # Keep this to ignore an element, or else comment out
                IgnoreElementRegion(
                    element=driver.find_element(By.ID, 'SubMenu.Item.2.About-us')  # Replace with actual ID
                )
            ]
        )

        # Mark the job as passed (conditionally for demonstration)
        driver.execute_script('sauce:job-result=passed')

    except Exception as e:
        print(f"An error occurred: {e}")
        # Mark the job as failed
        driver.execute_script('sauce:job-result=failed')

    finally:
        # Finish the visual build and quit the driver
        client.finish_build()
        driver.quit()

test_website()
