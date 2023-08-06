from pyfonycore.bootstrap.config.Config import Config
from pyfonycore.bootstrap.config.raw import containerInitResolver, rootModuleNameResolver, allowedEnvironmentsResolver, kernelClassResolver

def create(rawConfig, pyprojectSource: str):
    if containerInitResolver.containerInitDefined(rawConfig):
        initContainer = containerInitResolver.resolve(rawConfig, pyprojectSource)
    else:
        from pyfonycore.container.containerInit import init as initContainer # pylint: disable = import-outside-toplevel

    return Config(
        initContainer,
        kernelClassResolver.resolve(rawConfig),
        rootModuleNameResolver.resolve(rawConfig, pyprojectSource),
        allowedEnvironmentsResolver.resolve(rawConfig)
    )
