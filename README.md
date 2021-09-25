# hmif-send-mail

Python package for automated mail sending

## Installation

### Building from source
Before building, you need to have setuptools and wheel installed:
```bash
python -m pip install --upgrade setuptools wheel
```

Then build the package and install the distribution. For the second command, change the version accordingly
```bash
python setup.py bdist_wheel && python -m pip install dist/sendmail-1.0.0-py3-none-any.whl
```

### Installing from PyPi (Currently not supported)
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
    name: HMIF Tech
    email: info@hmif.tech
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

### Example

#### Content of TestTemplate
```txt
Hello {{ fullName }}! Your verdict is: {{ verdictStatus }}
```

#### Content of data (`.csv`) file
The first row of the csv file must contains all variables required in the template, and must contains `email` column.
The `email` column is used for the recipients' email addresses.

```csv
email,fullName,verdictStatus
test@example.com,Test Recipient,success
test2@example.com,Test Recipient 2,failed
```

#### Result
The following email would be sent to `test@example.com` from `info@hmif.tech`

```txt
Hello Test Recipient! Your verdict is: success
```
