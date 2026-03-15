"""
DamnGood TUI - Beautiful terminal interface with colors, ASCII art, and style.
"""

import random
import sys
import time
from typing import Any, Dict, List, Optional

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.rule import Rule
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# Custom Theme
DAMNGOOD_THEME = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "server.name": "bold magenta",
        "server.enabled": "bold green",
        "server.disabled": "dim red",
        "client.name": "bold cyan",
        "client.auto": "dim yellow",
        "accent": "bold bright_magenta",
        "muted": "dim white",
        "highlight": "bold bright_cyan",
    }
)

console = Console(theme=DAMNGOOD_THEME)

# ASCII Art
LOGO_LINES = [
    r"    ██████╗  █████╗ ███╗   ███╗███╗   ██╗ ██████╗  ██████╗  ██████╗ ██████╗ ",
    r"    ██╔══██╗██╔══██╗████╗ ████║████╗  ██║██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗",
    r"    ██║  ██║███████║██╔████╔██║██╔██╗ ██║██║  ███╗██║   ██║██║   ██║██║  ██║",
    r"    ██║  ██║██╔══██║██║╚██╔╝██║██║╚██╗██║██║   ██║██║   ██║██║   ██║██║  ██║",
    r"    ██████╔╝██║  ██║██║ ╚═╝ ██║██║ ╚████║╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝",
    r"    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ",
]

TAGLINES = [
    "MCP servers, managed like a boss.",
    "Your AI assistants called. They want their configs back.",
    "One registry to rule them all.",
    "Because config files shouldn't be a damn mess.",
    "Sync once. Work everywhere.",
    "The MCP wrangler you didn't know you needed.",
    "Manage MCPs more efficiently, starting today.",
    "Centralized. Synchronized. Damn good.",
]

TIPS = [
    "[muted]Tip:[/muted] Run [highlight]damngood sync[/highlight] to push servers to all your clients",
    "[muted]Tip:[/muted] Use [highlight]damngood client list[/highlight] to see discovered AI tools",
    "[muted]Tip:[/muted] Use [highlight]damngood import[/highlight] to pull existing configs into the registry",
    "[muted]Tip:[/muted] Use [highlight]damngood add <name>[/highlight] to register a new MCP server",
    "[muted]Tip:[/muted] Use [highlight]damngood show <name>[/highlight] for detailed server info",
    "[muted]Tip:[/muted] Use [highlight]damngood instructions add <name>[/highlight] to manage agent instructions",
    "[muted]Tip:[/muted] Use [highlight]damngood skills add <name>[/highlight] to create reusable slash commands",
    "[muted]Tip:[/muted] Run [highlight]damngood instructions sync[/highlight] to push instructions to all clients",
]

# Gradient colors for the logo (top to bottom)
GRADIENT_COLORS = [
    "#ff6b6b",
    "#ee5a24",
    "#f0932b",
    "#f9ca24",
    "#badc58",
    "#6ab04c",
]


def print_logo(animate: bool = True):
    """Print the DamnGood ASCII art logo with gradient colors."""
    console.print()

    for i, line in enumerate(LOGO_LINES):
        color = GRADIENT_COLORS[i % len(GRADIENT_COLORS)]
        styled = Text(line, style=Style(color=color, bold=True))
        console.print(Align.center(styled))
        if animate:
            time.sleep(0.04)

    console.print()

    # Tagline
    tagline = random.choice(TAGLINES)
    console.print(Align.center(Text(tagline, style="italic bright_white")))
    console.print()


def print_version():
    """Print version info below the logo."""
    version_text = Text("v0.1.0", style="dim")
    console.print(Align.center(version_text))
    console.print()


