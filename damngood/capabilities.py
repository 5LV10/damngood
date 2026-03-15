"""
DamnGood capabilities matrix - tracks what each AI coding tool supports
for instructions and skills, and where to find those files per platform.
"""

import os
import platform as _platform
from pathlib import Path
from typing import Any, Dict, Optional


def _detect_os() -> str:
    system = _platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "linux"


def _get_appdata() -> Path:
    return Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming")))


CURRENT_OS = _detect_os()


def _build_capabilities() -> Dict[str, Dict[str, Any]]:
    home = Path.home()
    caps: Dict[str, Dict[str, Any]] = {}

    # Claude Code CLI — key "claude" in clients.json, also aliased as "claude-code"
    caps["claude"] = {
        "instructions": True,
        "instructions_path": home / ".claude" / "CLAUDE.md",
        "instructions_format": "markdown",
        "skills": True,
        "skills_dir": home / ".claude" / "skills",
    }
    caps["claude-code"] = caps["claude"]  # alias

    # Gemini CLI
    caps["gemini"] = {
        "instructions": True,
        "instructions_path": home / ".gemini" / "GEMINI.md",
        "instructions_format": "markdown",
        "skills": False,
        "skills_dir": None,
    }

    # Cursor — writes a dedicated .mdc rule file (always-apply)
    caps["cursor"] = {
        "instructions": True,
        "instructions_path": home / ".cursor" / "rules" / "damngood-instructions.mdc",
        "instructions_format": "mdc",
        "skills": False,
        "skills_dir": None,
    }

    # Windsurf (Codeium) — global rules markdown file
    caps["windsurf"] = {
        "instructions": True,
        "instructions_path": home / ".codeium" / "windsurf" / "memories" / "global_rules.md",
        "instructions_format": "markdown",
        "skills": False,
        "skills_dir": None,
    }

    # OpenCode — platform-specific base dir
    if CURRENT_OS == "windows":
        opencode_base = _get_appdata() / "opencode"
    else:
        opencode_base = home / ".config" / "opencode"

    caps["opencode"] = {
        "instructions": True,
        "instructions_path": opencode_base / "AGENTS.md",
        "instructions_format": "markdown",
        "skills": True,
        "skills_dir": opencode_base / "skills",
    }

    # Continue.dev — dedicated rule file (does not touch user's other rules)
    caps["continue"] = {
        "instructions": True,
        "instructions_path": home / ".continue" / "rules" / "damngood.md",
        "instructions_format": "markdown",
        "skills": False,
        "skills_dir": None,
    }

    # Claude Desktop — no global instructions file
    caps["claude_desktop"] = {
        "instructions": False,
        "instructions_path": None,
        "instructions_format": None,
        "skills": False,
        "skills_dir": None,
    }

    return caps


CLIENT_CAPABILITIES: Dict[str, Dict[str, Any]] = _build_capabilities()


def supports_instructions(client_name: str) -> bool:
    return CLIENT_CAPABILITIES.get(client_name, {}).get("instructions", False)


def supports_skills(client_name: str) -> bool:
    return CLIENT_CAPABILITIES.get(client_name, {}).get("skills", False)


def get_instructions_path(client_name: str) -> Optional[Path]:
    return CLIENT_CAPABILITIES.get(client_name, {}).get("instructions_path")


def get_instructions_format(client_name: str) -> Optional[str]:
    return CLIENT_CAPABILITIES.get(client_name, {}).get("instructions_format")


def get_skills_dir(client_name: str) -> Optional[Path]:
    return CLIENT_CAPABILITIES.get(client_name, {}).get("skills_dir")
