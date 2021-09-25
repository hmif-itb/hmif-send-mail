# hmif-send-mail

Python package for automated mail sending

## Installation
```bash
python -m pip install sendmail
```

## Usage example
```bash
python -m sendmail --config=template.yml --service=aws
```

## Template example
```yaml
- sender:
    name: HMIF Careers
    email: careers@hmif.tech
  specs:
  - template: TestTemplate
    recipient_data: file.csv
```
### Template file documentation
| Variable | Description |
| ------------- | ------------- | 
| `sender` | `sender` object |
| `sender.name`| The name of the sender shown in the email | 
| `sender.email` | The email for sending |   
| `specs` | List of `spec` object |   
| `spec.template` | The name of the template used for the email |   
| `spec.recipient_data` | path to a csv file containing recipient data (email, and variables to replace in the template file) |   
