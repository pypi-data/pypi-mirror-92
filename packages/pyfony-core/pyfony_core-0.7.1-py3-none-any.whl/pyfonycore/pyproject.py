import os
from pathlib import Path
import tomlkit
from tomlkit.toml_document import TOMLDocument

def read(pyprojectPath: Path) -> TOMLDocument:
    with pyprojectPath.open('r', encoding='utf-8') as t:
        return tomlkit.parse(t.read())

def getPath(workingDir=os.getcwd()):
    return Path(workingDir).joinpath('pyproject.toml')
