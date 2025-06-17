from injector import inject, provider, singleton, Module
from config import ConfigurationSet
from .config import load_config

class ConfigModule(Module):

    @singleton
    @provider
    def provide_config(self) -> ConfigurationSet:
        return load_config()
