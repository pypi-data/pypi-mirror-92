from pyfonycore.bootstrap.config.raw import containerInitResolver

def resolve(rawConfig, pyprojectSource: str):
    if 'rootModuleName' in rawConfig:
        return rawConfig['rootModuleName']

    containerInitSpec = containerInitResolver.getContainerInit(rawConfig, pyprojectSource)

    return _resolveRootModuleName(containerInitSpec[0])

def _resolveRootModuleName(moduleName):
    return moduleName[0:moduleName.find('.')]
