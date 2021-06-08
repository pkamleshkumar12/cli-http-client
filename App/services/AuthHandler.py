from __future__ import annotations

import sys
from abc import ABC, abstractmethod
from typing import Any, Optional
import os
from App.Configuration import Configuration
from App.services import IOService
import requests


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
        super().handle(request, headers, configs)


class CustomSLAuthenticationHandler(AbstractHandler):
    def handle(self, request: Any, headers, configs) -> str:

        if request.get("type") == "Custom_Auth_SL":

            try:
                print('Handled at CustomSLOauth')
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

                r = requests.post(url, json=payload, headers=auth_headers)
                response_json = r.json()
                print("r: ", r)
                print("response:", r.json())
                authorization_token = response_json.get('userDetails').get('utoken')
                print("token from the authorization server: ", authorization_token)
                headers["Authorization"] = authorization_token
                return f"Handled at CustomSLAuthenticationHandler {request}"
            except FileNotFoundError as fnf_error:
                SystemExit(fnf_error)
            except Exception as e:
                print("Exception occurred while handling Custom_Auth_SL")
                SystemExit(e)
                sys.exit()

        else:
            return super().handle(request, headers, configs)


class CustomSFDCOauth(AbstractHandler):

    def handle(self, request: Any, headers, configs) -> str:

        if request.get("type") == "Custom_Auth_SFDC":
            try:
                print('Handled at CustomSFDCOauth')
                payload = {
                    'grant_type': request.get('grant_type'),
                    'client_id': request.get('client_id'),
                    'client_secret': request.get('client_secret'),
                    'username': request.get('username'),
                    'password': request.get('password')
                }

                url = request.get("authorization_url")

                response = requests.post(url, data=payload)
                response_json = response.json()
                print("response from SFDC auth server: ", response_json)

                access_token = response_json.get('access_token')
                headers['Authorization'] = "Bearer " + access_token
                return "yes"
            except FileNotFoundError as fnf_error:
                SystemExit(fnf_error)
                sys.exit()
            except Exception as e:
                print("Exception occurred while handling Custom_Auth_SFDC")
                SystemExit(e)
                sys.exit()

        else:
            return super().handle(request, headers, configs)


def client_code(handler: Handler, auth_json, headers, config) -> None:
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """

    result = handler.handle(auth_json, headers, config)
    print('result: ', result)
    if result:
        print(f"  {result}", end="")
    else:
        print(f"  {auth_json} was left unhandled.", end="")


class AuthHandler:
    def __init__(self, config: Configuration, headers: dict):

        basicAuthHandler = BasicAuthenticationHandler()
        customSLAuthHandler = CustomSLAuthenticationHandler()
        customSFDCAuthHandler = CustomSFDCOauth()

        basicAuthHandler.set_next(customSLAuthHandler).set_next(customSFDCAuthHandler)

        # The client should be able to send a request to any handler

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
