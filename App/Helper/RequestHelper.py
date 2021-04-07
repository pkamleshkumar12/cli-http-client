import requests
import json
import os


class RequestHelper:
    def __init__(self, systemName, interfaceName, versionNumber, useCase):
        """

            :type systemName: str
            """
        self.systemName = systemName
        self.interfaceName = interfaceName
        self.versionNumber = versionNumber
        self.useCase = useCase

    def getRequest(self):
        print(" " + self.interfaceName)
        r = requests.get('https://606c16c9f8678400172e7274.mockapi.io/api/v1/customers')
        print(r.text)

    def postRequest(self):
        payload = self.loadJson()
        r = requests.post('https://606c16c9f8678400172e7274.mockapi.io/api/v1/customers', data=payload)
        print(r.text)

    def loadJson(self):
        """

        :rtype: object
        """
        t = ('data',
             self.systemName,
             self.interfaceName,
             self.versionNumber,
             self.useCase,
             'RequestBody.json')
        filePath = os.path.sep.join(t)
        print(filePath)
        with open(filePath) as f:
            data = json.load(f)
            print('requestBody')
            print(data)

        return data
