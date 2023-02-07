from config import WEBSITE_NAME


class Utils:

    # This method is used to preformat a dict with all needed parameters for the render_template method
    # That allow to not have to say the website name each time per example
    @staticmethod
    def get_preformat_render(template, obj=None):
        return {"template_name_or_list": template, "title": WEBSITE_NAME, "obj": obj}

    # Same as get_preformat_render but allow to add custom parameters (If more than 1 object)
    @staticmethod
    def get_custom_preformat_render(template, **kwargs):
        return {"template_name_or_list": template, "title": WEBSITE_NAME, **kwargs}
