import os
import json
from .helpers import dump_to_json

class Mailer:
    def __init__(self, name=None, email=None):
        if name:
            self.set_name(name)
        if email:
            self.set_email(email)

    def set_name(self, name):
        self.name = name
    
    def set_email(self, email):
        self.email = email

    def send(self, receiver, template):
        self.create_json_send(receiver, template)
        os.system('cmd /c "aws ses send-templated-email --cli-input-json file://tmp/tes.json"')

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

    def send_mail_one_by_one(self, receivers, template):
        for receiver in receivers:
            self.send(receiver, template)
    
    def send_mail_all(self, receivers, template):
        tmp = {}
        tmp["Source"] = f"{self.name} <{self.email}>"
        tmp["Template"] = template
        tmp["ConfigurationSetName"] = "Mentoring-Lolos-Rendering"
        tmp["Destinations"] = []
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
            tmp["Destinations"].append(obj)
        default = {}
        for attr in vars(receivers[0]):
            default[attr] = attr
        tmp["DefaultTemplateData"] = json.dumps(default)
        dump_to_json(tmp, "./tmp/tes.json")
        os.system('cmd /c "aws ses send-bulk-templated-email --cli-input-json file://tmp/tes.json"')
