import logging

logger = logging.getLogger("python-ai-agent")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)
