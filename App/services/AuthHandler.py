from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional
import os
from App.Configuration import Configuration
from App.services import IOService
import requests
import json


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request, headers, configs) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # basicAuth.set_next(oauth2).set_next(custom_Auth)
        return handler

    @abstractmethod
    def handle(self, request: Any, headers, configs) -> str:
        if self._next_handler:
            return self._next_handler.handle(request, headers, configs)

        return None


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""


class BasicAuthenticationHandler(AbstractHandler):
    def handle(self, request: Any, headers, configs) -> str:
        super().handle(request)


class CustomSLAuthenticationHandler(AbstractHandler):
    def handle(self, request: Any, headers, configs) -> str:

        if request.get("type") == "Custom_Auth_SL":

            t = ('data',
                 configs.systemName,
                 configs.interfaceName,
                 configs.versionNumber,
                 configs.useCase,
                 'AuthBody.json')
            auth_body_file_path = os.path.sep.join(t)
            payload = IOService.load_json(auth_body_file_path)

            t = ('data',
                 configs.systemName,
                 configs.interfaceName,
                 configs.versionNumber,
                 configs.useCase,
                 'AuthHeader.json')
            auth_header_file_path = os.path.sep.join(t)
            auth_headers = IOService.load_json(auth_header_file_path)

            url = request.get("authorization_url")

            r = requests.post(url, data=payload, headers=auth_headers)
            response_json = r.json()

            authorization_token = response_json.get('userDetails').get('utoken')
            print("token from the authorization server: ", authorization_token)
            headers["Authorization"] = authorization_token
            return f"Handled at CustomSLAuthenticationHandler {request} "
        else:
            return super().handle(request)


def client_code(handler: Handler, auth_json, headers, config) -> None:
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """

    # auth_type = auth_json.get("type")

    result = handler.handle(auth_json, headers, config)
    if result:
        print(f"  {result}", end="")
    else:
        print(f"  {auth_json} was left unhandled.", end="")


class AuthHandler:
    def __init__(self, config: Configuration, headers: dict):

        basicAuthHandler = BasicAuthenticationHandler()
        customerSLAuthHandler = CustomSLAuthenticationHandler()

        basicAuthHandler.set_next(customerSLAuthHandler)

        # The client should be able to send a request to any handler

        print("Chain: Basic Auth > Customer SL Auth")

        t = ('data',
             config.systemName,
             config.interfaceName,
             config.versionNumber,
             config.useCase,
             'Auth.json'
             )
        filePath = os.path.sep.join(t)
        auth_json = IOService.load_json(filePath)

        if bool(auth_json):
            client_code(basicAuthHandler, auth_json, headers, config)
        else:
            pass
