from flask import Markup


class SeePeopleViewModel:

    def __init__(self, dataface_list: list, list_error: list = None, postback: bool = False):
        self.data_list = dataface_list

        self.postback = postback
        if self.postback:
            self.is_error: bool = list_error is not []
            if self.is_error:
                errors_message = '<br>'.join(list_error)
                self.message = Markup(f"Error for : {errors_message}")
            else:
                self.message = f"Success !"
