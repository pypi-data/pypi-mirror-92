import functools
import logging
from pathlib import Path
from typing import Callable, Dict, Any, List, Tuple

from pycmdtf import defs
from pycmdtf.actions.checks import ActionChecks
from pycmdtf.config import Config

ActionCallable = Callable[['TestContext', 'Dict[str, Any]'], Any]
ValidatorCallable = Callable[['TestContext', 'Dict[str, Any]', 'Any'], Any]


class TestContext:
    def __init__(self, cfg: Config, test: defs.TestDef, log: logging.Logger):
        self.cfg = cfg
        self.test = test
        self.log = log

        self._checks = ActionChecks(self.log)

    @property
    def checks(self) -> 'ActionChecks':
        return self._checks

    @property
    def outputs(self) -> Path:
        pth = self.cfg.paths.artifacts / 'out' / self.test.namespace.path
        if not pth.exists():
            pth.mkdir(parents=True)
        return pth

    def cwd(self) -> Path:
        return self.cfg.paths.workdir


class GeneralEntRegister:
    _INSTANCE: 'GeneralEntRegister' = None

    @classmethod
    def instance(cls) -> 'GeneralEntRegister':
        if cls._INSTANCE is None:
            cls._INSTANCE = cls()
        return cls._INSTANCE

    def __init__(self):
        self.ents = {}

    def add(self, name: str, func: Callable) -> 'GeneralEntRegister':
        self.ents[name] = func
        return self

    def get(self, name: str) -> Callable:
        return self.ents.get(name)


class ActionRegister(GeneralEntRegister):
    pass


class ValidatorsRegister(GeneralEntRegister):
    pass


#######
# Decorators
#######


def action(name: str):
    def _inner_params(func: Callable):
        ActionRegister.instance().add(name, func)

        @functools.wraps(func)
        def _inner(ctx: 'TestContext', params: Dict[str, Any]):
            ctx.log.info(f"[VALIDATE] Validating test {ctx.test.name} "
                         f"by \"{name}\" validator: {params}")
            res = func(ctx, params)
            ctx.log.debug(f"[VALIDATE] Result: {res}")
            return res

        return _inner

    return _inner_params


def validator(name: str):
    def _inner_params(func: Callable):
        ValidatorsRegister.instance().add(name, func)

        @functools.wraps(func)
        def _inner(ctx: 'TestContext', params: Dict[str, Any], action_result: Any):
            ctx.log.info(f"[VALIDATE] Validating test {ctx.test.name} "
                         f"by \"{name}\" validator: {action_result}")
            res = func(ctx, params, action_result)
            ctx.log.debug(f"[VALIDATE] Result: {res}")
            return res

        return _inner

    return _inner_params
