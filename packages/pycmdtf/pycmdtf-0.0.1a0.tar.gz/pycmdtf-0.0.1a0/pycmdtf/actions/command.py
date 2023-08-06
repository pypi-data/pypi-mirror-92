import os
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, MutableMapping

from pycmdtf import utils
from pycmdtf.actions import general
from pycmdtf.actions.general import TestContext
from pycmdtf.utils import AsDict, execute_cmd, CommandResult

DIFF_MODES = dict(
    normal=['-u'],
    case=['-u', '-i'],
    space=['-u', '-b', '-B', '-w'],
    casespace=['-u', '-b', '-B', '-w', '-i'],
)


class CommandActionResult(AsDict):
    def __init__(self, cmd: Union[List[str], str], cmd_result: CommandResult,
                 valgrind: Optional[Path] = None):
        self.valgrind = valgrind
        self.cmd = cmd
        self.cmd_result = cmd_result

    @property
    def stdout(self) -> Path:
        return self.cmd_result.stdout

    @property
    def stderr(self) -> Path:
        return self.cmd_result.stderr

    @property
    def exit_code(self) -> int:
        return self.cmd_result.exit

    def as_dict(self) -> MutableMapping:
        cmd_dict = self.cmd_result.as_dict()
        cmd_dict['cmd'] = self.cmd
        if self.valgrind is not None:
            cmd_dict['valgrind'] = str(self.valgrind)
        return cmd_dict


@general.action('cmd')
def command_action(ctx: 'TestContext', params: Dict[str, Any]) -> CommandActionResult:
    environment = {
        'CMDT_SUITE': ctx.test.suite.id,
        'CMDT_TEST': ctx.test.id,
        'CMDT_SCENARIO': ctx.test.scenario.id,
        'CMDT_TEST_NM': ctx.test.namespace.str(),
        'CMDT_CFG_ARTIFACTS': ctx.cfg.paths.artifacts,
        'CMDT_CFG_WORKDIR': ctx.cfg.paths.workdir,
        'CMDT_OUTPUTS': ctx.outputs,
    }

    all_env = os.environ.copy()
    all_env.update(environment)

    stdout = ctx.outputs / f'{ctx.test.id}-action.stdout'
    stderr = ctx.outputs / f'{ctx.test.id}-action.stderr'

    stdin = FileAssertion.parse(params.get('in'))
    in_path = _create_assertion(ctx, stdin, kind='stdin', ext='in')

    cmd_param = params['cmd']  # it is must!
    cmd_param = cmd_param if isinstance(cmd_param, list) else [cmd_param]
    args = params.get('args', [])
    timeout = params.get('timeout', 600)
    cwd = ctx.cwd()
    valgrind = utils.to_bool(params.get('valgrind', False))

    command = [*cmd_param, *args]
    val_log = None
    if valgrind:
        val_log = ctx.outputs / f'{ctx.test.id}-action.valgrind.log'
        command = ['valgrind',
                   "--leak-check=full",
                   "--track-fds=yes",
                   "--child-silent-after-fork=yes",
                   f'--log-file={val_log}',
                   '--', *command]

    cmd_result: CommandResult = execute_cmd(
        command,
        log=ctx.log,
        stdout=stdout,
        stderr=stderr,
        stdin=in_path,
        cwd=str(cwd),
        env=all_env,
        timeout=timeout,
    )

    return CommandActionResult(command, cmd_result=cmd_result, valgrind=val_log)


@general.validator(name="cmd")
def validate_command_action(ctx: 'TestContext', params: Dict[str, Any],
                            action_result: 'CommandActionResult'):
    ctx.log.info(f"[VALID] Validating: {action_result}")
    validate_exit_code(ctx, params, action_result)
    validate_stdout(ctx, params, action_result)
    validate_stderr(ctx, params, action_result)

    if utils.to_bool(params.get('valgrind', False)):
        pass


@general.validator(name="cmd_exit")
def validate_exit_code(ctx: 'TestContext', params: Dict[str, Any],
                       action_result: 'CommandActionResult'):
    expected = int(params.get('exit', 0))
    expected = expected if expected != "any" else None
    if expected is not None:
        return ctx.checks.check(
            "exit_code",
            expected == action_result.exit_code,
            provided=action_result.exit_code,
            expected=expected,
            msg="Provided exit code does not match",
        )


