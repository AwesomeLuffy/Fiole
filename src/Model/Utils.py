from typing import Match

from app_config import WEBSITE_NAME
from enum import Enum
import re


class FieldsType(Enum):
    DA = 1
    NAME = 2
    FILE = 3


class Utils:
    PATTERN_REGEX_DA = re.compile("^[0-9]{9,12}$")

    PATTERN_REGEX_NAME = re.compile("^[a-zA-ZÀ-ÿ\\-\\s]{1,40}$")

    LIST_ACCEPT_FILES = [".jpg", ".jpeg", ".png"]

    # This method is used to preformat a dict with all needed parameters for the render_template method
    # That allow to not have to say the website name each time per example
    @staticmethod
    def get_preformat_render(template, obj=None):
        return {"template_name_or_list": template, "title": WEBSITE_NAME, "obj": obj}

    # Same as get_preformat_render but allow to add custom parameters (If more than 1 object)
    @staticmethod
    def get_custom_preformat_render(template, **kwargs):
        return {"template_name_or_list": template, "title": WEBSITE_NAME, **kwargs}

    # Method to verify field from a form
    @staticmethod
    def verify_field(field: str, field_type: FieldsType) -> Match[str] | None | bool:
        if field_type == FieldsType.DA:
            return Utils.PATTERN_REGEX_DA.match(field)
        elif field_type == FieldsType.NAME:
            return Utils.PATTERN_REGEX_NAME.match(field)
        elif field_type == FieldsType.FILE:
            return field.split(".")[-1] not in Utils.LIST_ACCEPT_FILES
        else:
            return False
