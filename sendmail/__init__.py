
import argparse
from .helpers import yaml_parser
from .mailer import Mailer
from .utils import csv_to_receivers

def test():
    return ("hello world")

def send_mail():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="yaml file as mail configuration")
    args = parser.parse_args()

    config_yaml_file = args.config
    config_data = yaml_parser(config_yaml_file)

    for items in config_data:
        sender_name = items["sender"]["name"]
        sender_email = items["sender"]["email"]

        mailer = Mailer(sender_name, sender_email)
        
        for spec in items["spec"]:
            template_name = spec["template"]
            template_data = spec["receiver_data"]

            mail_receivers = csv_to_receivers(template_data)
            mailer.send_mail_all(mail_receivers, template_name)
