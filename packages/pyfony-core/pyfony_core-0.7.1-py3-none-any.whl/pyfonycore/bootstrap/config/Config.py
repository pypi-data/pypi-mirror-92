class Config:

    def __init__(
        self,
        containerInitFunction: callable,
        kernelClass: type,
        rootModuleName: str,
        allowedEnvironments: list,
    ):
        self.__containerInitFunction = containerInitFunction
        self.__kernelClass = kernelClass
        self.__rootModuleName = rootModuleName
        self.__allowedEnvironments = allowedEnvironments

    @property
    def containerInitFunction(self):
        return self.__containerInitFunction

    @property
    def kernelClass(self):
        return self.__kernelClass

    @property
    def rootModuleName(self):
        return self.__rootModuleName

    @property
    def allowedEnvironments(self):
        return self.__allowedEnvironments
