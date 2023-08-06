import uuid
from copy import deepcopy
from typing import Optional, Any, Dict, List, TypeVar, Set, Iterable

from pycmdtf import utils
from pycmdtf.utils import Namespace, AsDict

GeneralDefinition = TypeVar('GeneralDefinition', bound='_Definition')


class _Definition(AsDict):
    """Shared base for all definitions, all other defs. are extending it
    """

    def __init__(self, name: str, desc: Optional[str] = None,
                 tags: Optional[Iterable[str]] = None, parent: '_Definition' = None):
        """Name of the entity, should be snake case
        :param name: str
        :param desc: str Description of the entity
        :param tags: Iterable[str] provided tags
        :param parent: Parent entity
        """
        self._name: str = name
        self._id: str = utils.slugify(name or desc or str(uuid.uuid4()))
        self.desc: Optional[str] = desc or name
        self.tags = set(tags or [])
        self._parent: Optional[GeneralDefinition] = parent
        self._namespace = None

    @property
    def parent(self) -> 'GeneralDefinition':
        return self._parent

    @property
    def namespace(self) -> 'Namespace':
        if self._namespace is None:
            if self._parent is None:
                self._namespace = Namespace([self.id])
            else:
                self._namespace = self._parent.namespace.new_with_id(self.id)
        return self._namespace

    @parent.setter
    def parent(self, val: 'GeneralDefinition'):
        self._parent = val
        self._namespace = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @name.setter
    def name(self, val: str):
        self._name = val
        self._namespace = None
        self._id = utils.slugify(val)

    def info(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'namespace': self.namespace.str(),
            'propagated_tags': self.propagated_tags,
        }

    def _parent_tags(self) -> Set[str]:
        parent = self._parent.tags.copy() if self.parent else set()
        return _update_tags(parent, self.tags)

    def _children_tags(self) -> Set[str]:
        return set()

    @property
    def propagated_tags(self) -> Set[str]:
        tags = set()
        tags.update(self._parent_tags())
        tags.update(self._children_tags())
        return tags


class SuiteDef(_Definition):
    def __init__(self, name: str, desc: str, tags: Iterable[str] = None,
                 defaults: Dict[str, Any] = None):
        """Create new Suite definition
        :param name: Suite name, must follow pattern: ([\\w_\\d]+)
            examples: [hw01, test_suite]
        :param desc: Description of the suite
        :param defaults: Default parameters,
            that will be provided to the action or validator
        """
        super().__init__(name, desc)
        self.tags = set(tags or [])
        self.defaults: Dict[str, Any] = defaults or {}
        self.scenarios: List[ScenarioDef] = []

    def _children_tags(self) -> Set[str]:
        tags = set()
        for sc in self.scenarios:
            tags.update(sc.propagated_tags)
        return tags

    def add_scenario(self, scenario: 'ScenarioDef') -> 'SuiteDef':
        scenario.parent = self
        self.scenarios.append(scenario)
        return self

    def merge_defaults(self) -> Dict[str, Any]:
        return deepcopy(self.defaults)


class ScenarioDef(_Definition):
    AD_EXCLUDED = ['suite']

    def __init__(self, name: str, desc: str, tags: List['str'], parent: 'SuiteDef' = None,
                 defaults: Dict[str, Any] = None, depends_on: List[str] = None):
        """Create new Scenario definition
        :param parent: Parent suite
        :param name: Scenario name, must follow pattern: ([\\w_\\d]+)
            examples: [smoke_test, test_scenario1]
        :param desc: Description of the Scenario
        :param defaults: Default parameters,
            that will be provided to the action or validator
        """
        super().__init__(name, desc, parent=parent)
        self.defaults: Dict[str, Any] = defaults or {}
        self.depends_on: List[Dict] = depends_on or []
        self.tags: Set[str] = set(tags or [])
        # Subscenarios
        self.scenarios: List['ScenarioDef'] = []
        # Tests
        self.tests: List['TestDef'] = []
        self.before: List['TestDef'] = []
        self.after: List['TestDef'] = []

    @property
    def suite(self) -> Optional['SuiteDef']:
        if isinstance(self._parent, SuiteDef):
            return self._parent
        if isinstance(self._parent, ScenarioDef):
            return self._parent.suite
        # This should never happen in runtime
        return None

    def merge_defaults(self) -> Dict[str, Any]:
        if self.parent is None:
            return deepcopy(self.defaults)
        return utils.dict_deepmerge(self.parent.merge_defaults(), self.defaults)

    def add_scenario(self, scenario: 'ScenarioDef') -> 'ScenarioDef':
        scenario.parent = self
        # Propagate parent tags to the child
        self.scenarios.append(scenario)
        return self

    def add_test(self, test: 'TestDef', kind: str = 'normal') -> 'ScenarioDef':
        test.parent = self
        if kind == 'before':
            self.before.append(test)
        elif kind == 'after':
            self.after.append(test)
        else:
            self.tests.append(test)
        return self

    def _children_tags(self) -> Set[str]:
        tags = set()
        for sc in self.scenarios:
            tags.update(sc._children_tags())
        for test in self.tests:
            tags.update(test.tags)
        return tags


class TestDef(_Definition):
    AD_EXCLUDED = ['suite', 'scenario']

    def __init__(self, name: str, desc: str, tags: List[str] = None,
                 scenario: 'ScenarioDef' = None, params: Dict[str, Any] = None):
        super().__init__(name, desc, parent=scenario)
        self.params: Dict[str, Any] = params or {}
        self.action: Optional[TestActionDef] = None
        self.validators: List[TestActionValidatorDef] = []
        self.tags: Set[str] = set(tags or [])

    @property
    def is_required(self) -> bool:
        return utils.to_bool(self.params.get('required'))

    @property
    def scenario(self) -> 'ScenarioDef':
        return self._parent

    @property
    def suite(self) -> 'SuiteDef':
        return self.scenario.suite

    def defaults(self):
        return self.scenario.merge_defaults()


class TestEntityDef(AsDict):
    def __init__(self, name: str, params: Dict[str, Any]):
        self.name = name
        self.params = params


class TestActionDef(TestEntityDef):
    pass


class TestActionValidatorDef(TestEntityDef):
    pass


def _update_tags(parent: Set['str'], tags: Set[str]) -> Set[str]:
    full = parent.copy()
    for tag in tags:
        if tag.startswith('-'):
            tag = tag[1:]
            if tag in full:
                full.remove(tag)
        else:
            full.add(tag)
    return full
