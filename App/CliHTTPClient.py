from cement.core.foundation import CementApp
from App.controllers.MainController import MainController


class CliHTTPClient(CementApp):
    class Meta:
        label = 'CliApp'
        handlers = [
            MainController
        ]


def main():
    with CliHTTPClient() as app:
        app.config.parse_file('config.conf')
        app.run()

