import sys

from loguru import logger

from app.config import get_settings


def setup_logging() -> None:
    """Configure loguru to log only to the console (no file sinks)."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=get_settings().log_level.upper(),
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )
