"""
Shared utilities for damngood instructions and skills management.
"""

import os
import platform as _platform
import re
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Tuple


def _detect_os() -> str:
    system = _platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "linux"


CURRENT_OS = _detect_os()


def get_editor() -> str:
    """Get the editor command from environment or fallback."""
    editor = os.environ.get("EDITOR")
    if editor:
        return editor

    if CURRENT_OS == "windows":
        candidates = ["code", "notepad++", "notepad"]
    else:
        candidates = ["nano", "vim", "vi"]

    for cmd in candidates:
        if shutil.which(cmd):
            return cmd

    raise RuntimeError("No editor found. Please set the EDITOR environment variable.")


def open_in_editor(path: Path) -> bool:
    """
    Open *path* in the user's preferred editor.
    Returns True if the editor exited cleanly (exit code 0), False otherwise.
    """
    editor = get_editor()
    try:
        subprocess.run([editor, str(path)], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def parse_frontmatter(text: str) -> Tuple[Dict, str]:
    """
    Parse YAML-ish frontmatter delimited by ``---`` lines at the top of *text*.

    Supports:
    - Scalars:        key: value
    - Quoted strings: key: "value"  /  key: 'value'
    - Inline lists:   key: [a, b, c]
    - Booleans:       true / false

    Returns ``(metadata_dict, body_text)``.
    If no frontmatter is present, returns ``({}, text)``.
    """
    if not text.startswith("---"):
        return {}, text

    lines = text.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, text

    fm_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1:]).lstrip("\n")

    meta: Dict = {}
    for line in fm_lines:
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if not key:
            continue

        if val.startswith("[") and val.endswith("]"):
            # Inline list: [a, b, c]
            items = [
                x.strip().strip('"').strip("'")
                for x in val[1:-1].split(",")
                if x.strip()
            ]
            meta[key] = items
        elif val.lower() == "true":
            meta[key] = True
        elif val.lower() == "false":
            meta[key] = False
        else:
            meta[key] = val.strip('"').strip("'")

    return meta, body


def build_frontmatter(meta: Dict) -> str:
    """
    Serialize *meta* back to YAML-ish frontmatter (``---`` delimited).
    """
    lines = ["---"]
    for key, val in meta.items():
        if isinstance(val, list):
            items = ", ".join(str(x) for x in val)
            lines.append(f"{key}: [{items}]")
        elif isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        else:
            s = str(val)
            # Quote if value contains characters that could confuse the parser
            if any(c in s for c in ['"', "'", ":", "#", "[", "]"]):
                s = f'"{s}"'
            lines.append(f"{key}: {s}")
    lines.append("---")
    return "\n".join(lines)


def validate_name(name: str) -> bool:
    """Return True if *name* is a safe identifier for filesystem and registry use."""
    return bool(re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$", name))
