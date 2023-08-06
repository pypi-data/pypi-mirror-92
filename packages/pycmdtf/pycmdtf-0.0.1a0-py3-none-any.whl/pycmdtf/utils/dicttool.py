import json
from enum import Enum
from pathlib import Path
from typing import Dict, Any, Iterable, List, Mapping, MutableMapping, Optional


class AsDict:
    """Mixin, if adds methods, as_dict, as_json, as_yaml
    In order to implement this trait you need to implement method, _ad_dict
    """
    AD_PROPS = None
    AD_EXCLUDED = None

    def _ad_dict(self) -> Optional[Dict]:
        return None

    def as_dict(self) -> MutableMapping:
        return obj_as_dict(self,
                           props=self.AD_PROPS,
                           exclude=self.AD_EXCLUDED,
                           func=_custom_mapper,
                           inner=self._ad_dict())

    def as_json(self, indent=2) -> str:
        return json.dumps(self.as_dict(), indent=indent, default=_json_default_serial)

    def as_yaml(self) -> str:
        import yaml
        return yaml.safe_dump(self.as_dict())

    def __str__(self) -> str:
        return str(self.as_dict())

    def __repr__(self) -> str:
        return self.__str__()


def dict_deepmerge(orig: Dict, other: Dict) -> Dict:
    from deepmerge import always_merger
    return always_merger.merge(orig, other)


def dict_filter(d: Dict, excluded: List = None, included: List = None) -> Dict:
    result = {}
    for key, val in d.items():
        if excluded and key in excluded:
            continue
        if not included or key in included:
            result[key] = val
    return result


def dict_extract(d: Dict, keys: List, with_rest: bool = False) -> List:
    result = [d.get(key) for key in keys]
    if with_rest:
        result.append(dict_filter(d, excluded=keys))
    return result


def obj_as_dict(obj, props: Iterable[str] = None, exclude: List[str] = None, func=None,
                inner=None) -> Dict:
    func = func or _default_mapper
    data = inner or {}
    if inner is None:
        if isinstance(obj, Mapping):
            data = {**obj}

        elif isinstance(obj, object) and not props:
            data = obj.__dict__

    if props:
        data.update({k: getattr(obj, k) for k in props})

    result = {}
    for k, v in data.items():
        if k.startswith("_") or (exclude and k in exclude):
            continue
        result[k] = func(v)
    return result


def _default_mapper(v: Any) -> Any:
    if isinstance(v, Enum):
        return v.value
    return v


def _custom_mapper(v: Any) -> Any:
    if isinstance(v, AsDict):
        return v.as_dict()
    if isinstance(v, Path):
        return str(v)
    if isinstance(v, list):
        return [_custom_mapper(i) for i in v]
    if isinstance(v, set):
        return {_custom_mapper(i) for i in v}
    elif isinstance(v, Enum):
        return v.value

    return v


def _json_default_serial(param: Any) -> Any:
    if isinstance(param, AsDict):
        return param.as_dict()
    if isinstance(param, Enum):
        return param.value
    if isinstance(param, set):
        return list(param)
    return str(param)
