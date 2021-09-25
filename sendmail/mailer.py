import os
import json
import boto3

from .helpers import file_to_raw

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
    
    def create_template(self, template_name, subject, html_file, text_file):
        try:
            Template = {
                "TemplateName": template_name,
                "SubjectPart": subject,
            }
            if html_file:
                Template["HtmlPart"] = file_to_raw(html_file)
            if text_file:
                Template["TextPart"] = file_to_raw(text_file)
            _ = self.client.create_template(
                Template=Template
            )
        except Exception as e:
            print(e)

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
