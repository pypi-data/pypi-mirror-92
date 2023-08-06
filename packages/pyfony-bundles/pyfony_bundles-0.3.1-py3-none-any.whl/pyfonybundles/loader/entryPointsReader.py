import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata # pylint: disable = no-name-in-module
else:
    import importlib_metadata # pylint: disable = import-error

def getByKey(key: str):
    return importlib_metadata.entry_points().get(key, ())
