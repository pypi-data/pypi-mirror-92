from enum import Enum, auto

from dataclasses import dataclass

import pkg_resources

from goldpot.CompletionEnginesConfig import CompletionEnginesConfigReader, CompletionEngineConfig

class Engines(Enum):
    ADA = auto()
    BABBAGE = auto()
    CURIE = auto()
    DAVINCI = auto()
    CURIE_INSTRUCT = auto()
    DAVINCI_INSTRUCT_BETA = auto()

    def __str__(self):
        return self.name.lower().replace('_', '-')

class DefaultConfig:
    resource_package = __name__
    resource_path = '/'.join(('../conf', 'sample_engines_config.yml'))  # Do not use os.path.join()
    conf = pkg_resources.resource_filename(resource_package, resource_path)

    completion_engine_config: CompletionEngineConfig = CompletionEnginesConfigReader().read(conf).get("TST")
    search_engine_config = Engines.ADA
    max_chars: int = 7500
