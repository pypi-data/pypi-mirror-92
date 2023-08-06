import itertools
import sys
from itertools import takewhile, accumulate
from typing import Iterable


class Splitter:
    # TODO: more general (2d) knapsack opt approach
    # TODO: tail rec for current implementation

    @staticmethod
    def len_chunk_split(items: Iterable[str], max_len: int = sys.maxsize, max_chunks: int = sys.maxsize) -> Iterable[str]:

        def chunks(iterable, n):
            for i in range(0, len(iterable), n):
                yield iterable[i:i+n]

        def rec(items, res: Iterable[str] = [], pending=True):
            if len(items) == 0 or not pending:
                return res
            else:
                split_n = len(list(takewhile(lambda cum_len: not cum_len > max_len, accumulate([len(s) for s in items]))))
                return rec(items[split_n:], res + [items[:split_n]], split_n > 0)

        return [list(chunks(split, max_chunks)) for split in rec(items) if len(split) > 0]
