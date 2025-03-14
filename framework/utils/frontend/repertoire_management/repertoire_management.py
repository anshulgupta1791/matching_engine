from framework.utils.frontend.repertoire_management.repertoire_management_config import (
    RepertoireManagementConfig as rm_config)
from framework.utils.frontend.fe_general import FEGeneral as fe_general

class RepertoireManagement:
    config = rm_config

    def __init__(self, driver=None):
        super(RepertoireManagement, self).__init__(driver)
        self.fe_general = fe_general(driver)

    def click_additional_features_option(self, option):
        """
        click_additional_features_option(option)

        :Description: Clicks on an additional feature option in the Repertoire Management page.
        :param option:(str) The option to be clicked.
        :return: None
        """
        self.fe_general.scroll_into_view(self.config.additional_features_title)
        locator = self.fe_general.format_locator(locator=self.config.sub_list, value=option)
        self.fe_general.click_element(locator)