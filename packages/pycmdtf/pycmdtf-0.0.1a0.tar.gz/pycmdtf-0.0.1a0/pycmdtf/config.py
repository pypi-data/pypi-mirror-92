import tempfile
from pathlib import Path
from typing import Dict, Optional, Union, Any

from pycmdtf.utils import AsDict

PROJECT_ROOT = Path(__file__).parent.parent


class Config(AsDict):
    """Configuration
    Paths:
    - workdir - Working directory, all other paths used in definitions should be relative
    to this directory
    - artifacts - where to store the artifacts
    - tags - tags expression, specify which tags should executed by logical expression
        Example: "sanity and smoke", or "compilation and smoke"
    """

    def __init__(self, workdir: Path, artifacts: Union[str, Path] = None,
                 tags: Optional[str] = None):
        self.paths = ConfigPaths(workdir=workdir, artifacts=artifacts)
        self.tags_expr = tags
        self.template_vars: Dict[str, Any] = {}
        self.defaults = {}

    def _ad_dict(self) -> Optional[Dict]:
        return {
            'paths': self.paths.as_dict(),
            'target': self.tags_expr,
            'template_vars': self.template_vars,
        }

    def cwd(self) -> Path:
        return self.paths.workdir


class ConfigPaths(AsDict):
    def __init__(self, workdir: Path, artifacts: Path):
        self._wd = Path(workdir) if workdir else Path.cwd()
        self._artifacts = Path(artifacts) if artifacts else None

    @property
    def workdir(self) -> Path:
        return self._wd

    @property
    def artifacts(self) -> Path:
        if self._artifacts is None:
            self._artifacts = Path(tempfile.mkdtemp(prefix="pycmdtf-artifacts-"))
        return self._artifacts
