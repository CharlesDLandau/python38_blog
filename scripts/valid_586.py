from typing import Literal

def valid_586(k: Literal[0, 1, 2, 99]):
    if k < 100:
        return k
    else:
        return float(k)
valid_586(43)