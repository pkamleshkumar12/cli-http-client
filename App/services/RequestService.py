import requests
import os

from App.services import IOService


class RequestService:

    path = None

    def __init__(self, config):
        """

            :type systemName: str
            """
        self.config = config
        self.env = self.load_env_variables()
        self.path = self.load_path()
        self.pathVariable = self.load_path_variable()

    def get_request(self):
        url = self.get_request_url()
        print('url ->', url)
        r = requests.get(url)
        print(r.text)

    def post_request(self):
        payload = IOService.load_json(self.get_request_file_path())
        url = self.post_request_url()
        print('payload -> ', payload)
        print('url ->', url)
        r = requests.post(url, data=payload)
        print(r.text)

    def get_request_file_path(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'RequestBody.json')
        return os.path.sep.join(t)

    def get_request_url(self):
        host = ''.join(
            [
                str(self.env.get('protocol')),
                "://",
                str(self.env.get('host')),

            ])

        path = "/".join(
            [
                str(self.path.get('baseUrl')),
                str(self.pathVariable.get('path'))
            ]
        )
        return '/'.join([host, path])

    def post_request_url(self):
        host = ''.join(
            [
                str(self.env.get('protocol')),
                "://",
                str(self.env.get('host')),

            ])

        path = "/".join(
            [
                str(self.path.get('baseUrl'))
            ]
        )
        return '/'.join([host, path])

    def get_query_file_path(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'RequestBody.json')
        return os.path.sep.join(t)

    def load_env_variables(self):
        t = ('data',
             self.config.systemName,
             'config.json'
             )
        envFilePath = os.path.sep.join(t)
        json = IOService.load_json(envFilePath)
        return json.get('env').get(self.config.environment)

    def load_path(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             'path.json'
             )
        filePath = os.path.sep.join(t)
        return IOService.load_json(filePath)

    def load_path_variable(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'PathVariable.json'
             )
        filePath = os.path.sep.join(t)
        return IOService.load_json(filePath)