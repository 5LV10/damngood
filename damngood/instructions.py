"""
DamnGood Instructions Manager — centrally manage agent instruction snippets
and sync them to AI coding tools in their native format.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from damngood.capabilities import CLIENT_CAPABILITIES, supports_instructions
from damngood.utils import (
    build_frontmatter,
    open_in_editor,
    parse_frontmatter,
    validate_name,
)

# Sentinel markers that delimit the managed block inside instruction files.
# HTML comments are invisible in rendered Markdown, so they don't clutter
# CLAUDE.md / GEMINI.md when viewed in the tool.
SENTINEL_START = "<!-- DAMNGOOD:START -->"
SENTINEL_COMMENT = "<!-- Managed by damngood. Run 'damngood instructions sync' to update. -->"
SENTINEL_END = "<!-- DAMNGOOD:END -->"

# Warn (but don't error) when Windsurf's combined char limit is approached.
WINDSURF_WARN_THRESHOLD = 11000  # actual limit is 12 000

DAMNGOOD_DIR = Path.home() / ".damngood"
INSTRUCTIONS_DIR = DAMNGOOD_DIR / "instructions"
INDEX_FILE = INSTRUCTIONS_DIR / "index.json"

try:
    from damngood.tui import (
        print_capability_warning,
        print_error,
        print_header,
        print_info,
        print_instructions_sync_result,
        print_snippet_detail,
        print_snippet_list,
        print_success,
        print_sync_complete,
        print_warning,
    )

    HAS_TUI = True
except ImportError:
    HAS_TUI = False


class InstructionsRegistry:
    """Manages central instruction snippets and syncs them to AI coding tools."""

    # ------------------------------------------------------------------ #
    # Storage helpers                                                      #
    # ------------------------------------------------------------------ #

    @classmethod
    def ensure_dirs(cls):
        INSTRUCTIONS_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def load_index(cls) -> Dict[str, Any]:
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                _err(f"Corrupted instructions index at {INDEX_FILE}: {e}")
                sys.exit(1)
        return {"version": 1, "snippets": {}}

    @classmethod
    def save_index(cls, index: Dict[str, Any]):
        cls.ensure_dirs()
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

    @classmethod
    def snippet_path(cls, name: str) -> Path:
        return INSTRUCTIONS_DIR / f"{name}.md"

    # ------------------------------------------------------------------ #
    # CRUD                                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def list_snippets(cls):
        index = cls.load_index()
        snippets = index.get("snippets", {})

        if HAS_TUI:
            print_snippet_list(snippets)
            return

        if not snippets:
            print("No instruction snippets found. Use 'damngood instructions add <name>'.")
            return

        print("\nInstruction Snippets:")
        print("-" * 72)
        print(f"{'Name':<20} {'Description':<32} {'Clients'}")
        print("-" * 72)
        for name, meta in sorted(snippets.items()):
            desc = meta.get("description", "")[:30]
            clients = ", ".join(meta.get("clients", []))
            enabled_mark = "✓" if meta.get("enabled", True) else "✗"
            print(f"{name:<20} {desc:<32} {clients} [{enabled_mark}]")
        print()

    @classmethod
    def show_snippet(cls, name: str):
        index = cls.load_index()
        snippets = index.get("snippets", {})

        if name not in snippets:
            _err(f"Snippet '{name}' not found")
            sys.exit(1)

        meta = snippets[name]
        path = cls.snippet_path(name)
        content = path.read_text(encoding="utf-8") if path.exists() else "(no content)"

        if HAS_TUI:
            print_snippet_detail(name, meta, content)
        else:
            print(f"\nSnippet: {name}")
            print("-" * 40)
            for k, v in meta.items():
                print(f"  {k}: {v}")
            print(f"\nContent:\n{content}\n")

    @classmethod
    def add_snippet(cls, name: str):
        if not validate_name(name):
            _err(f"Invalid name '{name}'. Use letters, numbers, hyphens, underscores only.")
            sys.exit(1)

        index = cls.load_index()
        if name in index.get("snippets", {}):
            _err(f"Snippet '{name}' already exists. Use 'damngood instructions edit {name}'.")
            sys.exit(1)

        supported = _instruction_client_list()
        clients_hint = ", ".join(supported)

        template = (
            f"---\n"
            f'description: "Brief description of this instruction snippet"\n'
            f"clients: [{clients_hint}]\n"
            f"enabled: true\n"
            f"---\n\n"
            f"Write your instruction content here in plain Markdown.\n\n"
            f"This will be appended to each assigned client's global instructions\n"
            f"file during sync.\n"
        )

        cls.ensure_dirs()
        tmp = INSTRUCTIONS_DIR / f"_tmp_{name}.md"
        tmp.write_text(template, encoding="utf-8")

        if not open_in_editor(tmp):
            tmp.unlink(missing_ok=True)
            _warn("Editor closed without saving. Snippet not added.")
            return

        saved = tmp.read_text(encoding="utf-8")
        tmp.unlink(missing_ok=True)

        meta, body = parse_frontmatter(saved)

        if not meta.get("description"):
            _err("Missing 'description' in frontmatter. Snippet not saved.")
            sys.exit(1)

        if not body.strip():
            _warn("Empty content body. Snippet not saved.")
            sys.exit(1)

        cls.snippet_path(name).write_text(body, encoding="utf-8")

        now = datetime.now().isoformat()
        index.setdefault("snippets", {})[name] = {
            "name": name,
            "description": meta.get("description", ""),
            "clients": meta.get("clients", []),
            "enabled": meta.get("enabled", True),
            "created_at": now,
            "updated_at": now,
        }
        cls.save_index(index)

        if HAS_TUI:
            print_success(f"Added snippet [server.name]{name}[/server.name] to instructions registry")
        else:
            print(f"Added snippet '{name}'")

    @classmethod
    def edit_snippet(cls, name: str):
        index = cls.load_index()
        snippets = index.get("snippets", {})

        if name not in snippets:
            _err(f"Snippet '{name}' not found")
            sys.exit(1)

        meta = snippets[name]
        content_path = cls.snippet_path(name)
        existing_body = content_path.read_text(encoding="utf-8") if content_path.exists() else ""

        fm_meta = {
            "description": meta.get("description", ""),
            "clients": meta.get("clients", []),
            "enabled": meta.get("enabled", True),
        }
        edit_text = build_frontmatter(fm_meta) + "\n\n" + existing_body

        cls.ensure_dirs()
        tmp = INSTRUCTIONS_DIR / f"_tmp_{name}.md"
        tmp.write_text(edit_text, encoding="utf-8")

        if not open_in_editor(tmp):
            tmp.unlink(missing_ok=True)
            _warn("Editor closed without saving. No changes made.")
            return

        saved = tmp.read_text(encoding="utf-8")
        tmp.unlink(missing_ok=True)

        new_meta, new_body = parse_frontmatter(saved)

        if not new_meta.get("description"):
            _err("Missing 'description' in frontmatter. Changes discarded.")
            sys.exit(1)

        content_path.write_text(new_body, encoding="utf-8")

        index["snippets"][name].update(
            {
                "description": new_meta.get("description", meta.get("description", "")),
                "clients": new_meta.get("clients", meta.get("clients", [])),
                "enabled": new_meta.get("enabled", meta.get("enabled", True)),
                "updated_at": datetime.now().isoformat(),
            }
        )
        cls.save_index(index)

        if HAS_TUI:
            print_success(f"Updated snippet [server.name]{name}[/server.name]")
        else:
            print(f"Updated snippet '{name}'")

    @classmethod
    def remove_snippet(cls, name: str):
        index = cls.load_index()
        snippets = index.get("snippets", {})

        if name not in snippets:
            _err(f"Snippet '{name}' not found")
            sys.exit(1)

        del index["snippets"][name]
        cls.save_index(index)
        cls.snippet_path(name).unlink(missing_ok=True)

        if HAS_TUI:
            print_success(f"Removed snippet [server.name]{name}[/server.name]")
            print_info("Run 'damngood instructions sync' to update client files.")
        else:
            print(f"Removed snippet '{name}'")
            print("Run 'damngood instructions sync' to update client files.")

    # ------------------------------------------------------------------ #
    # Sync                                                                 #
    # ------------------------------------------------------------------ #

    @classmethod
    def sync(cls):
        """Sync instruction snippets to all enabled clients that support instructions."""
        from damngood.mcp_manager import ClientManager

        index = cls.load_index()
        snippets = index.get("snippets", {})
        all_clients = ClientManager.get_enabled_clients_for_instructions()

        if not all_clients:
            _warn("No enabled clients support instructions.")
            return

        if HAS_TUI:
            print_header("Syncing Instructions")

        synced_any = False

        for client_name, client_cfg in all_clients.items():
            cap = CLIENT_CAPABILITIES.get(client_name, {})
            target_path: Path = cap.get("instructions_path")
            fmt: str = cap.get("instructions_format", "markdown")

            if not target_path:
                continue

            # Gather enabled snippets assigned to this client
            assigned: List[Tuple[str, str]] = []
            for sname, smeta in snippets.items():
                if client_name in smeta.get("clients", []) and smeta.get("enabled", True):
                    spath = cls.snippet_path(sname)
                    body = spath.read_text(encoding="utf-8").strip() if spath.exists() else ""
                    if body:
                        assigned.append((sname, body))

            managed_content = "\n\n---\n\n".join(body for _, body in assigned)

            # Read existing file
            existing = target_path.read_text(encoding="utf-8") if target_path.exists() else ""

            # Merge managed section using sentinel strategy
            new_content = _merge_managed_section(existing, managed_content, fmt, client_name)

            # Windsurf char-limit advisory
            if client_name == "windsurf" and len(new_content) > WINDSURF_WARN_THRESHOLD:
                _warn(
                    f"windsurf: combined instructions file is {len(new_content):,} chars "
                    f"(Windsurf has a 12,000 char combined limit)."
                )

            # Write to disk
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(new_content, encoding="utf-8")

            synced_any = True

            if HAS_TUI:
                print_instructions_sync_result(client_name, len(assigned), str(target_path))
            else:
                print(f"  ✓ {client_name}: {len(assigned)} snippet(s) → {target_path}")

        if synced_any:
            if HAS_TUI:
                print_sync_complete()
            else:
                print("\nInstructions sync complete!")
        else:
            if HAS_TUI:
                print_info("No snippets synced (check client assignments and snippet content).")
            else:
                print("No snippets synced.")


# ------------------------------------------------------------------ #
# Internal helpers                                                     #
# ------------------------------------------------------------------ #


def _instruction_client_list() -> List[str]:
    """Return client names that support instructions (excluding alias)."""
    return [
        c
        for c in CLIENT_CAPABILITIES
        if c != "claude-code" and supports_instructions(c)
    ]


def _merge_managed_section(
    existing: str, managed_content: str, fmt: str, client_name: str
) -> str:
    """
    Insert or replace the managed section within *existing* using sentinel markers.

    Strategy
    --------
    1. Split *existing* into ``pre``, old managed content, and ``post`` using
       the sentinel markers.
    2. If ``managed_content`` is empty → strip sentinels entirely (clean removal).
    3. Otherwise → write ``pre + SENTINEL_START + content + SENTINEL_END + post``.

    Cursor MDC special handling
    ---------------------------
    Cursor rule files require YAML frontmatter at the very top.  If the file
    is new (``existing`` is empty), we prepend the required frontmatter before
    the managed block so Cursor picks up the rule immediately with
    ``alwaysApply: true``.
    """
    pre, sentinel_found, remainder = existing.partition(SENTINEL_START)
    if sentinel_found:
        _, _, post = remainder.partition(SENTINEL_END)
    else:
        post = ""

    if not managed_content:
        # Remove managed section — keep user content only
        result = pre.rstrip("\n")
        if post.strip():
            result = result + "\n\n" + post.lstrip("\n")
        return result

    block = f"{SENTINEL_START}\n{SENTINEL_COMMENT}\n\n{managed_content}\n\n{SENTINEL_END}"

    # For Cursor MDC: prepend frontmatter when creating the file from scratch
    if fmt == "mdc" and not existing.strip():
        pre = "---\ndescription: DamnGood managed instructions\nalwaysApply: true\n---\n\n"

    result = pre.rstrip("\n")
    if result:
        result += "\n\n"
    result += block

    if post.strip():
        result += "\n\n" + post.lstrip("\n")

    return result


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