def print_welcome():
    """Print the full welcome screen with logo and quick-help."""
    print_logo()
    print_version()

    # Quick-start box — MCP servers
    mcp_commands = Table.grid(padding=(0, 3))
    mcp_commands.add_column(style="highlight", justify="right")
    mcp_commands.add_column(style="white")

    mcp_commands.add_row("damngood list", "List centrally managed MCP servers")
    mcp_commands.add_row("damngood add <name>", "Add a new MCP server")
    mcp_commands.add_row("damngood sync", "Sync servers to all clients")
    mcp_commands.add_row("damngood import", "Import existing client configs")
    mcp_commands.add_row("damngood client list", "Show registered AI clients")

    mcp_panel = Panel(
        mcp_commands,
        title="[bold bright_white]⚡ MCP Servers[/]",
        border_style="bright_magenta",
        padding=(1, 2),
    )

    # Quick-start box — Instructions & Skills
    ai_commands = Table.grid(padding=(0, 3))
    ai_commands.add_column(style="highlight", justify="right")
    ai_commands.add_column(style="white")

    ai_commands.add_row("damngood instructions add <name>", "Add an instruction snippet")
    ai_commands.add_row("damngood instructions sync", "Sync instructions to all clients")
    ai_commands.add_row("damngood skills add <name>", "Add a reusable skill")
    ai_commands.add_row("damngood skills sync", "Sync skills to all clients")
    ai_commands.add_row("damngood --help", "Full help & options")

    ai_panel = Panel(
        ai_commands,
        title="[bold bright_white]🧠 Instructions & Skills[/]",
        border_style="cyan",
        padding=(1, 2),
    )

    console.print(Align.center(Columns([mcp_panel, ai_panel])))

    # Random tip
    console.print()
    console.print(Align.center(random.choice(TIPS)))
    console.print()


# Formatted Output Helpers
def print_header(title: str):
    """Print a styled section header."""
    console.print()
    console.print(Rule(f"[bold bright_magenta] {title} [/]", style="bright_magenta"))
    console.print()


def print_success(message: str):
    """Print a success message."""
    console.print(f"  [success]✓[/success] {message}")


def print_error(message: str):
    """Print an error message."""
    console.print(f"  [error]✗[/error] {message}")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"  [warning]⚠[/warning] {message}")


def print_info(message: str):
    """Print an info message."""
    console.print(f"  [info]ℹ[/info] {message}")


# Server Display
def print_server_list(servers: Dict[str, Any], title: str = "MCP Servers"):
    """Print a beautifully formatted server list."""
    if not servers:
        print_header(title)
        console.print(
            Align.center(
                Text(
                    "No servers found. Use 'damngood add <name>' to add one.",
                    style="muted",
                )
            )
        )
        console.print()
        return

    print_header(title)

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="dim",
        row_styles=["", "dim"],
        pad_edge=True,
        expand=False,
    )
    table.add_column("  Server", style="server.name", min_width=18)
    table.add_column("Command", min_width=20)
    table.add_column("Clients", style="client.name", min_width=15)
    table.add_column("Status", justify="center", min_width=10)

    for name, config in sorted(servers.items()):
        cmd = config.get("command", "N/A")
        args = " ".join(config.get("args", []))
        full_cmd = f"{cmd} {args}"
        if len(full_cmd) > 35:
            full_cmd = full_cmd[:32] + "..."

        clients = ", ".join(config.get("clients", []))
        enabled = config.get("enabled", True)
        status = (
            Text("● ACTIVE", style="server.enabled")
            if enabled
            else Text("○ OFF", style="server.disabled")
        )

        table.add_row(f"  {name}", full_cmd, clients, status)

    console.print(Align.center(table))
    console.print()


