import importlib
import pkgutil
import sys
from functools import reduce, wraps
from pathlib import Path
from typing import Any, List


def import_all(name):
    for _, module_name, _ in pkgutil.walk_packages(sys.modules[name].__path__):
        importlib.import_module(f"{name}.{module_name}")


def requires_all_imports(import_all):
    def wrapper(fn):
        all_imported = False

        @wraps(fn)
        def wrapped(*args, **kwargs):
            nonlocal all_imported

            if not all_imported:
                import_all()
                all_imported = True

            return fn(*args, **kwargs)

        return wrapped

    return wrapper


def wrap(val):
    if isinstance(val, (list, tuple)):
        return val
    else:
        return (val,)


def flow(fns: List, val: Any):
    return reduce(lambda f, x: x(f), fns, val)
