from pathlib import Path
import sys
import os
from typing import Union

def resource_path(relative_path: Union[str, Path]) -> Path:
    """
    Return absolute Path to resource, whether running in a PyInstaller bundle
    (sys._MEIPASS) or running normally from project root.
    relative_path: path relative to project root (e.g. "assets/stc.png")
    """
    rel = Path(relative_path)
    # running in a bundle
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / rel
    # running normally: project root is two parents up from this file
    project_root = Path(__file__).resolve().parents[2]
    return project_root / rel

def get_writable_dir() -> Path:
    """
    Return a user-writable directory for storing app data (Documents\RecordSync on Windows).
    Create directory if it does not exist.
    """
    if os.name == "nt":
        userprofile = os.environ.get("USERPROFILE")
        if userprofile:
            docs = Path(userprofile) / "Documents"
        else:
            docs = Path.home() / "Documents"
    else:
        # fallback for dev on Linux/macOS when running python main.py
        docs = Path.home() / "Documents"
    dst = docs / "RecordSync"
    dst.mkdir(parents=True, exist_ok=True)
    return dst

def writable_file(relative_name: Union[str, Path]) -> Path:
    """
    Return a Path to a writable file under the user Documents\RecordSync directory.
    """
    return get_writable_dir() / Path(relative_name).name