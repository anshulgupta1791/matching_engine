from pathlib import Path
import yaml
from selenium.common import NoSuchElementException
from framework import ROOT_DIR
from framework.utils.frontend.fe_general import FEGeneral as fe_general
from framework.utils.frontend.matching_engine_home.matching_engine_home_config import (
    MatchingEngineHomeConfig as me_config)


class MatchingEngineHome:
    config = me_config
    config_sample_path = Path(f'{ROOT_DIR}/utils/config_sample.yaml')
    with config_sample_path.open() as file:
        config_data = yaml.safe_load(file)
    url = config_data.get('url')

    def __init__(self, driver):
        """
        __init__()

        :Description: Initialize the MatchingEngineHome class.
        :param driver: The WebDriver instance to use for browser interactions.
        """
        self.driver = driver
        self.fe_general = fe_general()

    def navigate_to_matching_engine_home(self):
        """
        navigate_to_matching_engine_home()

        :Description: Navigate to the Matching Engine Home page.
        :return: None
        """
        self.fe_general.go_to_page()

    def click_header_option(self, header_option):
        """
        click_header_option()

        :Description: Click on the specified header option.
        :param header_option: The header option to click on.
        :return: None
        """
        locator = self.config.me_header_options
        formatted_locator = self.fe_general.format_locator(locator, value=header_option)
        self.fe_general.click_element(formatted_locator)

    def click_products_supported(self, add_feature_option, element_text):
        """
        click_additional_features_option()

        :Description: Click on the specified additional features option.
        :param add_feature_option: The additional features option to click on.
        :param element_text: The expected text to verify after clicking.
        :return: None
        """
        self.fe_general.scroll_into_view(self.config.additional_features_title)
        formatted_locator = self.fe_general.format_locator(
            self.config.additional_features_options, value=add_feature_option)
        self.fe_general.click_element(formatted_locator)
        self.fe_general.verify_element_text(self.config.products_supported_heading, element_text)

    def assert_products_supported(self, locator, expected_products):
        """
        assert_products_supported()

        :Description: Asserts that the product list passed from the test is present under the "Products Supported"
                      section.
        :param locator: The locator for the product elements.
        :param expected_products: The list of expected products to verify.
        :return: None
        """
        try:
            product_elements = self.fe_general.find_element(locator, multiple=True)
            if product_elements:
                actual_products = [element.text.strip() for element in product_elements]
                missing_products = [product for product in expected_products if product not in actual_products]
                extra_products = [product for product in actual_products if product not in expected_products]
                if missing_products or extra_products:
                    error_message = "Product list assertion failed:\n"
                    if missing_products:
                        error_message += f"Missing products: {missing_products}\n"
                    if extra_products:
                        error_message += f"Extra products: {extra_products}\n"
                    raise AssertionError(error_message)
                else:
                    assert True
            else:
                raise NoSuchElementException(f"No product elements found with locator: {locator}")
        except (NoSuchElementException, AssertionError, Exception) as e:
            print(f"Error: {e}")
            raise
