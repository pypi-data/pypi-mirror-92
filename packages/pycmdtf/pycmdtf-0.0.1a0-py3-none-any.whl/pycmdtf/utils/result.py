from enum import Enum
from typing import MutableMapping, Optional, Dict, TypeVar

from pycmdtf.utils import AsDict


class ResultKind(Enum):
    PASS = 'pass'
    FAIL = 'fail'
    SKIP = 'skip'
    ERROR = 'error'

    def is_pass(self) -> bool:
        return self == self.PASS

    def is_fail(self) -> bool:
        return self == self.FAIL

    def is_error(self) -> bool:
        return self == self.ERROR

    def is_skip(self) -> bool:
        return self == self.SKIP

    def is_ok(self) -> bool:
        return self.is_skip() or self.is_pass()

    def is_nok(self) -> bool:
        return not self.is_ok()


_GeneralResult = TypeVar('_GeneralResult', bound='GeneralResult')


class GeneralResult(AsDict):
    def __init__(self, kind: 'ResultKind', msg: Optional[str]):
        self.kind = kind
        self.message: Optional[str] = msg

    def is_ok(self) -> bool:
        return self.kind.is_ok()

    def is_nok(self) -> bool:
        return self.kind.is_nok()

    def is_pass(self) -> bool:
        return self.kind.is_pass()

    def is_fail(self) -> bool:
        return self.kind.is_fail()

    def is_skip(self) -> bool:
        return self.kind.is_skip()

    def is_error(self) -> bool:
        return self.kind.is_error()

    def set(self, kind: ResultKind, msg: str) -> '_GeneralResult':
        self.message = msg
        self.kind = kind
        return self

    def set_fail(self, msg: str) -> '_GeneralResult':
        return self.set(ResultKind.FAIL, msg)

    def set_pass(self, msg: str) -> '_GeneralResult':
        return self.set(ResultKind.PASS, msg)

    def set_skip(self, msg: str) -> '_GeneralResult':
        return self.set(ResultKind.SKIP, msg)

    def set_err(self, msg: str) -> '_GeneralResult':
        return self.set(ResultKind.ERROR, msg)

    def _ad_dict(self) -> Optional[Dict]:
        result = {'kind': self.kind.value}
        if self.message:
            result['message'] = self.message
        return result
