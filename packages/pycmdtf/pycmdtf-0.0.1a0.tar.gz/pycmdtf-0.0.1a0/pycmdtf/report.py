import sys
from io import TextIOBase
from os import unlink
from pathlib import Path
from typing import Union, List

from pycmdtf.runner import SuiteResult, TestResult, ScenarioResult
import junitparser
from xml.sax.saxutils import escape

from pycmdtf.utils import LOG


def report_junit(suite_result: 'SuiteResult', path: Path,
                 scenario_as_suite: bool = False) -> (junitparser.JUnitXml, Path):
    xml = junitparser.JUnitXml(suite_result.df.name)
    root = junitparser.TestSuite(name=suite_result.df.name)
    hostname = get_hostname()
    xml.add_testsuite(root)
    root.hostname = hostname
    flat_scenarios = flatten_scenarios(suite_result)
    for sc in flat_scenarios:
        if scenario_as_suite:
            unit_suite = junitparser.TestSuite(name=sc.df.name)
            unit_suite.hostname = hostname
            xml.add_testsuite(unit_suite)
        else:
            unit_suite = root

        for test_res in sc.test_results:
            junit_t = _report_test_result(test_res)
            unit_suite.add_testcase(junit_t)
    if path.is_dir():
        path /= f'suite_{suite_result.df.name}.xml'
    if path.exists():
        unlink(str(path))
    LOG.info(f"[REPORT] Generating Junit Report to: {path}")
    xml.write(str(path))
    return xml, path


def _report_test_result(test_res: 'TestResult'):
    junit_t = junitparser.TestCase(
        name=test_res.df.desc,
        classname=test_res.df.namespace.str(),
    )
    junit_t.time = test_res.elapsed / 1000000000.0
    msg = escape(test_res.message or '')
    if test_res.is_skip():
        junit_t.result = [junitparser.Skipped(msg)]
    if test_res.is_fail():
        res = [junitparser.Failure(msg)]
        for check in test_res.checks.checks:
            if check.is_nok():
                fail = junitparser.Failure(escape(check.message or ''))
                fail.text = escape(check.fail_msg(True))
                res.append(fail)
        junit_t.result = res
    if test_res.is_error():
        junit_t.result = [junitparser.Error(msg)]
    return junit_t


def print_simple_suite_result(result: 'SuiteResult', out: TextIOBase = sys.stdout):
    suite = result.df
    out.write(f"Suite[{suite.id}] {suite.desc}: {result.kind.value}\n")
    for sc_res in result.scenario_results:
        print_simple_scenario_result(sc_res, out=out, indent=0)


def print_simple_scenario_result(result: 'ScenarioResult', out: TextIOBase = sys.stdout,
                                 indent: int = 0):
    space = " " * (indent * 2)
    sc = result.df
    out.write(f"{space} -> Scenario[{sc.id}] {sc.desc}: {result.kind.value}\n")
    if not result.is_pass():
        out.write(f"{space}  Message: {result.message}\n")
    for tres in result.test_results:
        t = tres.df
        out.write(f"{space}  * [{t.id}] {t.desc}: {tres.kind.value}\n")
        if not tres.is_pass():
            out.write(tres.checks.fail_msg(False))

    for sub_res in result.scenario_results:
        print_simple_scenario_result(sub_res, out=out, indent=indent + 1)


def flatten_scenarios(ent: Union['ScenarioResult', 'SuiteResult']) -> List[ScenarioResult]:
    result = []
    for sc in ent.scenario_results:
        result.append(sc)
        result.extend(flatten_scenarios(sc))
    return result


def get_hostname() -> str:
    import socket
    return socket.gethostname()


def xml_pretty(path: Path) -> str:
    import xml.dom.minidom
    try:
        dom = xml.dom.minidom.parse(str(path))
        return dom.toprettyxml()
    except Exception as e:
        LOG.error(f"[XML] Unable to parse the XML {path}: e", e)
        return ''
