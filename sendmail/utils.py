from .helpers import dump_to_json, read_csv
from .mailer import Mailer
from .receiver import MailReceiverEntity

def csv_to_receivers(filename):
    rows = read_csv(filename)
    header = rows[0]
    delimiter = ","

    col = []
    for attr in header:
        col.append(str(attr))

    mail_receivers = []
    for row in rows[1:]:
        params = {}
        for idx, val in enumerate(row):
            if col[idx] == "":
                continue
            params[col[idx]] = val
        entity = MailReceiverEntity(**params)
        mail_receivers.append(entity)

    return mail_receivers
