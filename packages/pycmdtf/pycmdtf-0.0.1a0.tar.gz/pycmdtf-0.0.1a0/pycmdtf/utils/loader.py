import importlib
import importlib.machinery
import importlib.util
from pathlib import Path
from typing import List

from pycmdtf.utils import LOG


def import_module_file(module_name: str, path: Path):
    """Imports and loads the scenario `instructions.py`F module in the kontr_tests dir
    Args:
        module_name(str): Name of the module,
        path:(Path): Location of the module
    Returns: Scenario definition module instance

    """
    full_path = str(path)
    loader = importlib.machinery.SourceFileLoader(module_name, full_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    LOG.info(f"[CLI] Loading module: {mod}")
    return mod


def import_module(path: Path) -> List:
    if not path.is_dir():
        return [import_module_file(path.stem, path)]
    result = []
    for fp in path.glob("*.py"):
        if fp.stem.startswith(".") or fp.stem.startswith("_"):
            continue
        result.append(import_module_file(fp.stem, fp))
    return result
