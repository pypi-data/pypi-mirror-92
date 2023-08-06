from typing import List
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.pathResolver import resolvePath
from pyfonybundles.Bundle import Bundle
from pyfonybundles.loader import pyfonyBundlesLoader
from pyfonycore.bootstrap.config.Config import Config

def init(appEnv: str, bootstrapConfig: Config) -> ContainerInterface:
    bundles = pyfonyBundlesLoader.loadBundles()
    kernel = createKernel(appEnv, bootstrapConfig, bundles)

    return kernel.initContainer()

def initWithCurrentBundle(appEnv: str, bootstrapConfig: Config) -> ContainerInterface:
    bundles = pyfonyBundlesLoader.loadBundlesWithCurrent()
    kernel = createKernel(appEnv, bootstrapConfig, bundles)

    return kernel.initContainer()

def createKernel(appEnv: str, bootstrapConfig: Config, bundles: List[Bundle]):
    kernel = bootstrapConfig.kernelClass(
        appEnv,
        resolvePath(bootstrapConfig.rootModuleName) + '/_config',
        YamlConfigReader(),
        bundles,
    )
    kernel.setAllowedEnvironments(bootstrapConfig.allowedEnvironments)

    return kernel
