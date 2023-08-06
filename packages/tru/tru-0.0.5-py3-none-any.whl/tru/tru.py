import importlib
from .io import dump, load


def reload(package):
    importlib.reload(package)