def print_server_detail(name: str, config: Dict[str, Any]):
    """Print detailed server info in a nice panel."""
    print_header(f"Server: {name}")

    detail = Table.grid(padding=(0, 2))
    detail.add_column(style="bold bright_cyan", justify="right", min_width=12)
    detail.add_column(style="white")

    detail.add_row("Type", config.get("type", "stdio"))
    detail.add_row("Command", config.get("command", "N/A"))
    detail.add_row("Args", " ".join(config.get("args", [])) or "(none)")

    env = config.get("env", {})
    if env:
        env_str = "\n".join(f"{k}={v}" for k, v in env.items())
        detail.add_row("Env", env_str)
    else:
        detail.add_row("Env", "(none)")

    clients = config.get("clients", [])
    detail.add_row("Clients", ", ".join(clients) if clients else "(none)")

    enabled = config.get("enabled", True)
    status_text = (
        Text("● Active", style="server.enabled")
        if enabled
        else Text("○ Disabled", style="server.disabled")
    )
    detail.add_row("Status", status_text)

    if "created_at" in config:
        detail.add_row("Created", config["created_at"])
    if "updated_at" in config:
        detail.add_row("Updated", config["updated_at"])

    panel = Panel(
        detail,
        border_style="bright_magenta",
        padding=(1, 3),
    )
    console.print(Align.center(panel))
    console.print()


# Client Display
def print_client_list(clients: Dict[str, Dict[str, Any]]):
    """Print a beautifully formatted client list."""
    if not clients:
        print_header("Registered Clients")
        console.print(
            Align.center(
                Text(
                    "No clients found. Use 'damngood client register' to add one.",
                    style="muted",
                )
            )
        )
        console.print()
        return

    print_header("Registered Clients")

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="dim",
        row_styles=["", "dim"],
        pad_edge=True,
        expand=False,
    )
    table.add_column("  Client", style="client.name", min_width=14)
    table.add_column("Status", justify="center", min_width=12)
    table.add_column("Discovery", justify="center", min_width=12)
    table.add_column("Config Path", style="muted", min_width=30)

    for name, client in sorted(clients.items()):
        enabled = client.get("enabled", True)
        status = (
            Text("● ACTIVE", style="server.enabled")
            if enabled
            else Text("○ OFF", style="server.disabled")
        )
        auto = (
            Text("auto", style="client.auto")
            if client.get("auto_discovered", False)
            else Text("manual", style="dim")
        )
        path = client.get("path", "N/A")
        if len(path) > 45:
            path = "..." + path[-42:]
        table.add_row(f"  {name}", status, auto, path)

    console.print(Align.center(table))
    console.print()


# Legacy Server Display
def print_legacy_server_list(servers: Dict[str, Any], client_type: str):
    """Print servers for single-client mode."""
    if not servers:
        print_header(f"Servers ({client_type})")
        console.print(Align.center(Text("No MCP servers configured.", style="muted")))
        console.print()
        return

    print_header(f"Servers ({client_type})")

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="dim",
        pad_edge=True,
        expand=False,
    )
    table.add_column("  Server", style="server.name", min_width=18)
    table.add_column("Type", min_width=8)
    table.add_column("Command", min_width=20)
    table.add_column("Status", justify="center", min_width=10)

    for name, config in sorted(servers.items()):
        stype = config.get("type", "stdio")
        cmd = config.get("command", "N/A")
        enabled = config.get("enabled", True)
        status = (
            Text("● ACTIVE", style="server.enabled")
            if enabled
            else Text("○ OFF", style="server.disabled")
        )
        table.add_row(f"  {name}", stype, cmd, status)

    console.print(Align.center(table))
    console.print()


