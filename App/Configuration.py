class Configuration:

    def __init__(self, systemName, interfaceName, versionNumber, useCase, environment, loadRequestFileFrom, exportLogsTo):
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

    def get_config(self):
        return self

    def __str__(self):
        return "System Name: {0}" \
               "Interface Name: {1}" \
               "Version Number: {2}" \
               "useCase: {3}" \
               "environment: {4}"\
            .format(self.systemName,
                    self.interfaceName,
                    self.versionNumber,
                    self.useCase,
                    self.environment)