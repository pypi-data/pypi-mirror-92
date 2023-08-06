import logging
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from pycmdtf.utils.dicttool import AsDict
from pycmdtf.utils.logger import LOG

TIMEOUT_EXIT = 251


def execute_cmd(cmd: Union[str, List[str]], ws: Path = None, stdin: Optional[Path] = None,
                stdout: Path = None, stderr: Path = None, nm: str = None, cwd: str = None,
                log: logging.Logger = None, **kwargs) -> 'CommandResult':
    log = log or LOG
    cwd = str(cwd) if cwd else None
    nm = nm or cmd[0] if isinstance(cmd, list) else cmd.split()[0]
    stdout = stdout or ws / f'{nm}.stdout'
    stderr = stderr or ws / f'{nm}.stderr'
    log.info(f"[CMD] Execute: {cmd}")
    log.debug(f"[CMD] (cwd: {cwd}; stdin: {stdin}; out: {stdout}; err: {stderr})")

    start_time = time.perf_counter_ns()
    exec_result, ok = _exec_command(cmd, stdin, stdout, stderr, cwd, kwargs)
    end_time = time.perf_counter_ns()
    log.info(f"[CMD] Result: {exec_result}")
    log.debug(f" -> Command stdout {stdout}")
    log.debug(f"STDOUT: {stdout.read_bytes()}")
    log.debug(f" -> Command stderr {stderr}")
    log.debug(f"STDERR: {stderr.read_bytes()}")

    return CommandResult(
        exit_code=exec_result.returncode if ok else TIMEOUT_EXIT,
        timeout=None if ok else exec_result.timeout,
        elapsed=end_time - start_time,
        stdout=stdout,
        stderr=stderr,
    )


def _exec_command(cmd: Union[str, List[str]], stdin: Path, stdout: Path, stderr: Path,
                  cwd, kwargs) -> (Any, bool):
    with stdout.open('w') as fd_out, stderr.open('w') as fd_err:
        fd_in = Path(stdin).open() if stdin else None
        try:
            exec_result = subprocess.run(
                cmd,
                stdout=fd_out,
                stderr=fd_err,
                stdin=fd_in,
                cwd=cwd,
                **kwargs
            )
        except subprocess.TimeoutExpired as e:
            return e, False
        if fd_in:
            fd_in.close()
    return exec_result, True


class CommandResult(AsDict):
    def __init__(self, exit_code: int, stdout: Path, stderr: Path,
                 elapsed: int, timeout: Optional[int] = None):
        self.exit = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.elapsed = elapsed
        self.timeout = timeout

    def as_dict(self) -> Dict:
        res = {
            'exit': self.exit,
            'stdout': str(self.stdout),
            'stderr': str(self.stderr),
            'elapsed': self.elapsed,
        }
        if self.timeout is not None:
            res['timeout'] = self.timeout
        return res
