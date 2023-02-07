class AddPeopleViewModel:

    def __init__(self, count: int = 0, is_error: bool = False):
        self.is_error: bool = is_error
        self.count: int = count
        if self.is_error:
            self.message = f"Error occured, {count:02d} added"
        else:
            self.message = f"Success ! {count:02d} added !"
