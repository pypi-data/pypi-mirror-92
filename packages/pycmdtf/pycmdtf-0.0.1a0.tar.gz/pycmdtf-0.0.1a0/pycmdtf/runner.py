import time
from pathlib import Path
from typing import List, Dict, Optional, Union, TypeVar

from pycmdtf import defs, utils
from pycmdtf.actions.general import ActionRegister, ValidatorsRegister, TestContext, ActionCallable
from pycmdtf.actions.checks import ActionChecks
from pycmdtf.config import Config
from pycmdtf.defs import GeneralDefinition
from pycmdtf.utils import logger, Namespace
from pycmdtf.utils.result import GeneralResult, ResultKind


class SuiteRunner:
    def __init__(self, cfg: 'Config', suite: 'defs.SuiteDef'):
        self.cfg = cfg
        self.suite = suite
        self.log = logger.for_suite(cfg.paths.artifacts, suite.name)
        self._nm_res: Dict[str, ResultKind] = {}
        self._actions = ActionRegister.instance()
        self._validators = ValidatorsRegister.instance()
        self._tags_eval = utils.TagsEvaluator(cfg.tags_expr, self.suite.propagated_tags)

    def run_suite(self) -> 'SuiteResult':
        suite = self.suite
        self.log.info(f"[RUN] Suite: {suite.namespace}")
        suite_result = SuiteResult(suite)
        for scenario in suite.scenarios:
            sc_res = self.run_scenario(scenario)
            self.log.debug(f"[RUN] Scenario result: {sc_res.kind} {sc_res.message}")
            self._nm_res[scenario.namespace.str()] = sc_res.kind
            suite_result.add_scenario_result(sc_res)
        self.log.debug(f"[RUN] Suite result: {suite_result.kind} {suite_result.message or ''}")
        return suite_result

    def run_scenario(self, scenario: 'defs.ScenarioDef') -> 'ScenarioResult':
        self.log.info(f"[RUN] Scenario: {scenario.namespace}")
        scenario_result = ScenarioResult(scenario)
        # Check tags
        if not self._tags_eval.evaluate(scenario.propagated_tags):
            return scenario_result.set_skip("Tags check has failed - skipping")
        # Check dependencies:
        if not self._check_dependencies(scenario.depends_on, scenario.namespace):
            return scenario_result.set_skip("Dependency check has failed - skipping")

        # Execute scenario before tests
        if not self._execute_tests(scenario, scenario_result, scenario.before, kind='before'):
            self.log.warning(f"[RUN] Before tests has failed for {scenario.namespace}")
        else:
            # Execute scenario tests if before tests has passed
            self._execute_tests(scenario, scenario_result, scenario.tests, kind='tests')

        # Execute after tests - execute always
        if not self._execute_tests(scenario, scenario_result, scenario.after, kind='after'):
            self.log.warning(f"[RUN] Before tests has failed for {scenario.namespace}")

        if scenario.scenarios and not scenario_result.is_pass():
            self.log.warning("[RUN] Sub-scenarios are not executed since"
                             f" the scenario {scenario.namespace} did not pass, "
                             f"result = {scenario_result.kind}, message: {scenario_result.message}")
            return scenario_result

        # Execute subscenarios if any
        for sub in scenario.scenarios:
            self.log.info(f"[RUN] Sub-scenarios for {scenario.namespace}")
            sub_res = self.run_scenario(sub)
            self.log.debug(f"[RUN] Scenario result: {sub_res.kind}, {sub_res.message}")
            scenario_result.add_scenario_result(sub_res)
        return scenario_result

    def _execute_tests(self, scenario: defs.ScenarioDef, scenario_result: 'ScenarioResult',
                       collection: List['defs.TestDef'], kind: str = None):
        self.log.debug(f"[RUN] Executing {kind} tests for {scenario.namespace}")
        skip = False
        for test in collection:
            if not skip:
                start_time = time.perf_counter_ns()
                result = self.run_test(test)
                end_time = time.perf_counter_ns()
                result.elapsed = end_time - start_time
            else:
                result = TestResult(test)\
                    .set_skip("Test not executed, one of required test has failed")
            self._nm_res[scenario.namespace.str()] = result.kind
            scenario_result.add_test_result(result)
            if result.is_pass() and test.is_required:
                skip = True
        return scenario_result.is_pass()

    def run_test(self, test: defs.TestDef) -> 'TestResult':
        test_result = TestResult(test)
        self.log.info(f"[RUN] Test: {test.namespace}")
        # Check tags
        if not self._tags_eval.evaluate(test.tags):
            return test_result.set_skip("Tags check has failed - skipping")

        # create context:
        ctx = TestContext(self.cfg, test, log=self.log)

        # Execute test action
        action = self._actions.get(test.action.name)
        if not action:
            self.log.error(f"[RUN] Unable to find action: {test.action.name} for {test.namespace}")
            return test_result.set_err("Test action not found")

        try:
            action_result = self._execute_action(test, action, ctx)
            test_result.action_result = action_result
        except Exception as ex:
            self.log.error(f"[RUN] ERROR: Test action failed {test.namespace} - {test.action.name}",
                           ex)
            test_result.action_result = ex
            return test_result.set_err("Action call failed, see logs for more details!")

        # Execute action validators
        for vdef in test.validators:
            validator = self._validators.get(vdef.name)
            if not validator:
                self.log.error(f"[RUN] Unable to find validator: {vdef.name} for {test.namespace}")
                test_result.set_err(f"Test validator not found ({vdef.name})")
                break
            validator_params = self._get_params(test, test.action)
            try:
                self.log.info(f"[RUN] Validator: {vdef.name} for {test.namespace}")
                validator(ctx, validator_params, action_result)
            except Exception as ex:
                self.log.error(f"[RUN] ERROR: Test validator failed {test.namespace} - {vdef.name}",
                               ex)
                test_result.set_err("Action call failed, see logs for more details!")
                break

        test_result.add_checks(ctx.checks)

        return test_result

    def _execute_action(self, test: defs.TestDef, action: ActionCallable, ctx: 'TestContext'):
        action_params = self._get_params(test, test.action)
        self.log.info(
            f"[RUN] Action: {test.action.name} for {test.namespace}, params: {action_params}")
        start_time = time.perf_counter_ns()
        action_result = action(ctx, action_params)
        end_time = time.perf_counter_ns()
        elapsed = end_time - start_time
        self.log.debug(f"[RUN] Result Action {test.action.name} for {test.namespace} "
                       f"({elapsed} ns): f{action_result}")
        return action_result

    def _get_params(self, test: 'defs.TestDef', action: 'defs.TestEntityDef'):
        self.log.debug(f"Getting params for {test.namespace}")
        params = utils.dict_deepmerge(test.defaults(), action.params)
        self.log.debug(f"Merged params for {test.namespace}")
        return params

    def _check_dependencies(self, dependencies: List[Union[str, Dict]], nm: Namespace) -> bool:
        for dep in dependencies:
            self.log.debug(f"[RUN] Checking dependency: {dep} for {nm}")
            if isinstance(dep, str):
                dep = {'result': dep}
            assert isinstance(dep, dict)
            if 'result' in dep:
                res = self._nm_res.get(self.suite.name + '/' + dep['result'])
                if res is None:
                    self.log.warning(f"[RUN] Dependency check - missing result for: {dep}")
                    continue
                kind = dep.get('value', 'pass')
                if res != ResultKind(kind):
                    self.log.warning(f"[RUN] Dependency check - dependency failed {dep}: {res}")
                    return False
                return True
            pth = dep.get('file_exists', dep.get('file_exist'))
            if pth:
                pth = Path(pth)
                pth = pth if pth.is_absolute() else self.cfg.cwd() / pth
                if not pth.exists():
                    self.log.warning(
                        f"[RUN] Dependency check - file or dir does not exists {dep}: {pth}")
                    return False
                return True

        return True


