class InvalidDataError(Exception):
    def __init__(self, message, error, data):
        super().__init__(message)

        self.error = error
        self.data = data

    def __repr__(self):
        return f'Errors: {self.error} with full response {self.data}'

    def __str__(self):
        return f'Errors: {self.error} with full response {self.data}'
