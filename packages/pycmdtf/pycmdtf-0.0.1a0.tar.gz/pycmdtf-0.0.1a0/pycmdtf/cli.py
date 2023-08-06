from pathlib import Path
from typing import List

import click

import pycmdtf
from pycmdtf import parser, runner, report
from pycmdtf.actions.general import ActionRegister, ValidatorsRegister
from pycmdtf.config import Config
from pycmdtf.utils import logger


@click.group("pycmdtf", help='Command Test Runtime - Execute test')
@click.version_option(version=pycmdtf.__version__)
@click.option("-L", "--log-level", help="Set log level", default="ERROR")
def cli_main(log_level):
    logger.load_config(log_level)


@cli_main.command('list-actions', help="List all available actions")
def cli_list_actions():
    areg = ActionRegister.instance()
    print("Actions:")
    for name in areg.ents.keys():
        print("-", name)
    print()
    vals = ValidatorsRegister.instance()
    print("Validators:")
    for name in vals.ents.keys():
        print("-", name)


@cli_main.command('help-action', help="Show help for the action")
@click.argument("action-name")
@click.option('-V', '--validator', help="Show help for the validator",
              is_flag=True, default=False)
def cli_help_action(action_name: str, validator: bool = False):
    acts = ActionRegister.instance()
    if not validator:
        val = acts.get(action_name)
        if val:
            print(f"Action name: {action_name}")
            if val.__doc__:
                print(val.__doc__)
        print()

    vals = ValidatorsRegister.instance()
    val = vals.get(action_name)
    if val:
        print(f"Validator name: {action_name}")
        if val.__doc__:
            print(val.__doc__)


@cli_main.command('parse', help="Parse suite definition")
@click.option('-T', '--template', help="Set template parameter (string)", multiple=True)
@click.argument("tests")
def cli_parse(tests: str, template: List[str]):
    cfg = Config(Path(tests))
    for temp in template:
        name, value = temp.split(':', 2)
        cfg.template_vars[name.strip()] = value.strip()
    suite = parser.parse_suite(cfg)
    print(suite.as_json())
    print_suite_definition(suite)


def print_suite_definition(suite):
    print(f"Suite[{suite.id}] {suite.desc}")
    for sc in suite.scenarios:
        print_scenario_definition(sc)


def print_scenario_definition(sc, indent=0):
    space = " " * (indent * 2)
    print(f"{space}|-> Scenario[{sc.id}] {sc.desc}")
    for col in [sc.before, sc.tests, sc.after]:
        for test in col:
            print(f"{space}|  * Test[{test.id}] {test.desc}")

    for sub in sc.scenarios:
        print_scenario_definition(sub, indent + 1)


@cli_main.command('execute', help="Execute suite")
@click.option('-A', '--artifacts', help="Artifacts directory", default=None)
@click.option('-t', '--tags-expr',
              help="Tags expression, to select test and scenarios based on tags", default=None)
@click.option('-T', '--template', help="Set template parameter (string)", multiple=True)
@click.option('-D', '--default', help="Set default parameter", multiple=True)
@click.argument("workdir")
def cli_execute(workdir: str, artifacts: str, tags_expr: str, template: List['str'],
                default: List['str'] = None):
    cfg = Config(Path(workdir), artifacts=artifacts, tags=tags_expr)
    for temp in template:
        name, value = temp.split(':', 2)
        cfg.template_vars[name.strip()] = value.strip()

    suite = parser.parse_suite(cfg)
    result = runner.SuiteRunner(cfg, suite).run_suite()
    # print(result.as_json())
    _, path = report.report_junit(result, path=cfg.paths.artifacts)
    json_report = cfg.paths.artifacts / f'report_{result.df.id}.json'
    Path(json_report).write_text(result.as_json(0))
    print(report.xml_pretty(path))

    report.print_simple_suite_result(result)

    print(f"Artifacts: {cfg.paths.artifacts}")
    print(f"JUnit report: {path}")
    print(f"JSON report: {json_report}")


if __name__ == '__main__':
    cli_main()
