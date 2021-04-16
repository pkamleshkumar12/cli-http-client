from cement import App
from cement import App, Controller, ex
from App.Configuration import Configuration
from App.services.RequestService import RequestService

class Base(Controller):
    class Meta:
        label = 'base'

    @ex(
        help='GET request Command',
        arguments=[
            (['-sn', '--systemName'],
             {'help': 'System Name',
              'action': 'store',
              'dest': 'systemName', }),
            (['-in', '--interfaceName'],
             {'help': 'Interface Name',
              'action': 'store',
              'dest': 'interfaceName', }),
            (['-vn', '--versionNumber'],
             {'help': 'Version Number',
              'action': 'store',
              'dest': 'versionNumber', }),
            (['-uc', '--useCase'],
             {'help': 'Use Case',
              'action': 'store',
              'dest': 'useCase', }),
            (['-env', '--environment'],
             {'help': 'Environment',
              'action': 'store',
              'dest': 'environment', }),
        ]
    )
    def get(self):
        self.app.log.info('Inside get command!')
        if self.app.pargs.systemName:
            self.app.log.info("Received option: systemName => %s" % self.app.pargs.systemName)
        if self.app.pargs.interfaceName:
            self.app.log.info("Received option: interfaceName => %s" % self.app.pargs.interfaceName)
        if self.app.pargs.versionNumber:
            self.app.log.info("Received option: versionNumber => %s" % self.app.pargs.versionNumber)
        if self.app.pargs.useCase:
            self.app.log.info("Received option: useCase => %s" % self.app.pargs.useCase)
        if self.app.pargs.environment:
            self.app.log.info("Received option: environment => %s" % self.app.pargs.environment)

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment
                               )

        r = RequestService(config)
        r.get_request()

    @ex(
        help='post request Command',
        arguments=[
            (['-sn', '--systemName'],
             {'help': 'System Name',
              'action': 'store',
              'dest': 'systemName', }),
            (['-in', '--interfaceName'],
             {'help': 'Interface Name',
              'action': 'store',
              'dest': 'interfaceName', }),
            (['-vn', '--versionNumber'],
             {'help': 'Version Number',
              'action': 'store',
              'dest': 'versionNumber', }),
            (['-uc', '--useCase'],
             {'help': 'Use Case',
              'action': 'store',
              'dest': 'useCase', }),
            (['-env', '--environment'],
             {'help': 'Environment',
              'action': 'store',
              'dest': 'environment', }),
        ]
    )
    def post(self):
        self.app.log.info('Inside post command!')
        if self.app.pargs.systemName:
            self.app.log.info("Received option: systemName => %s" % self.app.pargs.systemName)
        if self.app.pargs.interfaceName:
            self.app.log.info("Received option: interfaceName => %s" % self.app.pargs.interfaceName)
        if self.app.pargs.versionNumber:
            self.app.log.info("Received option: versionNumber => %s" % self.app.pargs.versionNumber)
        if self.app.pargs.useCase:
            self.app.log.info("Received option: useCase => %s" % self.app.pargs.useCase)
        if self.app.pargs.environment:
            self.app.log.info("Received option: environment => %s" % self.app.pargs.environment)

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment
                               )

        r = RequestService(config)
        r.post_request()


class CliHTTPClient(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
        ]


with CliHTTPClient() as app:
    app.run()
