from cement.core.controller import CementBaseController, expose

from App.services.RequestService import RequestService
from App.Configuration import Configuration


class MainController(CementBaseController):
    class Meta:
        label = 'base'
        description = "My Application does amazing things!"
        arguments = [
            (['-sn', '--systemName'],
             dict(action='store', help='System Name')),
            (['-in', '--interfaceName'],
             dict(action='store', help='Interface Name')),
            (['-vn', '--versionNumber'],
             dict(action='store', help='Version Name')),
            (['-uc', '--useCase'],
             dict(action='store', help='Use Case')),
            (['-env', '--environment'],
             dict(action='store', help='Environment'))
        ]

    @expose(hide=True)
    def default(self):
        self.app.log.info('Inside MainController.default()')
        if self.app.pargs.systemName:
            print("Received option: systemName => %s" % self.app.pargs.systemName)

    @expose(aliases=['rget', 'GET'], help="GET Method")
    def get(self):
        self.app.log.info("GET Request..")
        if self.app.pargs.systemName:
            print("Received option: systemName => %s" % self.app.pargs.systemName)
        if self.app.pargs.interfaceName:
            print("Received option: interfaceName => %s" % self.app.pargs.interfaceName)
        if self.app.pargs.versionNumber:
            print("Received option: versionNumber => %s" % self.app.pargs.versionNumber)
        if self.app.pargs.useCase:
            print("Received option: useCase => %s" % self.app.pargs.useCase)
        if self.app.pargs.environment:
            print("Received option: environment => %s" % self.app.pargs.environment)

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment)

        r = RequestService(config)
        r.get_request()

    @expose(aliases=['rpost', 'POST'], help="POST Method")
    def post(self):
        self.app.log.info("POST Request...")
        if self.app.pargs.systemName:
            print("Received option: systemName => %s" % self.app.pargs.systemName)
        if self.app.pargs.interfaceName:
            print("Received option: interfaceName => %s" % self.app.pargs.interfaceName)
        if self.app.pargs.versionNumber:
            print("Received option: versionNumber => %s" % self.app.pargs.versionNumber)
        if self.app.pargs.useCase:
            print("Received option: useCase => %s" % self.app.pargs.useCase)
        if self.app.pargs.environment:
            print("Received option: environment => %s" % self.app.pargs.environment)

        config = Configuration(self.app.pargs.systemName,
                               self.app.pargs.interfaceName,
                               self.app.pargs.versionNumber,
                               self.app.pargs.useCase,
                               self.app.pargs.environment)

        r = RequestService(config)
        r.post_request()

        @expose(aliases=['configbysystem'], help="Retrieve all the config by system")
        def config_by_systems():
            pass
