from typing import Match

from app_config import WEBSITE_NAME
from enum import Enum
from src.Model.Database.database_handler import DatabaseHandler
import re


class Utils:

    # This method is used to preformat a dict with all needed parameters for the render_template method
    # That allow to not have to say the website name each time per example
    @staticmethod
    def get_preformat_render(template, obj=None):
        """Method to preformat a dict with all needed parameters for the render_template method
        The main purpose is to not have to say the website name each time per example
        :param template: The template name
        :param obj: The object to pass to the template
        """
        return {"template_name_or_list": template, "title": WEBSITE_NAME, "obj": obj}

    # Same as get_preformat_render but allow to add custom parameters (If more than 1 object)
    @staticmethod
    def get_custom_preformat_render(template, **kwargs):
        """Method to preformat a dict with all needed parameters for the render_template method
        Same as get_preformat_render but allow to add custom parameters (If more than 1 object)
        """
        return {"template_name_or_list": template, "title": WEBSITE_NAME, **kwargs}


