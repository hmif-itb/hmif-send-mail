class EmailHeaderNotFoundException(Exception):
    def __init__(self, filename):
        super().__init__(f"email header not found in file {filename}")

class InvalidRecipientEntityException(Exception):
    def __init__(self):
        super().__init__(f"no email address found, maybe check your .csv header?")

class TemplateNotFoundException(Exception):
    def __init__(self, template_name):
        super().__init__(f"An error occurred (TemplateDoesNotExist) when calling the GetTemplate operation: Template {template_name} does not exist.")

class TemplateAndCSVNotMatchException(Exception):
    def __init__(self, template_name, csv_name, field):
        super().__init__(f"An error occured. Template {template_name} contains a field not populated in {csv_name} (Field '{field}' exist in template but not in csv file)")
