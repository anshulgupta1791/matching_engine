import pytest
from framework.utils.frontend.fe_general import FEGeneral
from framework.utils.frontend.matching_engine_home.matching_engine_home import MatchingEngineHome


@pytest.fixture(scope="session", autouse=True)
def basic_setup():
    """
    basic_setup()

    :Description: Setup method to initialize FEGeneral and open the browser.
    :return: An instance of the FEGeneral class.
    """
    fe_general = FEGeneral()
    fe_general.open_browser()
    yield fe_general
    fe_general.close_browser()

@pytest.fixture(scope="session")
def products_supported(basic_setup, request):
    """
    products_supported()

    :Description: Fixture to perform setup for products supported under additional features on repertoire management
                  page.
    :param basic_setup: The basic setup fixture that initializes the browser.
    :param request: The pytest request object that provides information about the test session.
    :return: An instance of the MatchingEngineHome class and passes to the test.
    """
    driver = basic_setup.driver
    header_option = request.param[0]
    sub_module = request.param[1]
    af_option = request.param[2]
    products_supported_heading_text = request.param[3]
    me_home = initialize_matching_engine_home(
        driver, header_option, sub_module, af_option, products_supported_heading_text)
    yield me_home

def initialize_matching_engine_home(driver, header_option, sub_module, af_option, products_supported_heading_text):
    """
    initialize_matching_engine_home()
    
    :Description: Helper method to initialize the MatchingEngineHome class and navigate to the required page.
    :param driver: The Selenium WebDriver instance.
    :param header_option: The header option to click on from home page.
    :param sub_module: The submodule to click on from the header option.
    :param af_option: The additional features option to click.
    :param products_supported_heading_text: The expected heading text to verify after clicking on {af_option}.
    :return: An instance of the MatchingEngineHome class.
    """
    me_home = MatchingEngineHome(driver)
    me_home.navigate_to_matching_engine_home()
    me_home.click_header_option(header_option)
    me_home.click_header_option(sub_module)
    me_home.click_products_supported(af_option, products_supported_heading_text)
    return me_home