from pathlib import Path
import yaml
from framework import ROOT_DIR
from framework.utils.frontend.matching_engine_home.matching_engine_home_config import (
    MatchingEngineHomeConfig as me_config)
from framework.utils.frontend.fe_general import FEGeneral as fe_general

class MatchingEngineHome:
    config = me_config
    config_sample_path = Path(f'{ROOT_DIR}/utils/config_sample.yaml')
    with config_sample_path.open() as file:
        config_data = yaml.safe_load(file)
    url = config_data.get('url')

    def __init__(self, driver=None):
        super(MatchingEngineHome, self).__init__(driver)
        self.fe_general = fe_general(driver)

    def navigate_to_matching_engine_home(self):
        """
        navigate_to_matching_engine_home()

        :Description: Navigate to the Matching Engine Home page.
        :return: None
        """
        self.fe_general.go_to_page()
        print(f'Navigating to {self.url}')
        self.fe_general.verify_element_present(self.url, page_url=True)

    def click_header_option(self, header_option):
        """
        click_header_option(header_option)

        :Description: Click on the specified header option.
        :param header_option: The header option to click on.
        :return: None
        """
        locator = self.fe_general.format_locator(locator=self.config.me_header_options, value=header_option)
        self.fe_general.click_element(locator)

