from typing import Set, Iterable

from pycmdtf.utils.logger import LOG


class TagsEvaluator:
    def __init__(self, expression: str, registered_tags=None):
        self.expression = expression
        self.registered_tags: Set[str] = set(registered_tags or [])
        self.log = LOG

    def evaluate(self, tags: Iterable['str']):
        expr = self.expression
        if not expr:
            return True
        params = {tag: (tag in tags) for tag in self.registered_tags}
        self.log.debug(f"[TAGS] Eval: \"{expr}\": {tags}")
        try:
            return eval(expr, {'__builtins__': None}, params)
        except Exception as ex:
            self.log.warning(f"There is some error: {ex}")
            return False