RuntimeResult = TypeVar('RuntimeResult', bound='_Result')


class _Result(GeneralResult):
    def __init__(self, df: 'GeneralDefinition'):
        super().__init__(ResultKind.PASS, None)
        self._df = df

    def _set_result(self, result: 'GeneralResult', msg: str = None):
        if result.is_nok():
            self.kind = result.kind
            self.message = msg

    def _ad_dict(self) -> Optional[Dict]:
        x = super(_Result, self)._ad_dict()
        x['entity'] = self._df.info()
        return x


class SuiteResult(_Result):
    def __init__(self, df: 'GeneralDefinition'):
        super().__init__(df)
        self._scenario_results: List['ScenarioResult'] = []

    @property
    def df(self) -> 'defs.SuiteDef':
        return self._df

    @property
    def scenario_results(self) -> List['ScenarioResult']:
        return self._scenario_results

    def _ad_dict(self) -> Optional[Dict]:
        x = super(SuiteResult, self)._ad_dict()
        x['scenarios'] = self.scenario_results
        return x

    def add_scenario_result(self, result: 'ScenarioResult'):
        self._set_result(result, "Some of the scenarios has failed")
        self._scenario_results.append(result)


class ScenarioResult(_Result):
    def __init__(self, df):
        super().__init__(df)
        self._scenario_results: List['ScenarioResult'] = []
        self._test_results: List['TestResult'] = []

    def add_test_result(self, result: 'TestResult'):
        self._set_result(result, "Some of the tests has failed")
        self._test_results.append(result)

    def add_scenario_result(self, result: 'ScenarioResult'):
        self._set_result(result, "Some of the sub-scenarios has failed")
        self._scenario_results.append(result)

    @property
    def scenario_results(self) -> List['ScenarioResult']:
        return self._scenario_results

    @property
    def df(self) -> 'defs.ScenarioDef':
        return self._df

    @property
    def test_results(self) -> List['TestResult']:
        return self._test_results

    def _ad_dict(self) -> Optional[Dict]:
        x = super(ScenarioResult, self)._ad_dict()
        x['tests'] = self.test_results
        if self.scenario_results:
            x['scenarios'] = self.scenario_results
        return x


class TestResult(GeneralResult):
    def __init__(self, df: defs.TestDef):
        super().__init__(ResultKind.PASS, None)
        self.elapsed = 0
        self.df: 'defs.TestDef' = df
        self.action_result = None
        self.checks: Optional[ActionChecks] = None

    def add_checks(self, checks: 'ActionChecks'):
        self.checks = checks
        if self.kind.is_ok() and checks.is_fail():
            self.set_fail("Checks has failed")

    def fail_msg(self):
        res = f"Message[{self.kind.value}]: {self.message}"
        res += self.checks.fail_msg()
        return res

    def _ad_dict(self) -> Optional[Dict]:
        x = super(TestResult, self)._ad_dict()
        x['elapsed'] = self.elapsed
        x['entity'] = self.df.info()
        x['action'] = self.action_result
        x['checks'] = self.checks.checks
        return x