# Sync Display
def create_sync_progress() -> Progress:
    """Create a styled progress bar for sync operations."""
    return Progress(
        SpinnerColumn("dots", style="bright_magenta"),
        TextColumn("[bold bright_white]{task.description}"),
        BarColumn(
            bar_width=30,
            style="dim",
            complete_style="bright_magenta",
            finished_style="green",
        ),
        TextColumn("[muted]{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    )


def print_sync_header(server_count: int, client_count: int):
    """Print sync operation header."""
    print_header("Syncing")
    console.print(
        Align.center(
            Text(
                f"Pushing {server_count} server(s) → {client_count} client(s)",
                style="bold bright_white",
            )
        )
    )
    console.print()


def print_sync_client(client_name: str, synced_count: int, path: str):
    """Print sync status for a single client."""
    console.print(
        f"  [success]✓[/success] [client.name]{client_name}[/client.name]  "
        f"[muted]→[/muted]  {synced_count} server(s)  "
        f"[muted]({path})[/muted]"
    )


def print_sync_complete():
    """Print sync complete message."""
    console.print()
    console.print(
        Align.center(
            Panel(
                "[bold green]✓ Sync complete![/]",
                border_style="green",
                padding=(0, 3),
            )
        )
    )
    console.print()


# Import Display
def print_import_found(server_name: str, client_name: str):
    """Print discovered server during import."""
    console.print()
    console.print(
        f"  [accent]Found[/accent] server [server.name]{server_name}[/server.name] "
        f"in [client.name]{client_name}[/client.name]"
    )


def print_capability_warning(client_name: str, feature: str):
    """Warn that a client does not support a feature."""
    console.print(
        f"  [warning]⚠[/warning] [client.name]{client_name}[/client.name] "
        f"does not support [highlight]{feature}[/highlight] — skipping"
    )


def print_instructions_sync_result(client_name: str, snippet_count: int, path: str):
    """Print sync status for instructions written to a single client."""
    console.print(
        f"  [success]✓[/success] [client.name]{client_name}[/client.name]  "
        f"[muted]→[/muted]  {snippet_count} snippet(s)  "
        f"[muted]({path})[/muted]"
    )


def print_skills_sync_result(client_name: str, skill_name: str, path: str):
    """Print sync status for a single skill written to a client."""
    console.print(
        f"  [success]✓[/success] [client.name]{client_name}[/client.name]  "
        f"[muted]→[/muted]  [server.name]{skill_name}[/server.name]  "
        f"[muted]({path})[/muted]"
    )


def print_snippet_list(snippets: Dict[str, Any]):
    """Print a formatted table of instruction snippets."""
    if not snippets:
        print_header("Instruction Snippets")
        console.print(
            Align.center(
                Text(
                    "No snippets found. Use 'damngood instructions add <name>' to add one.",
                    style="muted",
                )
            )
        )
        console.print()
        return

    print_header("Instruction Snippets")

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="dim",
        row_styles=["", "dim"],
        pad_edge=True,
        expand=False,
    )
    table.add_column("  Snippet", style="server.name", min_width=18)
    table.add_column("Description", min_width=28)
    table.add_column("Clients", style="client.name", min_width=18)
    table.add_column("Status", justify="center", min_width=10)

    for name, meta in sorted(snippets.items()):
        desc = meta.get("description", "")
        if len(desc) > 35:
            desc = desc[:32] + "..."
        clients = ", ".join(meta.get("clients", []))
        enabled = meta.get("enabled", True)
        status = (
            Text("● ON", style="server.enabled")
            if enabled
            else Text("○ OFF", style="server.disabled")
        )
        table.add_row(f"  {name}", desc, clients, status)

    console.print(Align.center(table))
    console.print()


def print_snippet_detail(name: str, meta: Dict[str, Any], content: str):
    """Print detailed snippet info."""
    print_header(f"Snippet: {name}")

    detail = Table.grid(padding=(0, 2))
    detail.add_column(style="bold bright_cyan", justify="right", min_width=12)
    detail.add_column(style="white")

    detail.add_row("Description", meta.get("description", "N/A"))
    clients = meta.get("clients", [])
    detail.add_row("Clients", ", ".join(clients) if clients else "(none)")
    enabled = meta.get("enabled", True)
    detail.add_row(
        "Status",
        Text("● Enabled", style="server.enabled")
        if enabled
        else Text("○ Disabled", style="server.disabled"),
    )
    if "created_at" in meta:
        detail.add_row("Created", meta["created_at"])
    if "updated_at" in meta:
        detail.add_row("Updated", meta["updated_at"])

    meta_panel = Panel(detail, title="[bold]Metadata[/]", border_style="bright_magenta", padding=(1, 2))

    content_panel = Panel(
        content.strip() if content.strip() else "[muted](empty)[/muted]",
        title="[bold]Content[/]",
        border_style="dim",
        padding=(1, 2),
    )

    console.print(Align.center(meta_panel))
    console.print(Align.center(content_panel))
    console.print()


def print_skill_list(skills: Dict[str, Any]):
    """Print a formatted table of skills."""
    if not skills:
        print_header("Skills")
        console.print(
            Align.center(
                Text(
                    "No skills found. Use 'damngood skills add <name>' to add one.",
                    style="muted",
                )
            )
        )
        console.print()
        return

    print_header("Skills")

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="dim",
        row_styles=["", "dim"],
        pad_edge=True,
        expand=False,
    )
    table.add_column("  Skill", style="server.name", min_width=18)
    table.add_column("Description", min_width=28)
    table.add_column("Clients", style="client.name", min_width=18)
    table.add_column("Invocable", justify="center", min_width=10)
    table.add_column("Status", justify="center", min_width=10)

    for name, meta in sorted(skills.items()):
        desc = meta.get("description", "")
        if len(desc) > 35:
            desc = desc[:32] + "..."
        clients = ", ".join(meta.get("clients", []))
        invocable = (
            Text("yes", style="success") if meta.get("user_invocable", True) else Text("no", style="muted")
        )
        enabled = meta.get("enabled", True)
        status = (
            Text("● ON", style="server.enabled")
            if enabled
            else Text("○ OFF", style="server.disabled")
        )
        table.add_row(f"  {name}", desc, clients, invocable, status)

    console.print(Align.center(table))
    console.print()


