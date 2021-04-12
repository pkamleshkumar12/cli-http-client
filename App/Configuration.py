class Configuration:

    def __init__(self, systemName, interfaceName, versionNumber, useCase, environment):
        """

            :type systemName: str
            """
        self.systemName = systemName
        self.interfaceName = interfaceName
        self.versionNumber = versionNumber
        self.useCase = useCase
        self.environment = environment

    def get_config(self):
        return self
