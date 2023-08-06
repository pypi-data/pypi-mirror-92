## Import the features
from spells import *

## Define commands
echo = {
    "win32": "rem Starting build",
    "linux": "# starting build",
    "darwin": "$linux"
}

venv = {
    "win32": "if not exist env ( python -m venv env )",
    "linux": 'if [ ! -d "env" ]; then python3 -m venv env; fi',
    "darwin": "$linux"
}

activate = {
    "win32": r"env\scripts\activate",
    "linux": ". env/bin/activate",
    "darwin": "$linux"
}

install = {
    "$all": "python -m pip install cutesnowflakes"
}

## Run a single command
result = os_cmd(echo)

if result != 0:
    print(result)
## Make a spell from commands
result = spell(echo, venv, activate, install)

if result != 0:
    print(result)
