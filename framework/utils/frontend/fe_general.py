"""
This file defines the `FEGeneral` class, which provides utility methods for interacting with a web browser using
Selenium WebDriver. It includes methods to open and close the browser, find and wait for elements, scroll elements into
view, take screenshots and attach them to Allure reports, and format locators. Configuration data is read from a YAML
file.
"""

import time
import allure
import yaml
from pathlib import Path
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from framework import ROOT_DIR
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class FEGeneral(webdriver):
    """
    FEGeneral class provides utility methods for interacting with a web browser using Selenium WebDriver.
    """
    config_sample_path = Path(f'{ROOT_DIR}/utils/config_sample.yaml')
    with config_sample_path.open() as file:
        config_data = yaml.safe_load(file)
    url = config_data.get('url')
    current_env = config_data.get('current_env')
    current_driver = config_data.get('current_driver')
    configured_wait = config_data.get('configured_wait')
    implicit_wait = config_data.get('implicit_wait')
    flaky_rerun = config_data.get('flaky_rerun')
    headless = config_data.get('headless')
    temp_dir = None
    driver = None

    def open_browser(self, temp_dir=None, test_name=None):
        """
        open_browser()

        :Description: Open a Chrome browser window in fullscreen mode and configure headless mode based on the headless
                      parameter.
        :param temp_dir: Optional; Temporary directory for browser data (default is None).
        :param test_name: Optional; Name of the test being run (default is None).
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
        wait_time = self.configured_wait
        self.driver.implicitly_wait(wait_time)

    def close_browser(self):
        """
        close_browser()

        :Description:Close the browser window.
        :return: None
        """
        if self.driver:
            self.driver.quit()

    def go_to_page(self, temp_dir=None, test_name=None):
        """
        open_browser_and_navigate()

        :Description: Open a Chrome browser window and navigate to the specified URL if provided.
        :param temp_dir: Optional; Temporary directory for browser data (default is None).
        :param test_name: Optional; Name of the test being run (default is None).
        :return: None
        """
        self.open_browser(temp_dir=temp_dir, test_name=test_name)
        self.driver.get(self.url)

    def find_element(self, locator, wait=True, **kwargs):
        """
        find_element()

        :Description: Find an element on the page using the provided locator.
        :param locator: The locator for the element.
        :param wait: Optional; whether to wait for the element to be present (default is True).
        :param kwargs: Additional keyword arguments.
            - multiple (bool): Whether to find multiple elements (default is False).
            - present (bool): Whether to wait for the element to be present (default is True).
            - timeout (int): The maximum time to wait for the element (default is False).
        :return: The found element.
        """
        try:
            multiple = kwargs.get('multiple', False)
            present = kwargs.get('present', True)
            timeout = kwargs.get('timeout', False)
            if present and wait:
                self.wait_for_element(locator, timeout=timeout)
            if multiple:
                element = self.driver.find_elements(*locator)
            else:
                element = self.driver.find_element(*locator)
            return element
        except NoSuchElementException:
            print(f"Element not found: " + str(locator[1]))
            return None

    def wait_for_element(self, locator, timeout):
        """
        wait_for_element()

        :Description: Wait for an element to be present on the page.
        :param locator: The locator for the element.
        :param timeout: Optional; the maximum time to wait for the element (default is None).
        :return: True if the element is found, False otherwise.
        """
        timeout = timeout if timeout else self.implicit_wait
        time.sleep(self.configured_wait)
        wait = WebDriverWait(self.driver, timeout)
        try:
            wait.until(EC.presence_of_element_located(locator))
            return True
        except Exception as e:
            print(f"Element not found: " + str(locator[1]))
            raise e

    def scroll_into_view(self, locator):
        """
        scroll_into_view()

        :Description: Scroll the page to bring the specified element into view.
        :param locator: The locator for the element.
        :return: None
        """
        if isinstance(locator, tuple):
            element = self.find_element(locator)
        else:
            element = locator
        self.driver.execute_script(
            "return arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)

    def click_element(self, locator, **kwargs):
        """
        click_element()

        :Description: Click on the specified element.
        :param locator: The locator for the element.
        :param kwargs: Additional keyword arguments.
            - multiple (bool): Whether to find multiple elements (default is False).
            - double_click (bool): Whether to double-click the element (default is False).
            - scroll_into_view (bool): Whether to scroll the element into view before clicking (default is False).
            - format_locator (bool): Whether to format the locator with provided values (default is False).
            - value: Values to replace in the locator string (used if format_locator is True).
            - keyword_value: Keyword arguments to replace in the locator string (used if format_locator is True).
            - element_number (int): Index of the element to click if multiple elements are found (default is 0).
        :return: None
        """
        multiple = kwargs.get('multiple', False)
        double_click = kwargs.get('double_click', False)
        scroll_into_view = kwargs.get('scroll_into_view', False)
        format_locator = kwargs.get('format_locator', False)
        if format_locator:
            locator = self.format_locator(locator, kwargs.get('value'), **kwargs.get('keyword_value'))
        if multiple:
            element = self.find_element(locator, multiple=True)
            element_number = kwargs.get('element_number', 0)
            element = element[element_number] if element else None
        else:
            element = self.find_element(locator)
        if double_click:
            self.action_chain_double_click(element)
        else:
            self.action_chain_click(element)
        if scroll_into_view:
            self.scroll_into_view(element)

    def action_chain_click(self, element):
        """
        action_chain_click()

        :Description: Click on the specified element using ActionChains.
        :param element: The element to click.
        :return: None
        """
        ActionChains(self.driver).move_to_element(element).click().perform()

    def action_chain_double_click(self, element):
        """
        action_chain_double_click()

        :Description: Double-click on the specified element.
        :param element: The element to double-click.
        :return: None
        """
        ActionChains(self.driver).move_to_element(element).double_click().perform()

    def verify_element_present(self, locator, wait=True, **kwargs):
        """
        verify_element_present()

        :Description: Verify if an element is present on the page or verify the page title if specified.
        :param locator: The locator for the element.
        :param wait: Optional; whether to wait for the element to be present (default is True).
        :param kwargs: Additional keyword arguments.
            - multiple (bool): Whether to expect multiple elements (default is False).
            - present (bool): Whether to wait for the element to be present (default is True).
            - timeout (int): The maximum time to wait for the element (default is self.implicit_wait).
            - page_title (bool): Whether to verify the page title instead of the element (default is False).
            - page_url (bool): Whether to verify the page URL instead of the element (default is False).
        :return: True if the element is present or the page title is correct, False otherwise.
        """
        if kwargs.get('page_title', False):
            return self.driver.title == locator
        if kwargs.get('page_url', False):
            return self.driver.current_url == locator
        result = False
        multiple = kwargs.get('multiple', False)
        present = kwargs.get('present', True)
        timeout = kwargs.get('timeout', self.implicit_wait)
        if present and wait:
            self.wait_for_element(locator, timeout=timeout)
        else:
            self.driver.implicitly_wait(0)
        elements = self.find_element(*locator)
        element_type = type(elements)
        if element_type != 'NoneType':
            if not elements:
                if present:
                    result = False
                else:
                    result = True
            else:
                if present:
                    try:
                        len(elements) == 1
                    except TypeError:
                        result = True
                    else:
                        print(f'Multiple elements found: {locator}'
                              f'Multiple elements expected?: {multiple}')
                        result = multiple
                else:
                    result = False
        return result

    def allure_screenshot(self, name=None):
        """
        allure_screenshot()

        :Description: Take a screenshot of the current browser window and save it with the specified name.
        :param name: Optional; the name for the screenshot (default is None).
        :return: None
        """
        if not name:
            name = "screenshot"
        screenshot_path = f"{name}.png"
        self.driver.save_screenshot(screenshot_path)
        with open(screenshot_path, "rb") as image_file:
            allure.attach(image_file.read(), name=name, attachment_type=allure.attachment_type.PNG)

    @staticmethod
    def format_locator(locator, *value, **keyword_value):
        """
        format_locator()

        :Description: Format a locator string with the provided values.
        :param locator: The locator string to format.
        :param value: Values to replace in the locator string.
        :param keyword_value: Keyword arguments to replace in the locator string.
        :return: The formatted locator string.
        """
        if value:
            return locator[0], locator[1].format(*value)
        return locator[0], locator[1].format(**keyword_value)

