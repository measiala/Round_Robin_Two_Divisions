"""
Misc functions needed by main programs
"""

def zmod(_a: int, _m: int):
    """Accepts an integer 'a' and returns the value mod 'm' with values (0,m-1)"""
    return _a % _m

def mod(_a: int, _m: int):
    """Accepts an integer 'a' and returns the value mod 'm' with values (1,m)"""
    return zmod(_a - 1, _m) + 1

def fact(_n: int, _k = 1):
    if _n in [0, 1] or _n == _k:
        return 1
    else:
        return _n * fact(_n - 1, _k)

def comb(_n: int, _k: int):
    if _n == _k:
        return 1
    elif _k > (_n - _k):
        return fact(_n, _k) / fact(_n - _k)
    else:
        return fact(_n, _n - _k) / fact(_k)