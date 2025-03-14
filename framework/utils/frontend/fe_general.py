from pathlib import Path
import yaml
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from framework import ROOT_DIR


class FEGeneral:
    """
    FEGeneral class provides utility methods for interacting with a web browser using Selenium WebDriver.
    """
    config_sample_path = Path(f'{ROOT_DIR}/utils/config_sample.yaml')
    with config_sample_path.open() as file:
        config_data = yaml.safe_load(file)
    run_opts = config_data.get('config', {}).get('run_opts', {})
    url = run_opts['url']
    current_env = run_opts['current_env']
    current_driver = run_opts['current_driver']
    configured_wait = run_opts['configured_wait']
    implicit_wait = run_opts['implicit_wait']
    headless = run_opts['headless']
    driver = None

    def __init__(self):
        """
        __init__()

        :Description: Initialize the FEGeneral class with the specified temporary directory.
        """
        self.driver = None

    # Browser related functions
    def open_browser(self):
        """
        open_browser()

        :Description: Open a Chrome browser window in fullscreen mode and configure headless mode based on the headless
                      parameter.
        :return: None
        """
        options = Options()
        options.add_argument("--start-fullscreen")
        if self.headless:
            options.add_argument("--headless")
        else:
            options.add_argument("--disable-gpu")
        driver_path = "/opt/homebrew/bin/chromedriver"
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(self.implicit_wait)

    def close_browser(self):
        """
        close_browser()

        :Description: Close the browser window and take a screenshot before closing.
        :return: None
        """
        if self.driver:
            self.driver.quit()

    def is_page_loaded(self):
        """
        is_page_loaded()

        :Description: Check if the page is fully loaded.
        :return: True if the page is fully loaded, False otherwise.
        """
        if self.driver:
            return self.driver.execute_script("return document.readyState") == "complete"
        return False

    # Navigation to URL
    def go_to_page(self, driver=None):
        """
        open_browser_and_navigate()

        :Description: Open a Chrome browser window and navigate to the specified URL if provided.
        :return: None
        """
        if not self.driver:
            self.open_browser()
        self.driver.get(self.url)

    # Element interaction functions
    def find_element(self, locator, wait=True, multiple=False):
        """
        find_element()

        :Description: Find an element on the page using the provided locator.
        :param locator: The locator for the element.
        :param wait: Optional; whether to wait for the element to be present (default is True).
        :param multiple: Optional; whether to find multiple elements (default is False).
        :return: The found element(s).
        """
        try:
            if wait:
                self.wait_for_element(locator)
            if multiple:
                elements = self.driver.find_elements(By.XPATH, locator)
                return elements
            else:
                element = self.driver.find_element(By.XPATH, locator)
                return element
        except NoSuchElementException:
            print(f"Element not found: {str(locator)}")
            return None

    def wait_for_element(self, locator):
        """
        wait_for_element()

        :Description: Wait for the page to load and the element to be clickable.
        :param locator: The locator for the element.
        :return: None
        """
        WebDriverWait(self.driver, self.configured_wait).until(lambda driver: self.is_page_loaded())
        wait = WebDriverWait(self.driver, self.configured_wait)
        wait.until(EC.element_to_be_clickable((By.XPATH, locator)))

    def scroll_into_view(self, locator):
        """
        scroll_into_view()

        :Description: Scroll the web page until the specified element is in view.
        :param locator: The locator for the element to scroll into view.
        :return: None
        """
        try:
            element = self.find_element(locator)
            # By using below command, we can scroll the element into view with JavaScript
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            # By using below command, we can scroll the element into view with Actions Class
            # ActionChains(self.driver).move_to_element(element).perform()
        except TimeoutException:
            print(f"Timeout while waiting for element: {locator}")

    def click_element(self, locator):
        """
        click_element()

        :Description: Click on the specified element.
        :param locator: The locator for the element.
        :return: None
        """
        element = self.find_element(locator)
        self.action_chain_click(element)

    def action_chain_click(self, element):
        """
        action_chain_click()

        :Description: Click on the specified element using ActionChains.
        :param element: The element to click.
        :return: None
        """
        ActionChains(self.driver).move_to_element(element).click().perform()

    def verify_element_text(self, locator, text, wait=True):
        """
        verify_element_text()

        :Description: Verify if the specified text is present in the element located by the given locator.
        :param locator: The locator for the element.
        :param text: The text to verify within the element.
        :param wait: Optional; whether to wait for the element to be present (default is True).
        :return: True if the text is present in the element, False otherwise.
        """
        if wait:
            self.wait_for_element(locator)
        element = self.find_element(locator)
        if element:
            return text in element.text
        return False

    @staticmethod
    def format_locator(locator, value):
        """
        format_locator()

        :Description: Format a locator string with the provided values.
        :param locator: The locator string to format.
        :param value: Values to replace in the locator string.
        :return: The formatted locator string.
        """
        if value:
            return str(locator.format(value))
        else:
            raise ValueError("No value provided for formatting the locator string.")
