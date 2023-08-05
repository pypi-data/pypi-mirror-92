
class ApiError(Exception):
    def __init__(self, msg, function_name, result):
        super(ApiError, self).__init__(f"An Error Occured :  {msg}")
        self.function_name = function_name
        self.result = result


class TelegramConnectionError(Exception):
    pass
