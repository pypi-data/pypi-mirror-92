from injecta.dtype.classLoader import loadClass

def containerInitDefined(rawConfig):
    return 'containerInit' in rawConfig

def resolve(rawConfig, pyprojectSource: str):
    containerInitFunctionSpec = getContainerInit(rawConfig, pyprojectSource)
    return loadClass(*containerInitFunctionSpec)

def getContainerInit(rawConfig: dict, pyprojectSource: str):
    if 'containerInit' not in rawConfig:
        raise Exception(f'containerInit is missing in {pyprojectSource} in pyproject.toml')

    return rawConfig['containerInit'].split(':')
