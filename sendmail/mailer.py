import os
import json
import boto3
import re
from tqdm import tqdm

from .helpers import file_to_raw
from .helpers import get_csv_headers
from botocore.exceptions import ClientError
from .exceptions import TemplateNotFoundException
from .exceptions import TemplateAndCSVNotMatchException

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
    
    def set_template(self, template):
        if "HtmlPart" in template:
            self.template_html = template["HtmlPart"]
        if "TextPart" in template:
            self.template_txt = template["TextPart"]

    def check_template_exist(self, template_name):
        try:
            r = self.client.get_template(
                TemplateName=template_name
            )
            self.set_template(r["Template"])
        except ClientError as e:
            if e.response['Error']['Code'] == "TemplateDoesNotExist":
                raise TemplateNotFoundException(template_name)
    
    def get_vars_from_template(self, raw_template):
        tokens = re.findall("{{ [^}]* }}", raw_template)
        tokens = list(map(lambda x: x[3:-3], tokens))
        return tokens

    def check_template_match(self, template_name, template_data):
        variables = []
        if self.template_html:
            variables = self.get_vars_from_template(self.template_html)
        elif self.template_txt:
            variables = self.get_vars_from_template(self.template_txt)
        else:
            raise TemplateNotFoundException(template_name)
        
        headers = get_csv_headers(template_data)
        for var in variables:
            if var not in headers:
                raise TemplateAndCSVNotMatchException(template_name, template_data, var)

    def send_mail(self, recipients, template):
        progress = tqdm(total=len(recipients))
        for recipient in recipients:
            destination = {}
            destination["ToAddresses"] = [recipient.email]
            template_data = json.dumps(vars(recipient))
            try:
                r = self.client.send_templated_email(
                    Source=f"{self.name} <{self.email}>",
                    ConfigurationSetName="Mentoring-Lolos-Rendering",
                    Template=template,
                    Destination=destination,
                    TemplateData=template_data
                )
                print(f"\nSuccess sending to {recipient.email}")
                progress.update(1)
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
