import glob
import json
import os
import re
import shutil
from pathlib import Path
from typing import Optional, Dict, List

from pycmdtf.utils.logger import LOG


def try_exist_file(root: Path, name: str, exts=None) -> Optional[Path]:
    exts = exts or ('yml', 'yaml', 'json')
    for ext in exts:
        pth = root / f"{name}.{ext}"
        LOG.debug(f"[FIND] Trying to find file {name} in {root} for \'{ext}\': {pth}")
        if pth.exists():
            LOG.debug(f"[PATH] Path: {name}: {pth}")
            return pth
    LOG.warning(f"No file with avaliable extensions({exts}) was found in: {root} ")
    return None


def load_dict_from_file(root: Path, name: str, exts=None) -> Optional[Dict]:
    pth = try_exist_file(root, name=name, exts=exts)
    if pth is None:
        return None

    return load_config_file(pth)


def load_config_file(pth: 'Path') -> Optional[Dict]:
    if not pth:
        return None
    ext = pth.suffix
    if ext in ['.yml', '.yaml']:
        import yaml
        return yaml.safe_load(pth.open())
    if ext in ['.json']:
        return json.load(pth.open())
    return None


def find_all_files(filename: str, root: Path = None, find_mode: str = 'normal') -> List[Path]:
    result = []
    root = Path(root) if root else None
    find_mode = (find_mode or 'normal').lower()

    merged = Path(filename) if not root else root / filename

    if find_mode == 'normal':
        result.append(merged)

    if find_mode == 'glob':
        for glb in glob.glob(str(merged)):
            result.append(glb)

    if find_mode in ['re', 'regex']:
        pat = re.compile(filename)
        for item in os.listdir(root):
            if pat.match(filename):
                result.append(root / item)

    return result


def copy_all_files(filename: str, target: Path, source: Path = None,
                   find_mode: str = 'normal') -> List[Path]:
    files = find_all_files(filename, root=source, find_mode=find_mode)
    result = []
    for file in files:
        copied = Path(shutil.copy2(str(file), str(target)))
        result.append(copied)
    return result


def endure_dir(pth: Path, clean: bool = False) -> Path:
    if pth.exists():
        if not clean:
            return pth
        shutil.rmtree(pth)
    pth.mkdir(parents=True)
