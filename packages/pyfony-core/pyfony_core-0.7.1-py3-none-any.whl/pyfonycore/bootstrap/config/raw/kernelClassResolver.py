from injecta.dtype.classLoader import loadClass
from pyfonycore.Kernel import Kernel

def resolve(rawConfig):
    return loadClass(*rawConfig['kernelClass'].split(':')) if 'kernelClass' in rawConfig else Kernel
