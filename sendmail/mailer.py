import os
import json
import boto3

class Mailer:
    def __init__(self, name=None, email=None):
        if name:
            self.set_name(name)
        if email:
            self.set_email(email)

        self.client = boto3.client('ses')

    def set_name(self, name):
        self.name = name
    
    def set_email(self, email):
        self.email = email

    def send_mail_all(self, recipients, template):
        destinations = []
        for recipient in recipients:
            obj = {}
            obj["Destination"] = {}
            obj["Destination"]["ToAddresses"] = [recipient.email]
            obj["ReplacementTemplateData"] = {}
            items = vars(recipient)
            for attr in items:
                if attr == "email":
                    continue
                obj["ReplacementTemplateData"][attr] = items[attr]
            obj["ReplacementTemplateData"] = json.dumps(obj["ReplacementTemplateData"])
            destinations.append(obj)

        default = {}
        for attr in vars(recipients[0]):
            default[attr] = attr
        default_template_data = json.dumps(default)

        try:
            _ = self.client.send_bulk_templated_email(
                Source=f"{self.name} <{self.email}>",
                ConfigurationSetName="Mentoring-Lolos-Rendering",
                Template=template,
                DefaultTemplateData=default_template_data,
                Destinations=destinations
            )
        except Exception as e:
            print(e)
