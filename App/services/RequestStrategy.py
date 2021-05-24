from __future__ import annotations
from abc import ABC, abstractmethod
from App import Configuration
from typing import Any
import json
import requests
import os

from datetime import datetime
from App.services import IOService

import logging
import sys
from App.services.AuthHandler import AuthHandler


class Context:

    def __init__(self, strategy: RequestStrategy, config: Configuration) -> None:
        self.config = config
        self._strategy = strategy
        self.logger = self.setup_custom_logger()

    @property
    def strategy(self) -> RequestStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: RequestStrategy) -> None:
        self._strategy = strategy

    def do_get_request(self) -> None:
        result = self._strategy.send_get_request(self.config,
                                                 self.logger)
        print(result)

    def do_post_request(self) -> None:
        result = self._strategy.send_post_request(self.config,
                                                  self.logger)
        print(result)

    def do_delete_request(self) -> None:
        result = self._strategy.send_delete_request(self.config,
                                                    self.logger)
        print(result)

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

    def set_log_file_path(self):
        if self.config.exportLogsTo:
            return os.path.join('logs', self.config.exportLogsTo)
        else:
            now = datetime.now()
            return os.path.join('logs', self.config.interfaceName + "_" + now.strftime("%H%M%S") + ".log")


class RequestStrategy(ABC):

    @abstractmethod
    def send_get_request(self, configuration: Configuration, logger):
        pass

    @abstractmethod
    def send_post_request(self, configuration: Configuration, logger):
        pass

    @abstractmethod
    def send_delete_request(self, configuration: Configuration, logger):
        pass


class RequestStrategyBySOAP(RequestStrategy):

    def __init__(self):
        self.config = None
        self.headers = None
        self.env = None
        self.path = None
        self.pathVariable = None
        self.queryParameters = None

    def send_get_request(self, configuration,
                         logger) -> str:
        logger.info(configuration)
        return "SOAP Get Request Executed"

    def send_post_request(self, configuration,
                          logger) -> str:
        self.config = configuration
        self.env = self.load_env_variables()
        self.path = self.load_path()
        self.headers = self.load_headers()
        self.pathVariable = self.load_path_variable()
        self.queryParameters = self.load_query_parameter()

        logger.info(self.config)
        print("configuration: ", configuration)
        print("headers: ", self.headers)
        AuthHandler(self.config, self.headers)
        url = self.post_request_url()

        payload = IOService.load_xml(self.get_request_file_path())
        print('payload -> ', payload)
        print('url ->', url)
        r = requests.post(url, data=payload, headers=self.headers)
        print(r.text)
        return "SOAP Post Request Executed"

    def send_delete_request(self, configuration: Configuration, logger):
        return "SOAP Delete Request Executed"

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

    def get_request_file_path(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'RequestBody.xml')
        return os.path.sep.join(t)

    def load_env_variables(self):
        t = ('data',
             self.config.systemName,
             'config.json'
             )
        envFilePath = os.path.sep.join(t)
        json_env = IOService.load_json(envFilePath)
        return json_env.get('env').get(self.config.environment)

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

    def load_headers(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'Header.json'
             )
        filePath = os.path.sep.join(t)
        return IOService.load_json(filePath)

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


class RequestStrategyByREST(RequestStrategy):

    def __init__(self):
        self.config = None
        self.headers = None
        self.env = None
        self.path = None
        self.pathVariable = None
        self.queryParameters = None

    def send_get_request(self, configuration: Configuration,
                         logger) -> str:
        self.config = configuration
        self.env = self.load_env_variables()
        self.path = self.load_path()
        self.headers = self.load_headers()
        self.pathVariable = self.load_path_variable()
        self.queryParameters = self.load_query_parameter()

        logger.info(self.config)
        print("configuration: ", configuration)
        print("headers: ", self.headers)

        AuthHandler(self.config, self.headers)
        url = self.get_request_url()
        print("url: ", url)
        r = requests.get(url, headers=self.headers)
        print("response: ", r.text)
        logger.info(r.json())

        return "REST Get Request Executed!!"

    def send_post_request(self, configuration,
                          logger) -> str:
        self.config = configuration
        self.env = self.load_env_variables()
        self.path = self.load_path()
        self.headers = self.load_headers()
        self.pathVariable = self.load_path_variable()
        self.queryParameters = self.load_query_parameter()

        logger.info(self.config)
        print("configuration: ", configuration)
        print("headers: ", self.headers)

        AuthHandler(self.config, self.headers)
        payload = IOService.load_json(self.get_request_file_path())
        url = self.post_request_url()
        print('payload -> ', payload)
        print('url ->', url)
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        print(r.text)
        logger.info(r.json())

        return "REST Post Request Executed!!"

    def send_delete_request(self, configuration: Configuration, logger):
        pass

    def load_env_variables(self):
        t = ('data',
             self.config.systemName,
             'config.json'
             )
        envFilePath = os.path.sep.join(t)
        json_env = IOService.load_json(envFilePath)
        return json_env.get('env').get(self.config.environment)

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

    def load_headers(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'Header.json'
             )
        filePath = os.path.sep.join(t)
        return IOService.load_json(filePath)

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

    def get_request_url(self):
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
        if self.get_query_parameter() is not None:
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

    def get_query_parameter(self):
        queryString = None
        if len(self.queryParameters) != 0:
            queryString = ""
            for key in self.queryParameters:
                queryString += key + "=" + self.queryParameters[key] + "&"

        if len(self.queryParameters) > 0:
            queryString = queryString[:-1]

        return queryString

    def get_request_file_path(self):
        t = ('data',
             self.config.systemName,
             self.config.interfaceName,
             self.config.versionNumber,
             self.config.useCase,
             'RequestBody.json')
        return os.path.sep.join(t)
