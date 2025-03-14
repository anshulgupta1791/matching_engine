from pathlib import Path
import yaml
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
    me_home_page_title = matching_engine_home_data.page_title
    me_header_options = matching_engine_home_data.header_options

    # Additional Features
    additional_features_title = matching_engine_home_data.additional_features.title
    additional_features_options = matching_engine_home_data.additional_features.options

    # Products Supported
    products_supported_heading = matching_engine_home_data.additional_features.products_supported.heading
    products_list = matching_engine_home_data.additional_features.products_supported.products_list