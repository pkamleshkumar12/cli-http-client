from cement.core.controller import CementBaseController, expose

from App.Helper.RequestHelper import RequestHelper


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
             dict(action='store', help='Use Case'))
        ]

    @expose(hide=True)
    def default(self):
        self.app.log.info('Inside MyBaseController.default()')
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

        r = RequestHelper(self.app.pargs.systemName,
                          self.app.pargs.interfaceName,
                          self.app.pargs.versionNumber,
                          self.app.pargs.useCase)
        r.getRequest()

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

        r = RequestHelper(self.app.pargs.systemName,
                          self.app.pargs.interfaceName,
                          self.app.pargs.versionNumber,
                          self.app.pargs.useCase)
        r.postRequest()