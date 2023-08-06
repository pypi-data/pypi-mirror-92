import os
import glob
import functools
from .global_vars import CACHE
from .io import dump, load


def hash_partial(p):
    """
    Partial's built in __hash__ won't give us the desired behavior
    """

    if not isinstance(p, functools.partial):
        raise RuntimeError("Must be of type functools.partial")

    h = hash(p.func.__name__)
    for k in sorted(p.keywords.keys()):
        h += k.__hash__() + p.keywords[k].__hash__()
    for a in p.args:
        h += a.__hash()
    return h


def cache_exec(f):
    """
    Example: from functools import partial; cache_exec(partial(f, a="A", b="B"))
    WARNING: Functions with same names will get the same cache values!
    """

    cache_exec_dir = os.path.join(CACHE, "cache_exec")
    if not os.path.isdir(cache_exec_dir):
        os.makedirs(cache_exec_dir, exist_ok=True)

    file_name = os.path.join(cache_exec_dir, str(hash_partial(f)) + ".pkl")
    files = glob.glob(os.path.join(cache_exec_dir, "*"))

    print(file_name)
    print(files)

    if file_name not in files:
        dump(f(), file_name)

    return load(file_name)
