from pathlib import Path
import yaml
from selenium.webdriver.common.by import By
from framework import ROOT_DIR
from dotmap import DotMap


class RepertoireManagementConfig:
    """
    Configuration class for Repertoire Management.
    """
    repertoire_management_data_path = (
        Path(f'{ROOT_DIR}/utils/frontend/repertoire_management/repertoire_management_data.yaml'))
    yaml_data = yaml.safeload(repertoire_management_data_path.read_text())
    repertoire_management_data = DotMap(yaml_data['repertoire_management_data'])

    # Additional Features
    additional_features_title = (By.XPATH, repertoire_management_data.additional_features.title)
    sub_list = (By.XPATH, repertoire_management_data.additional_features.sub_list)