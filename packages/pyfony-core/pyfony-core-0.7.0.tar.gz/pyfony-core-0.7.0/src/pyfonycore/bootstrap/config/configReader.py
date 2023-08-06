from pyfonycore import pyproject
from pyfonycore.bootstrap.config import configFactory
from pyfonycore.bootstrap.config.Config import Config
from pyfonycore.bootstrap.config.raw import rawConfigReader

def read() -> Config:
    rawConfig = rawConfigReader.read(pyproject.getPath())
    return configFactory.create(rawConfig, '[pyfony.bootstrap]')
