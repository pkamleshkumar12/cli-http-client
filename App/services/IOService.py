import json
import csv


class IOService:
    def __init__(self):
        pass


def load_json(filePath):
    """
        :rtype: object
        """
    try:
        with open(filePath) as f:
            data = json.load(f)

        return data
    except FileNotFoundError as fnf_error:
        print('Could not open json file; path:', filePath)
        SystemExit(fnf_error)


def load_csv(filePath):
    csv_in_list = list()
    try:
        with open(filePath, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, skipinitialspace=True)
            for row in reader:
                csv_in_list.append(list(row))

        return csv_in_list
    except FileNotFoundError as fnf_error:
        print('Could not open csv file; path:', filePath)
        SystemExit(fnf_error)


def load_xml(filePath):
    try:
        with open(filePath, 'r') as f:
            data = f.read()
        return data
    except FileNotFoundError as fnf_error:
        print('Could not open xml file; path:', filePath)
        print(fnf_error)
        SystemExit(fnf_error)
