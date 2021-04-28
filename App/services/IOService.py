import json
import csv
import os
from cement.utils.misc import init_defaults


class IOService:
    def __init__(self):
        pass


def load_json(filePath):
    """
        :rtype: object
        """
    with open(filePath) as f:
        data = json.load(f)

    return data


def load_csv(filePath):
    csv_in_list = list()
    with open(filePath, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, skipinitialspace=True)
        for row in reader:
            csv_in_list.append(list(row))

    return csv_in_list
