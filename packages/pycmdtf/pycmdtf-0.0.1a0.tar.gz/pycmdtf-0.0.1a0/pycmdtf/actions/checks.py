import logging
from pathlib import Path
from typing import Optional, List, Any, Dict

from pycmdtf.utils.result import GeneralResult, ResultKind


class ActionChecks:
    def __init__(self, log: logging.Logger):
        self._log = log
        self.checks: List[CheckResult] = []
        self._failed = False

    def check(self, name: str, cond: bool, **kwargs) -> 'CheckResult':
        kind = ResultKind.PASS if cond else ResultKind.FAIL
        result = CheckResult(kind, name=name, **kwargs)
        self.add(result)
        return result

    def add(self, check: 'CheckResult') -> 'ActionChecks':
        _log = self._log.debug if check.is_ok() else self._log.warning
        _log(f"[CHECK] adding check[{check.kind}]: {check}")
        self.checks.append(check)
        if not self._failed and check.is_nok():
            _log(f"[CHECK] Failing checks [{check.kind.value}]: {check}")
            self._failed = True
        return self

    def is_fail(self) -> bool:
        return self._failed

    def is_pass(self) -> bool:
        return not self._failed

    def fail_msg(self, with_content: bool = False) -> str:
        res = "Checks:\n"
        for ch in self.checks:
            if ch.is_nok():
                res += f"{ch.fail_msg(with_content)}\n"
        return res


class CheckResult(GeneralResult):
    def __init__(self, kind: 'ResultKind', name: str,
                 provided: Any, expected: Any, msg: Optional[str] = None,
                 detail: Dict = None, diff: str = None):
        super().__init__(kind, msg)
        self.name: str = name
        self.provided = provided
        self.expected = expected
        self.detail = detail
        self.diff = diff

    def fail_msg(self, with_content: bool = False) -> Optional[str]:
        res = f"\nResult: {self.kind.value}\nProvided: {self.provided}\nExpected: {self.expected}"
        if self.diff:
            res += f'\nDiff: {self.diff}\n'
            if with_content:
                res += f"\nDiff Content: \n{Path(self.diff).read_text()}\n"
        return res

    def __str__(self) -> str:
        s = f"[{self.kind.value}] {self.name}"
        if self.is_fail:
            s += f" {self.message or ''} provided:{self.provided}; expected:{self.expected}"
        if self.diff:
            s += f" diff:{self.diff}"
        return s

    def _ad_dict(self) -> Optional[Dict]:
        x = super(CheckResult, self)._ad_dict()
        x['check_name'] = self.name
        x['provided'] = self.provided
        x['expected'] = self.expected
        if self.detail:
            x['detail'] = self.detail
        if self.diff:
            x['diff'] = self.diff
        return x
