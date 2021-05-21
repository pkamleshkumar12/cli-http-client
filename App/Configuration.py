class Configuration:

    def __init__(self, systemName, interfaceName, versionNumber,
                 useCase, environment, loadRequestFileFrom,
                 exportLogsTo, webService):
        """

            :type systemName: str
            :type interfaceName: str
            """
        self.systemName = systemName
        self.interfaceName = interfaceName
        self.versionNumber = versionNumber
        self.useCase = useCase
        self.environment = environment
        self.loadRequestFileFrom = loadRequestFileFrom
        self.exportLogsTo = exportLogsTo
        self.webService = webService

    def get_config(self):
        return self

    def __str__(self):
        return "System Name: {0}" \
               " Interface Name: {1}" \
               " Version Number: {2}" \
               " UseCase: {3}" \
               " Environment: {4}"\
            .format(self.systemName,
                    self.interfaceName,
                    self.versionNumber,
                    self.useCase,
                    self.environment)