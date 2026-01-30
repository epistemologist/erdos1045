from __future__ import annotations
from mpmath import iv, mpf
from itertools import product, pairwise
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm

iv.dps = 15; mpf.dps = 15
iv.pretty = True

# Monkey patch some utility functions to mpmath interval
# TODO: replace mpmath with arb for speedup?
iv.mpf.left = lambda self: mpf(self.a)
iv.mpf.right = lambda self: mpf(self.b)
iv.mpf.size = lambda self: self.right() - self.left()

def split_interval(I: iv.mpf) -> List[iv.mpf]:
    # Split interval into two equally divided intervals
    return (
        iv.mpf( [I.a, (I.a + I.b)/2] ),
        iv.mpf( [(I.a + I.b)/2, I.b] )
    ) if I.size() > 0 else [I]

iv.mpf.split = lambda self: split_interval(self)
Interval = iv.mpf

