from __future__ import annotations

import sys
import logging

from subprocess import Popen, PIPE
from io import StringIO

from state import get_state

class _SimpleIO(StringIO):
    def __init__(self, initial_value: str = None, newline: str = None) -> None:
        super().__init__(initial_value=initial_value, newline=newline)

    def fileno(self) -> int:
        return 1

_log = logging.getLogger()
_log.setLevel(logging.INFO)

_SYSTEM = sys.platform

_shells = {
    "win32": ["cmd.exe", "/C"],
    "linux": ["/bin/sh", "-c"],
    "darwin": ["/bin/sh", "-c"]
}

_SHELL = _shells[_SYSTEM]

_state = get_state()

def _get_os_cmd(matrix: dict) -> str:
    if _SYSTEM not in matrix and "$all" not in matrix:
        raise KeyError("Platform not in `matrix` dict")

    if "$all" in matrix:
        return matrix["$all"]

    command = matrix[_SYSTEM]

    if command.startswith("$"):
        return matrix[command[1:]]

    return command

def _run_cmd(command: str) -> int:
    process = None
    output = _SimpleIO()

    process = Popen(
        _SHELL[0],
        universal_newlines=True,
        stdin=PIPE,
        stdout=output,
        stderr=output,
        shell=True,
        bufsize=1
    )

    if _SYSTEM == "win32":
        process.stdin.write("@echo off\n")

    process.stdin.write(command)
    process.stdin.close()
    output.close()
    process.wait()

    return process.returncode

def os_cmd(matrix: dict) -> int:
    command = _get_os_cmd(matrix)
    return _run_cmd(command + "\n")

def spell(*commands: dict) -> int:
    script = "".join(f"{_get_os_cmd(cmd)}\n" for cmd in commands)
    return _run_cmd(script)
