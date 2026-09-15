import subprocess
import sys


def quiet_subprocess_kwargs():
    """Hide console windows for command-line helpers launched by the Windows GUI."""
    if sys.platform == "win32":
        return {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)}
    return {}
