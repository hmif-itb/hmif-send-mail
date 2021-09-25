import json
import yaml
import csv

def file_to_raw(filename):
    with open(filename, "r") as file:
        f = file.read()
        return f

def dump_to_json(data, filename):
    with open(filename, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False)

def read_csv(filename):
    rows = []
    with open(filename, newline="") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",", quotechar=" ")
        for row in csv_reader:
            rows.append(row)
    return rows

def yaml_parser(yaml_file):
    with open(yaml_file, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)
