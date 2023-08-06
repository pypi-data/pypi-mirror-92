from pyfonycore.bootstrap.config import configReader

def init(appEnv: str):
    bootstrapConfig = configReader.read()
    return bootstrapConfig.containerInitFunction(appEnv, bootstrapConfig)
