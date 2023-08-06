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
#    resource_package = __name__
#    resource_path = '/'.join(('conf', 'sample_engines_config.yml'))  # Do not use os.path.join()
#    conf = pkg_resources.resource_filename(resource_package, resource_path)

    completion_engine_config: CompletionEngineConfig = CompletionEngineConfig(engine=Engines.ADA, max_tokens=256, temperature=0.0, top_p=0.0, n=1, stream=False,
                                                                              logprobs=None, echo=False, stop=['####'], presence_penalty=0.0, frequency_penalty=0.0, best_of=1)
#    CompletionEnginesConfigReader().read("conf/engines.yml").get("TST")
    search_engine_config = Engines.ADA
    max_chars: int = 7500
