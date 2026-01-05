from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Global console instance for consistent output
console = Console()


def print_command_start(command: str) -> None:
    header = Text()
    header.append("▶ ", style="bold green")
    header.append("Running: ", style="bold white")
    header.append(command, style="bold cyan")

    console.print()
    console.print(Panel(header, border_style="green", padding=(0, 1)))


def print_command_output(text: str) -> None:
    console.print(text, end="", highlight=False, markup=False)


def print_command_success(exit_code: int, execution_time: float | None = None) -> None:
    footer = Text()
    footer.append("✓ ", style="bold green")
    footer.append("Command completed ", style="green")
    footer.append(f"(exit code: {exit_code})", style="dim")

    if execution_time is not None:
        footer.append(f" in {execution_time:.1f}s", style="dim")

    console.print()
    console.print(Panel(footer, border_style="green", padding=(0, 1)))
    console.print()


def print_command_error(exit_code: int, error_message: str | None = None) -> None:
    footer = Text()
    footer.append("✗ ", style="bold red")
    footer.append("Command failed ", style="red")
    footer.append(f"(exit code: {exit_code})", style="dim")

    if error_message:
        footer.append(f"\n{error_message}", style="red dim")

    console.print()
    console.print(Panel(footer, border_style="red", padding=(0, 1)))
    console.print()


def print_command_timeout(partial_output: str | None = None) -> None:
    footer = Text()
    footer.append("⏱ ", style="bold yellow")
    footer.append("Command timed out", style="yellow")

    console.print()
    console.print(Panel(footer, border_style="yellow", padding=(0, 1)))
    console.print()
