import requests
import os
from datetime import datetime
from App.services import IOService
import logging
import sys

class RequestService:
    path = None
    logger = None

    def __init__(self, config):
        """

            :type systemName: str
            """
        self.config = config
        self.env = self.load_env_variables()
        self.path = self.load_path()
        self.pathVariable = self.load_path_variable()
        self.queryParameters = self.load_query_parameter()
        self.setup_custom_logger()

    def get_request(self):
        logger = logging.getLogger()

        # Now we are going to Set the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.info(self.config)

        if self.config.loadRequestFileFrom:
            csv_list = IOService.load_csv(self.get_csv_request_file_path())

            # appending extra column to csv_list with query parameter
            csv_list = self.append_query_parameters(csv_list)
            url = self.get_request_url(False)

            # q_pos is last column of the csv_list, where query is appended
            q_pos = len(csv_list[0])
            r = None
            for rows in csv_list[1:]:
                if rows[q_pos]:
                    r = requests.get(url + '?' + rows[q_pos])
                else:
                    r = requests.get(url)

                print(r.text)
                logger.info(r.json())

        else:
            url = self.get_request_url(True)
            r = requests.get(url)
            print(r.text)
            logger.info(r.json())

    # FIXME param in request need not be formed

    def append_query_parameters(self, csv_list):

        # header is the header in the CSV file; Ignoring the first 2 headers used for flags
        keys = csv_list[0][2:]
        for row in range(1, len(csv_list)):
            parameters = ''
            j = 2
            for key in keys:
                if csv_list[row][j]:
                    parameters += key + '=' + csv_list[row][j] + '&'
                    j += 1
            csv_list[row].append(parameters[:-1])
        return csv_list

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

    def get_csv_request_file_path(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             self.config.loadRequestFileFrom)
        return os.path.sep.join(t)

    def get_request_url(self, queryFromConfiguration):
        host = ''.join(
            [
                str(self.env.get('protocol')),
                "://",
                str(self.env.get('host')),

            ])
        if self.env.get('port'):
            host += ":" + self.env.get('port')

        path = str(self.path.get('baseUrl'))
        if self.pathVariable.get('path'):
            path += "/" + str(self.pathVariable.get('path'))

        url = '/'.join([host, path])
        if self.get_query_parameter is not None and queryFromConfiguration:
            url += "?" + self.get_query_parameter()

        return url

    def post_request_url(self):
        host = ''.join(
            [
                str(self.env.get('protocol')),
                "://",
                str(self.env.get('host')),

            ])
        if self.env.get('port'):
            host += ":" + self.env.get('port')

        path = str(self.path.get('baseUrl'))
        if self.pathVariable.get('path'):
            path += "/" + str(self.pathVariable.get('path'))

        url = '/'.join([host, path])

        return url

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

    def get_query_parameter(self):
        queryString = None
        if len(self.queryParameters) != 0:
            queryString = ""
            for key in self.queryParameters:
                queryString += key + "=" + self.queryParameters[key] + "&"

        if len(self.queryParameters) > 0:
            queryString = queryString[:-1]

        return queryString

    def load_query_parameter(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'RequestQuery.json'
             )
        filePath = os.path.sep.join(t)
        return IOService.load_json(filePath)

    def set_log_file_path(self):
        if self.config.exportLogsTo:
            return os.path.join('logs',self.config.exportLogsTo)
        else:
            now = datetime.now()
            return os.path.join('logs', self.config.interfaceName + "_" + now.strftime("%H:%M:%S"))

    def setup_custom_logger(self):
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler(self.set_log_file_path(), mode='w')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(None)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
        return logger