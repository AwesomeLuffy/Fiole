from flask import Markup


class AddPeopleViewModel:

    def __init__(self, count: int, list_error: list):
        self.is_error: bool = list_error is not None and len(list_error) > 0
        self.count: int = count
        if self.is_error:
            errors_message = '<br>'.join(list_error)
            self.message = Markup(f"{count:02d} added<br>Error for : {errors_message}")
        else:
            self.message = f"Success ! {count:02d} added !"
