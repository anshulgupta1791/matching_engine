from pathlib import Path
import yaml
from selenium.webdriver.common.by import By
from framework import ROOT_DIR
from dotmap import DotMap

class MatchingEngineHomeConfig:
    """
    Configuration class for Matching Engine Home.
    """
    matching_engine_home_data_path = (
        Path(f'{ROOT_DIR}/utils/frontend/matching_engine_home/matching_engine_home_data.yaml'))
    yaml_data = yaml.safe_load(matching_engine_home_data_path.read_text())
    matching_engine_home_data = DotMap(yaml_data['matching_engine_home_data'])

    # Home Page
    me_home_page_title = (By.XPATH, matching_engine_home_data.page_title)
    me_header_options = (By.XPATH, matching_engine_home_data.header_options)