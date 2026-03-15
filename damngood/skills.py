"""
DamnGood Skills Manager — centrally manage skill definitions and sync them
to AI coding tools in their native SKILL.md format.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from damngood.capabilities import CLIENT_CAPABILITIES, supports_skills
from damngood.utils import (
    build_frontmatter,
    open_in_editor,
    parse_frontmatter,
    validate_name,
)

# First line written to every managed SKILL.md.  Its presence means damngood
# owns the file; absence means a user-created file that we must not overwrite.
MANAGED_MARKER = "<!-- damngood-managed: do not edit manually -->"

DAMNGOOD_DIR = Path.home() / ".damngood"
SKILLS_DIR = DAMNGOOD_DIR / "skills"
INDEX_FILE = SKILLS_DIR / "index.json"

try:
    from damngood.tui import (
        print_capability_warning,
        print_error,
        print_header,
        print_info,
        print_skill_detail,
        print_skill_list,
        print_skills_sync_result,
        print_success,
        print_sync_complete,
        print_warning,
    )

    HAS_TUI = True
except ImportError:
    HAS_TUI = False


class SkillsRegistry:
    """Manages central skill definitions and syncs them to AI coding tools."""

    # ------------------------------------------------------------------ #
    # Storage helpers                                                      #
    # ------------------------------------------------------------------ #

    @classmethod
    def ensure_dirs(cls):
        SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load_index(cls) -> Dict[str, Any]:
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                _err(f"Corrupted skills index at {INDEX_FILE}: {e}")
                sys.exit(1)
        return {"version": 1, "skills": {}}

    @classmethod
    def save_index(cls, index: Dict[str, Any]):
        cls.ensure_dirs()
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

    @classmethod
    def skill_content_path(cls, name: str) -> Path:
        return SKILLS_DIR / name / "content.md"

    # ------------------------------------------------------------------ #
    # CRUD                                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def list_skills(cls):
        index = cls.load_index()
        skills = index.get("skills", {})

        if HAS_TUI:
            print_skill_list(skills)
            return

        if not skills:
            print("No skills found. Use 'damngood skills add <name>'.")
            return

        print("\nSkills:")
        print("-" * 80)
        print(f"{'Name':<20} {'Description':<30} {'Clients':<20} {'Invocable'}")
        print("-" * 80)
        for name, meta in sorted(skills.items()):
            desc = meta.get("description", "")[:28]
            clients = ", ".join(meta.get("clients", []))
            invocable = "yes" if meta.get("user_invocable", True) else "no"
            print(f"{name:<20} {desc:<30} {clients:<20} {invocable}")
        print()

    @classmethod
    def show_skill(cls, name: str):
        index = cls.load_index()
        skills = index.get("skills", {})

        if name not in skills:
            _err(f"Skill '{name}' not found")
            sys.exit(1)

        meta = skills[name]
        content_path = cls.skill_content_path(name)
        content = content_path.read_text(encoding="utf-8") if content_path.exists() else "(no content)"

        if HAS_TUI:
            print_skill_detail(name, meta, content)
        else:
            print(f"\nSkill: {name}")
            print("-" * 40)
            for k, v in meta.items():
                print(f"  {k}: {v}")
            print(f"\nContent:\n{content}\n")

    @classmethod
    def add_skill(cls, name: str):
        if not validate_name(name):
            _err(f"Invalid name '{name}'. Use letters, numbers, hyphens, underscores only.")
            sys.exit(1)

        index = cls.load_index()
        if name in index.get("skills", {}):
            _err(f"Skill '{name}' already exists. Use 'damngood skills edit {name}'.")
            sys.exit(1)

        supported = _skill_client_list()
        clients_hint = ", ".join(supported)

        template = (
            f"---\n"
            f'description: "What this skill does"\n'
            f"user-invocable: true\n"
            f"allowed-tools: [Read, Grep, Bash]\n"
            f"clients: [{clients_hint}]\n"
            f"enabled: true\n"
            f"---\n\n"
            f"# {name}\n\n"
            f"Describe what this skill does and how to invoke it.\n\n"
            f"## Steps\n\n"
            f"1. Step one\n"
            f"2. Step two\n"
        )

        cls.ensure_dirs()
        skill_dir = SKILLS_DIR / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        tmp = skill_dir / "_tmp_content.md"
        tmp.write_text(template, encoding="utf-8")

        if not open_in_editor(tmp):
            tmp.unlink(missing_ok=True)
            _warn("Editor closed without saving. Skill not added.")
            return

        saved = tmp.read_text(encoding="utf-8")
        tmp.unlink(missing_ok=True)

        meta, body = parse_frontmatter(saved)

        if not meta.get("description"):
            _err("Missing 'description' in frontmatter. Skill not saved.")
            sys.exit(1)

        cls.skill_content_path(name).write_text(body, encoding="utf-8")

        now = datetime.now().isoformat()
        index.setdefault("skills", {})[name] = _build_skill_meta(name, meta, now, now)
        cls.save_index(index)

        if HAS_TUI:
            print_success(f"Added skill [server.name]{name}[/server.name] to skills registry")
        else:
            print(f"Added skill '{name}'")

    @classmethod
    def edit_skill(cls, name: str):
        index = cls.load_index()
        skills = index.get("skills", {})

        if name not in skills:
            _err(f"Skill '{name}' not found")
            sys.exit(1)

        meta = skills[name]
        content_path = cls.skill_content_path(name)
        existing_body = content_path.read_text(encoding="utf-8") if content_path.exists() else ""

        fm_meta = {
            "description": meta.get("description", ""),
            "user-invocable": meta.get("user_invocable", True),
            "allowed-tools": meta.get("allowed_tools", []),
            "clients": meta.get("clients", []),
            "enabled": meta.get("enabled", True),
        }
        edit_text = build_frontmatter(fm_meta) + "\n\n" + existing_body

        cls.ensure_dirs()
        tmp = SKILLS_DIR / name / "_tmp_content.md"
        tmp.write_text(edit_text, encoding="utf-8")

        if not open_in_editor(tmp):
            tmp.unlink(missing_ok=True)
            _warn("Editor closed without saving. No changes made.")
            return

        saved = tmp.read_text(encoding="utf-8")
        tmp.unlink(missing_ok=True)

        new_meta, new_body = parse_frontmatter(saved)

        if not new_meta.get("description"):
            _err("Missing 'description'. Changes discarded.")
            sys.exit(1)

        content_path.write_text(new_body, encoding="utf-8")
        index["skills"][name].update(
            {
                **_build_skill_meta(name, new_meta, meta.get("created_at"), datetime.now().isoformat()),
                # preserve original created_at
                "created_at": meta.get("created_at"),
            }
        )
        cls.save_index(index)

        if HAS_TUI:
            print_success(f"Updated skill [server.name]{name}[/server.name]")
        else:
            print(f"Updated skill '{name}'")

    @classmethod
    def remove_skill(cls, name: str):
        index = cls.load_index()
        skills = index.get("skills", {})

        if name not in skills:
            _err(f"Skill '{name}' not found")
            sys.exit(1)

        skill_meta = skills.pop(name)
        cls.save_index(index)

        # Remove central content
        content_path = cls.skill_content_path(name)
        content_path.unlink(missing_ok=True)
        skill_dir = SKILLS_DIR / name
        if skill_dir.exists():
            try:
                skill_dir.rmdir()
            except OSError:
                pass  # non-empty dir — leave it

        # Remove native SKILL.md from each assigned client (if managed)
        for client_name in skill_meta.get("clients", []):
            cap = CLIENT_CAPABILITIES.get(client_name, {})
            skills_dir = cap.get("skills_dir")
            if skills_dir:
                native = Path(skills_dir) / name / "SKILL.md"
                if native.exists() and _is_managed(native):
                    native.unlink()
                    try:
                        native.parent.rmdir()
                    except OSError:
                        pass

        if HAS_TUI:
            print_success(f"Removed skill [server.name]{name}[/server.name]")
        else:
            print(f"Removed skill '{name}'")

    # ------------------------------------------------------------------ #
    # Sync                                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def sync(cls):
        """Sync skills to all enabled clients that support skills."""
        from damngood.mcp_manager import ClientManager

        index = cls.load_index()
        skills = index.get("skills", {})
        all_clients = ClientManager.get_enabled_clients_for_skills()

        if not all_clients:
            _warn("No enabled clients support skills.")
            return

        if HAS_TUI:
            print_header("Syncing Skills")

        synced_any = False

        for client_name, client_cfg in all_clients.items():
            cap = CLIENT_CAPABILITIES.get(client_name, {})
            skills_dir: Optional[Path] = cap.get("skills_dir")
            if not skills_dir:
                continue

            skills_dir_path = Path(skills_dir)

            for skill_name, skill_meta in skills.items():
                if client_name not in skill_meta.get("clients", []):
                    continue
                if not skill_meta.get("enabled", True):
                    continue

                content_path = cls.skill_content_path(skill_name)
                body = content_path.read_text(encoding="utf-8") if content_path.exists() else ""

                target = skills_dir_path / skill_name / "SKILL.md"
                target.parent.mkdir(parents=True, exist_ok=True)

                # Safety check: if the file exists but was not created by damngood, skip it
                if target.exists() and not _is_managed(target):
                    _warn(
                        f"Skipping {skill_name} for {client_name}: "
                        f"{target} was not created by damngood (no managed marker)."
                    )
                    continue

                target.write_text(_build_skill_file(skill_meta, body), encoding="utf-8")
                synced_any = True

                if HAS_TUI:
                    print_skills_sync_result(client_name, skill_name, str(target))
                else:
                    print(f"  ✓ {client_name}: {skill_name} → {target}")

        if synced_any:
            if HAS_TUI:
                print_sync_complete()
            else:
                print("\nSkills sync complete!")
        else:
            if HAS_TUI:
                print_info("No skills synced (check client assignments).")
            else:
                print("No skills synced.")


# ------------------------------------------------------------------ #
# Internal helpers                                                     #
# ------------------------------------------------------------------ #


def _skill_client_list() -> List[str]:
    """Return client names that support skills (excluding alias)."""
    return [
        c
        for c in CLIENT_CAPABILITIES
        if c != "claude-code" and supports_skills(c)
    ]


def _build_skill_meta(
    name: str, meta: Dict[str, Any], created_at: Optional[str], updated_at: str
) -> Dict[str, Any]:
    """Normalise raw frontmatter dict into the canonical skills index schema."""
    allowed_tools = meta.get("allowed-tools", meta.get("allowed_tools", []))
    if isinstance(allowed_tools, str):
        allowed_tools = [allowed_tools]
    return {
        "name": name,
        "description": meta.get("description", ""),
        "user_invocable": meta.get("user-invocable", meta.get("user_invocable", True)),
        "allowed_tools": allowed_tools,
        "clients": meta.get("clients", []),
        "enabled": meta.get("enabled", True),
        "created_at": created_at,
        "updated_at": updated_at,
    }


def _build_skill_file(skill_meta: Dict[str, Any], body: str) -> str:
    """Render the SKILL.md content that will be written to the client's skills dir."""
    fm: Dict[str, Any] = {"description": skill_meta.get("description", "")}
    if skill_meta.get("user_invocable") is not None:
        fm["user-invocable"] = skill_meta["user_invocable"]
    tools = skill_meta.get("allowed_tools", [])
    if tools:
        fm["allowed-tools"] = tools
    return MANAGED_MARKER + "\n" + build_frontmatter(fm) + "\n\n" + body


def _is_managed(path: Path) -> bool:
    """Return True if the first line of *path* is the managed marker."""
    try:
        first_line = path.read_text(encoding="utf-8").split("\n", 1)[0]
        return first_line.strip() == MANAGED_MARKER
    except OSError:
        return False


def _err(msg: str):
    if HAS_TUI:
        print_error(msg)
    else:
        print(f"Error: {msg}")


def _warn(msg: str):
    if HAS_TUI:
        print_warning(msg)
    else:
        print(f"Warning: {msg}")
