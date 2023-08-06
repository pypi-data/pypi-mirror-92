import string
from typing import Any, Dict

from .naming import Namespace, slugify
from .logger import LOG
from .dicttool import AsDict, dict_extract, dict_deepmerge, dict_filter
from .cmd import execute_cmd, CommandResult
from .tags import TagsEvaluator


def to_bool(param: Any) -> bool:
    if param is None:
        return False
    if isinstance(param, bool):
        return param
    if isinstance(param, str):
        return param and (param[0].lower() in ['1', 't', 'y'] or param == 'on')
    if isinstance(param, int):
        return param != 0
    return bool(param)


def expand_template(val: Any, params: Dict[str, Any]) -> Any:
    if isinstance(val, str):
        return string.Template(val).safe_substitute(params)
    if isinstance(val, dict):
        return {k: expand_template(v, params) for k, v in val.items()}
    if isinstance(val, list) or isinstance(val, set):
        return [expand_template(item, params) for item in val]
    return val
