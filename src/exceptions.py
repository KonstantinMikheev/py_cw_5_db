class APIExceptions(Exception):
    """
    Общий класс исключений для работы с API
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HeadHunterAPIException(APIExceptions):
    pass
