import sys
import shutil
from pathlib import Path
from consolebundle import CommandRunner

def isRunningInConsole():
    def compareExecutables(p1: Path, p2: Path):
        return p1.parents[0] == p2.parents[0] and p1.stem == p2.stem

    invokedUsingCommandRunner = Path(sys.argv[0]) == Path(CommandRunner.__file__)

    consolePath = shutil.which('console')
    invokedUsingScript = consolePath is not None and compareExecutables(Path(sys.argv[0]), Path(consolePath))

    return invokedUsingCommandRunner or invokedUsingScript
