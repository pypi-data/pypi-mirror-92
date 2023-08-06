import copy
from typing import Dict, Any, Type

from pycmdtf import defs, utils
from pycmdtf.config import Config
from pycmdtf.utils import LOG, fs


class Parser:
    def __init__(self, cfg: 'Config'):
        self.cfg: Config = cfg

    def parse_suite(self):
        LOG.info("[PARSE] Session parsing started")
        sess_dict = fs.load_dict_from_file(self.cfg.cwd(), 'suite')
        suite, template = self._parse_shared_base(sess_dict, 'suite',
                                                  cls=defs.SuiteDef,
                                                  parent_template=self.cfg.template_vars)
        for scenario_file in sess_dict['scenarios']:
            scenario = self.parse_scenario(scenario_file, template)
            suite.add_scenario(scenario)

        return suite

    def parse_scenario(self, file_path, template_vars: Dict[str, Any] = None):
        template_vars = copy.deepcopy(template_vars or {})
        LOG.info(f"[PARSE] Scenario: {file_path}")
        sc_dict = fs.load_config_file(self.cfg.cwd() / file_path)
        scenario, template_vars = self._parse_shared_base(
            sc_dict, 'scenario', parent_template=template_vars,
            cls=defs.ScenarioDef, depends_on=sc_dict.get('depends_on'),
        )

        for kind in ('before', 'tests', 'after'):
            for test in self._parse_tests(sc_dict, kind=kind, parent_vars=template_vars):
                scenario.add_test(test, kind)

        # Sub-scenarios, optional
        for sub_file in sc_dict.get('scenarios', []):
            scenario.add_scenario(self.parse_scenario(sub_file, template_vars))
        return scenario

    def _parse_tests(self, sc_dict, kind: str, parent_vars: Dict[str, Any]):
        parent_vars = parent_vars or {}
        result = []
        for test_df in sc_dict.get(kind, []):
            template = test_df.get('template')
            if template is None:
                test = parse_test(test_df)
                result.append(test)
                continue

            stripped = utils.dict_filter(test_df, ['template', 'cases'])
            cases = test_df.get('cases', [{'vars': {}}])
            for idx, case in enumerate(cases):
                new_def = copy.deepcopy(stripped)
                new_def.update(template)
                template_params = _merge_template_vars(parent_vars, case['vars'])
                template_params.update(self.cfg.template_vars)
                new_def = utils.expand_template(new_def, template_params)
                test = parse_test(new_def)
                if len(cases) != 1:
                    test.name = f"{test.name}_{idx}"
                result.append(test)
        return result

    def _parse_shared_base(self, df: Dict[str, Any], ent_name: str,
                           parent_template: Dict[str, Any],
                           cls: Type[defs.GeneralDefinition], **kwargs):
        defaults = df.get('defaults')
        template_vars = copy.deepcopy(df.get('template_vars', {}))
        template_vars = utils.dict_deepmerge(template_vars, parent_template)
        template_vars = _merge_template_vars(parent_template, template_vars)
        entity_template = utils.expand_template(template_vars, self.cfg.template_vars)
        defaults = utils.expand_template(defaults, entity_template)
        entity = df[ent_name]
        suite = cls(**entity, defaults=defaults, **kwargs)
        return suite, template_vars


def _merge_template_vars(parent_template: Dict[str, Any],
                         template_vars: Dict[str, Any]) -> Dict[str, Any]:
    expanded = utils.expand_template(template_vars, parent_template)
    template_vars = utils.dict_deepmerge(parent_template, expanded)
    return utils.expand_template(parent_template, template_vars)


def parse_suite(cfg: 'Config') -> 'defs.SuiteDef':
    return Parser(cfg).parse_suite()


def parse_test(df: Dict) -> 'defs.TestDef':
    LOG.info(f"[PARSE] Test: {df.get('desc', '')}")
    test_main_params = ['name', 'desc', 'tags']
    name, desc, tags, params = utils.dict_extract(df, test_main_params, with_rest=True)
    test = defs.TestDef(name, desc, tags=tags)
    action_df = df.get('action')
    no_validation = params.get('no_validate', False) or params.get('no_validation', False)
    if action_df is not None:
        test.action = defs.TestActionDef(**action_df)
    else:
        test.action = defs.TestActionDef(name='cmd', params=params)
        # Add cmd validator
        if not no_validation:
            test.validators = [defs.TestActionValidatorDef('cmd', params=params)]

    validators = df.get('validators')
    if validators is None or no_validation:
        return test

    for val_df in validators:
        test.validators.append(defs.TestActionValidatorDef(**val_df))

    return test