@general.validator(name="cmd_stdout")
def validate_stdout(ctx: 'TestContext', params: Dict[str, Any],
                    action_result: 'CommandActionResult'):
    expected = FileAssertion.parse(params.get('out'))
    if not expected:
        return True
    provided = action_result.stdout

    return _validate_content(ctx, params, expected, provided, kind='stdout')


@general.validator(name="cmd_stderr")
def validate_stderr(ctx: 'TestContext', params: Dict[str, Any],
                    action_result: 'CommandActionResult'):
    expected = FileAssertion.parse(params.get('err'))
    if not expected:
        return True
    provided = action_result.stderr

    return _validate_content(ctx, params, expected, provided, kind='stderr')


def _validate_content(ctx, params, expected: 'FileAssertion', provided: Path, kind: str):
    ctx.log.debug(f"[VALIDATE] Validating content[{kind}]: "
                  f"expected={expected}; provided={provided}")
    if expected.is_empty():
        size = provided.stat().st_size
        return ctx.checks.check(
            kind,
            size == 0,
            expected=0,
            provided=size,
            msg="File should be empty"
        )
    exp_path = _create_assertion(ctx, expected, kind)
    stdout = ctx.outputs / f'{ctx.test.id}-diff_{kind}.stdout'
    stderr = ctx.outputs / f'{ctx.test.id}-diff_{kind}.stderr'
    diff_mode = params.get('diff_mode', 'normal')
    diff_args = DIFF_MODES.get(diff_mode) or DIFF_MODES['normal']
    cwd = ctx.cwd()
    diff_cmd_res: CommandResult = execute_cmd(
        ['diff', *diff_args, str(provided), str(exp_path)],
        log=ctx.log,
        stdout=stdout,
        stderr=stderr,
        cwd=cwd,
    )
    return ctx.checks.check(
        f"diff_{kind}",
        diff_cmd_res.exit == 0,
        expected=str(exp_path),
        provided=str(provided),
        diff=str(stdout),
        detail=diff_cmd_res.as_dict(),
        msg=f"{kind.capitalize()} content do not match"
    )


def _create_assertion(ctx: TestContext, expected: 'FileAssertion',
                      kind: str, ext: str = 'out') -> Optional[Path]:
    if expected is None:
        return None
    if expected.is_path():
        if expected.path.is_absolute():
            return expected.path.resolve()
        else:
            return (ctx.cfg.cwd() / expected.path).resolve()

    exp_path = ctx.outputs / f'{ctx.test.id}-action_expected_{kind}.{ext}'
    if expected.binary:
        exp_path.write_bytes(expected.content)
    else:
        exp_path.write_text(expected.content)
    return exp_path


class FileAssertion(AsDict):
    @classmethod
    def parse(cls, inp: Any) -> Optional['FileAssertion']:
        if inp is None or inp == 'any':
            return None

        if inp in ['empty', '~']:
            return FileAssertion()

        if isinstance(inp, str):
            return FileAssertion(path=Path(inp))

        if isinstance(inp, dict):
            path = inp.get('path')
            content = inp.get('content')
            binary = inp.get('binary')
            return FileAssertion(path=path, content=content, binary=binary)

        return None

    def __init__(self, content: Union[bytes, str] = None,
                 path: Path = None, binary: bool = False):
        self.content: Optional[str, bytes] = content
        self.path: Optional[Path] = path
        self.binary: bool = binary or (isinstance(content, bytes) and content)

    def is_content(self) -> bool:
        return self.path is None and self.content is not None

    def is_empty(self) -> bool:
        return self.path is None and not self.content

    def is_path(self) -> bool:
        return self.path is not None and self.content is None

    def as_dict(self) -> MutableMapping:
        res = {
            'binary': self.binary,
        }

        if self.is_path():
            res['path'] = str(self.path)
        elif self.is_content():
            res['content'] = self.content
        return res


def to_file_path(val: Optional[str]) -> Optional[Path]:
    if not val or val in ['empty', '~']:
        return None
    return Path(val)
