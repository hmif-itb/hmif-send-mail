from .helpers import dump_to_json, read_csv
from .mailer import Mailer
from .recipient import MailRecipientEntity

def csv_to_recipients(filename):
    rows = read_csv(filename)
    header = rows[0]
    delimiter = ","

    col = []
    for attr in header:
        col.append(str(attr))

    recipients = []
    for row in rows[1:]:
        params = {}
        for idx, val in enumerate(row):
            params[col[idx]] = val
        entity = MailRecipientEntity(**params)
        recipients.append(entity)

    return recipients
