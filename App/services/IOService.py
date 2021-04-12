import json
import os


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
