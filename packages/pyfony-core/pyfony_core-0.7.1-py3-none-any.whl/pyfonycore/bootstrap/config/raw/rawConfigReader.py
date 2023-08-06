from pathlib import Path
from pyfonycore import pyproject

def isDefined(rawConfig):
    return 'pyfony' in rawConfig and 'bootstrap' in rawConfig['pyfony']

def read(pyprojectPath: Path):
    config = pyproject.read(pyprojectPath)
    return getBoostrapConfig(config)

def getBoostrapConfig(rawConfig):
    if 'pyfony' not in rawConfig:
        raise Exception('[pyfony] section is missing in pyproject.toml')

    if 'bootstrap' not in rawConfig['pyfony']:
        raise Exception('[pyfony.bootstrap] section is missing in pyproject.toml')

    return rawConfig['pyfony']['bootstrap']
