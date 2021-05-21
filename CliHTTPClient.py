from cement import App
from cement import App, Controller, ex
from App.Configuration import Configuration
from cement.utils.misc import init_defaults
from App.services.RequestStrategy import RequestStrategyBySOAP, Context, RequestStrategyByREST


class Base(Controller):
    class Meta:
        label = 'base'

    @ex(
        help='GET Request Command',
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
            (['--loadRequestFileFrom'],
             {'help': 'file location to load requests',
              'action': 'store',
              'dest': 'loadRequestFileFrom', }),
            (['--exportLogsTo'],
             {'help': 'export logs to give file name ',
              'action': 'store',
              'dest': 'exportLogsTo', }),
            (['-ws', '--webservice'],
             {'help': 'specify the type of web service, eg: SOAP, REST(default)',
              'action': 'store',
              'dest': 'webService', }),
        ]
    )
    def get(self):
        self.app.log.info('Inside get command!')
        ws = ""
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
        if self.app.pargs.loadRequestFileFrom:
            self.app.log.info("Received option: loadRequestFileFrom => %s" % self.app.pargs.loadRequestFileFrom)
        if self.app.pargs.exportLogsTo:
            self.app.log.info("Received option: exportLogsTo => %s" % self.app.pargs.exportLogsTo)
        if self.app.pargs.webService:
            self.app.log.info("Received option: webService => %s" % self.app.pargs.webService)
            ws = self.app.pargs.webService

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment,
                               self.app.pargs.loadRequestFileFrom,
                               self.app.pargs.exportLogsTo,
                               self.app.pargs.webService)

        context = Context(RequestStrategyBySOAP(), config)
        if ws == "SOAP":
            self.app.log.info("Client: Strategy is set to SOAP web service")
            context.do_get_request()
        else:
            self.app.log.info("Client: Strategy is set to REST web service")
            context.strategy = RequestStrategyByREST()
            context.do_get_request()

    @ex(
        help='Post Request Command',
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
            (['-ws', '--webservice'],
             {'help': 'specify the type of web service, eg: SOAP, REST(default)',
              'action': 'store',
              'dest': 'webService', }),
        ]
    )
    def post(self):
        self.app.log.info('Inside post command!')
        ws = ""
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
        if self.app.pargs.webService:
            self.app.log.info("Received option: webService => %s" % self.app.pargs.webService)
            ws = self.app.pargs.webService

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment,
                               None,
                               None,
                               self.app.pargs.webService)

        context = Context(RequestStrategyBySOAP(), config)
        if ws == "SOAP":
            self.app.log.info("Client: Strategy is set to SOAP web service")
            context.do_post_request()
        else:
            self.app.log.info("Client: Strategy is set to REST web service")
            context.strategy = RequestStrategyByREST()
            context.do_post_request()

    @ex(
        help='Delete Request Command',
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
            (['-ws', '--webservice'],
             {'help': 'specify the type of web service, eg: SOAP, REST(default)',
              'action': 'store',
              'dest': 'webService', }),
        ]
    )
    def delete(self):
        self.app.log.info('Inside delete command!')
        ws = ""
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
        if self.app.pargs.webService:
            self.app.log.info("Received option: webService => %s" % self.app.pargs.webService)
            ws = self.app.pargs.webService

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment,
                               None,
                               None,
                               self.app.pargs.webService)

        context = Context(RequestStrategyBySOAP(), config)
        if ws == "SOAP":
            self.app.log.info("Client: Strategy is set to SOAP web service")
            context.do_delete_request()
        else:
            self.app.log.info("Client: Strategy is set to REST web service")
            context.strategy = RequestStrategyByREST()
            context.do_delete_request()


class CliHTTPClient(App):
    class Meta:
        label = 'myapp'
        handlers = [
            Base,
        ]


with CliHTTPClient() as app:
    defaults = init_defaults('myapp', 'log.logging')
    defaults['log.logging']['file'] = 'my.log'
    app.run()
