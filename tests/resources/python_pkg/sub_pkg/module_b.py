"""Another dummy module."""
import sys
from pathlib import Path

import icecream as ic


def another_dummy_function() -> None:
    """Do stuff."""
    import nox
    
    sys.version_info
    ic(Path.cwd())
    nox.Session
    return None