def print_skill_detail(name: str, meta: Dict[str, Any], content: str):
    """Print detailed skill info."""
    print_header(f"Skill: {name}")

    detail = Table.grid(padding=(0, 2))
    detail.add_column(style="bold bright_cyan", justify="right", min_width=14)
    detail.add_column(style="white")

    detail.add_row("Description", meta.get("description", "N/A"))
    clients = meta.get("clients", [])
    detail.add_row("Clients", ", ".join(clients) if clients else "(none)")
    detail.add_row(
        "User-invocable",
        Text("yes", style="success") if meta.get("user_invocable", True) else Text("no", style="muted"),
    )
    tools = meta.get("allowed_tools", [])
    detail.add_row("Allowed tools", ", ".join(tools) if tools else "(all)")
    enabled = meta.get("enabled", True)
    detail.add_row(
        "Status",
        Text("● Enabled", style="server.enabled")
        if enabled
        else Text("○ Disabled", style="server.disabled"),
    )
    if "created_at" in meta:
        detail.add_row("Created", meta["created_at"])
    if "updated_at" in meta:
        detail.add_row("Updated", meta["updated_at"])

    meta_panel = Panel(detail, title="[bold]Metadata[/]", border_style="bright_magenta", padding=(1, 2))
    content_panel = Panel(
        content.strip() if content.strip() else "[muted](empty)[/muted]",
        title="[bold]Content[/]",
        border_style="dim",
        padding=(1, 2),
    )

    console.print(Align.center(meta_panel))
    console.print(Align.center(content_panel))
    console.print()


def print_import_result(imported: List[str]):
    """Print import summary."""
    if imported:
        console.print()
        console.print(
            Align.center(
                Panel(
                    f"[bold green]✓ Imported {len(imported)} server(s):[/]\n"
                    + ", ".join(f"[server.name]{s}[/server.name]" for s in imported)
                    + "\n\n[muted]Run 'damngood sync' to push to all clients[/muted]",
                    border_style="green",
                    padding=(1, 3),
                )
            )
        )
    else:
        console.print()
        print_info("No new servers to import")
    console.print()
