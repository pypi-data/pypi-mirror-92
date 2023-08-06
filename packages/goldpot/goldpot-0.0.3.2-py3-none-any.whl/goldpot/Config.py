from enum import Enum, auto
from typing import Optional, Iterable, Dict

from dataclasses import dataclass


class Engine(Enum):
    ADA = auto()
    BABBAGE = auto()
    CURIE = auto()
    DAVINCI = auto()
    INSTRUCT_CURIE_BETA = auto()
    INSTRUCT_DAVINCI_BETA = auto()

    def __str__(self):
        return self.name.lower().replace('_', '-')


@dataclass
class CompletionConfig:
    max_tokens: int = 10
    temperature: float = 0.7
    top_p: float = 0.0
    n: int = 1
    #stream: bool = False
    logprobs: Optional[int] = None
    echo: bool = False
    stop: Optional[Iterable[str]] = None
    presence_penalty: int = 0
    frequency_penalty: int = 0
    best_of: int = 1
    #logit_bias: Optional[Dict[str, int]] = None



class DefaultConfig:
    engine = Engine.ADA
    max_chars = 7500
    completion_config = CompletionConfig()

