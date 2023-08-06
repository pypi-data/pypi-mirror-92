from dataclasses import dataclass, field
from typing import Iterable
from pathlib import Path

from yamldataclassconfig import YamlDataClassConfig


@dataclass
class CompletionPromptConfig(YamlDataClassConfig):
    start: str = ""
    samples: Iterable[str] = field(
        default=None,
        metadata={'dataclasses_json': {'mm_field': Iterable[str]}})

    def read(self, path: str):
        self.load(Path(path))
        return self