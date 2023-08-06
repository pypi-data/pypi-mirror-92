import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Any, Dict, Tuple, Optional

from goldpot.CompletionPromptConfig import CompletionPromptConfig
from openai.openai_object import OpenAIObject

from goldpot.DefaultConfig import DefaultConfig
from goldpot.Utils import Splitter


@dataclass
class CompletionInput(ABC):
    @abstractmethod
    def get_prompts(self) -> Iterable[Iterable[str]]:
        raise NotImplementedError


@dataclass
class StringCompletionInput(CompletionInput):
    text: str
    max_chars: int = DefaultConfig.max_chars

    def get_prompts(self):
        return [''.join(chunk[0]) for chunk in Splitter.len_chunk_split(list(self.text), self.max_chars)]


@dataclass()
class SamplesCompletionInput(CompletionInput):
    start: str = ''
    end: str = ''
    max_chars: int = DefaultConfig.max_chars
    sep: str = '\n'
    sample_sep: str = '----'
    samples: Iterable[str] = field(default_factory=lambda: [])
    prompt_config: Optional[CompletionPromptConfig] = None

    def __post_init__(self):
        if self.prompt_config is not None:
            self.start = self.prompt_config.start
            self.samples = self.prompt_config.samples

    def get_prompts(self):
        samples = ''.join([self.sep + sample + self.sep + self.sample_sep + self.sep for sample in self.samples])
        begin = (self.start + samples)[:self.max_chars]
        left_chars = self.max_chars - len(begin)
        splits = Splitter.len_chunk_split(re.findall('[\w\W]*?[.!?]|[\w\W]+', self.end), left_chars)
        return [begin + ''.join(s) for split in splits for s in split]


@dataclass
class SearchInput:
    query: str
    docs: [str]
    max_chars: int = DefaultConfig.max_chars

    def get_docs(self):
        left_chars = self.max_chars - len(self.query)
        docs_split = Splitter.len_chunk_split(self.docs, left_chars)
        return [(self.query, d) for docs in docs_split for d in docs]


@dataclass
class CompletionResult:
    prompt: str
    finish_reason: str
    completion: str
    logprobs: Any


@dataclass
class CompletionOutput:
    output: Iterable[OpenAIObject]
    prompts: Iterable[str]
    completion: str = ''
    completions: Iterable[str] = field(default_factory=lambda: [])
    results: Iterable[CompletionResult] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.results = [CompletionResult(oo[1], c.finish_reason, c.text, c.logprobs) for oo in
                        zip(self.output, self.prompts) for c in oo[0].choices]
        self.completions = [r.completion for r in self.results]
        self.completion = '\n'.join(self.completions)

    # TODO: numpy vectorized version
    def extract(self, regex: str):
        ex = lambda s: re.search(regex, s, re.IGNORECASE)
        return list(map(ex, self.completions))

    def extract1(self, regex: str) -> str:
        ex = lambda match: match.group(1).strip() if match is not None and match.group(1) is not None else ""
        return list(map(ex, self.extract(regex)))


@dataclass
class SearchOutput:
    output: Iterable[OpenAIObject]
    docs: Iterable
    scores: Dict[str, float] = field(default_factory=lambda: {})
    scores_sorted: Iterable[Tuple[str, float]] = field(default_factory=lambda: [])

    def __post_init__(self):
        clip = lambda f: max(min(300.0, f), 0.0) / 300.0
        r = [(o.score, clip(o.score)) for oo in self.output for o in oo.data]
        self.scores = dict(zip(self.docs, r))
        self.scores_sorted = sorted(self.scores.items(), key=lambda i: i[1][1], reverse=True)