import argparse
from .helpers import yaml_parser
from .mailer import Mailer
from .utils import csv_to_recipients

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="yaml file as mail configuration")
    parser.add_argument("--service", help="mail service")
    parser.add_argument("--mode", help="package app mode", default="send_email")
    parser.add_argument("--template-name", help="name of the template to be made")
    parser.add_argument("--subject", help="subject of the email")
    parser.add_argument("--txt", help="txt template content of the email")
    parser.add_argument("--html", help="html template content of the email")
    args = parser.parse_args()

    mode = args.mode
    service = args.service

    if args.service == "aws":

        if mode == "create_template":
            mailer = Mailer()

            template_name = args.template_name
            subject = args.subject
            txt = args.txt
            html = args.html

            mailer.create_template(template_name, subject, html, txt)

        elif mode == "send_email":
            config_yaml_file = args.config
            config_data = yaml_parser(config_yaml_file)

            for items in config_data:
                sender_name = items["sender"]["name"]
                sender_email = items["sender"]["email"]
                mailer = Mailer(sender_name, sender_email)
                
                for spec in items["spec"]:
                    template_name = spec["template"]
                    template_data = spec["recipient_data"]

                    try:
                        mail_recipients = csv_to_recipients(template_data)
                        mailer.send_mail_all(mail_recipients, template_name)
                    except Exception as e:
                        print(e)
