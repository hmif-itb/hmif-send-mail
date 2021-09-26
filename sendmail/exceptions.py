class EmailHeaderNotFoundException(Exception):
    def __init__(self, filename):
        super().__init__(f"email header not found in file {filename}")

class InvalidRecipientEntityException(Exception):
    def __init__(self):
        super().__init__(f"no email address found, maybe check your .csv header?")
