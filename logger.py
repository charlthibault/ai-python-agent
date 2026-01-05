import logging

from rich.logging import RichHandler

logger = logging.getLogger("python-ai-agent")

handler = RichHandler(
    show_time=False,
    show_path=False,
    markup=True,
    rich_tracebacks=True,
)
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)
