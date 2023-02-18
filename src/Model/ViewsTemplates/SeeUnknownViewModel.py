class SeeUnknownViewModel:

    def __init__(self, unknown_list: list, postback: bool = False, count_affected: int = -1):
        self.unknown_list = unknown_list
        self.postback = postback
        self.is_error = False
        if self.postback:
            self.is_error: bool = count_affected == -1
            if self.is_error:
                self.message = f"Error occured..."
            else:
                self.message = f"Success ! {count_affected} deleted !"
