import os
import json
import boto3

from .helpers import dump_to_json

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

    def create_json_send(self, receiver, template):
        tmp = {}
        tmp["Source"] = f"{self.name} <{self.email}>"
        tmp["Template"] = template
        tmp["ConfigurationSetName"] = "Mentoring-Lolos-Rendering"
        tmp["Destination"] = {}
        tmp["Destination"]["ToAddresses"] = [receiver.email]
        tmp["TemplateData"] = {}
        items = vars(receiver)
        for attr in items:
            if attr == "email":
                continue
            tmp["TemplateData"][attr] = items[attr]
        tmp["TemplateData"] = json.dumps(tmp["TemplateData"])
        dump_to_json(tmp, "./tmp/tes.json")

    def send_mail_all(self, receivers, template):
        destinations = []
        for receiver in receivers:
            obj = {}
            obj["Destination"] = {}
            obj["Destination"]["ToAddresses"] = [receiver.email]
            obj["ReplacementTemplateData"] = {}
            items = vars(receiver)
            for attr in items:
                if attr == "email":
                    continue
                obj["ReplacementTemplateData"][attr] = items[attr]
            obj["ReplacementTemplateData"] = json.dumps(obj["ReplacementTemplateData"])
            destinations.append(obj)

        default = {}
        for attr in vars(receivers[0]):
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
