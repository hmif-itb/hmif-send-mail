class EmailHeaderNotFoundException(Exception):
    def __init__(self, filename):
        super().__init__(f"email header not found in file {filename}")
