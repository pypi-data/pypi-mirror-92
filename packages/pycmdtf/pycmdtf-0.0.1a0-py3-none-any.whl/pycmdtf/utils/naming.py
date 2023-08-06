import re
from pathlib import Path
from typing import Optional, List


class Namespace:
    def __init__(self, parts=None, sep: str = '/'):
        sep = sep or "/"
        self._parts = parts or []
        self._parent = None if not self._parts else Namespace(self._parts[:-1])
        self._str = sep.join(self._parts)
        self._id = parts[-1] if parts else None

    @property
    def id(self) -> str:
        return self._id

    @property
    def safe_id(self) -> str:
        return slugify(self.id)

    @property
    def parts(self) -> List[str]:
        return self._parts

    @property
    def path(self) -> Path:
        return Path(*self.parts)

    @property
    def parent(self) -> Optional['Namespace']:
        return self._parent

    def str(self) -> str:
        return self._str

    def __str__(self) -> str:
        return self.str()

    def new_with_id(self, nid: str) -> 'Namespace':
        return Namespace(self.parts + [nid])


def slugify(text, delim='-', max_len=None):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """
    if not text:
        return ''

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    text = text.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        text = text.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    text = re.sub('\\W', '', text)
    # "some   articles title  "
    # "some articles title "
    text = re.sub('\\s+', ' ', text)

    # "some articles title "
    # "some articles title"
    text = text.strip()

    # "some articles title"
    # "some-articles-title"
    text = text.replace(' ', delim)

    if max_len:
        return text[:max_len]
    return text
