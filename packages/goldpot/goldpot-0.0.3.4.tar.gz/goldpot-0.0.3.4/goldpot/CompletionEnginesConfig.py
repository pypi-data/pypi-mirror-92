from dataclasses import dataclass, field
from functools import reduce
from typing import Iterable, List, Optional, Dict
from pathlib import Path

from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig import YamlDataClassConfig


@dataclass
class CompletionEngineConfig(DataClassJsonMixin):
    engine: str
    max_tokens: int
    temperature: float
    top_p: float
    n: int
    stream: bool
    logprobs: Optional[int]
    echo: bool
    stop: Optional[List[str]]
    presence_penalty: float
    frequency_penalty: float
    best_of: int
    #logit_bias: Optional[Dict[str, int]]

    def __post_init__(self):
        if not isinstance(self.engine, str):
            self.engine = str(self.engine)


@dataclass
class CompletionEnginesConfigReader(YamlDataClassConfig):
    configs: List[Dict[str, CompletionEngineConfig]] = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': List[Dict[str, CompletionEngineConfig]]}})

    def read(self, path: str):
        self.load(Path(path))
        self.configs = reduce(lambda d1, d2: {**d1, **d2}, self.configs) # TODO: curerntly using Python 3.8, >=3.9 has d1|d2
        return self

    def get(self, handle: str):
        return self.configs.get(handle, None)

