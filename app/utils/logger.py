from pathlib import Path
import sys

from loguru import logger

from app.config.settings import get_settings


settings = get_settings()

# ---------------------------------------------------------
# Create Logs Folder
# ---------------------------------------------------------

log_directory = Path("logs")
log_directory.mkdir(exist_ok=True)

log_file = log_directory / "application.log"

# ---------------------------------------------------------
# Remove Default Logger
# ---------------------------------------------------------

logger.remove()

# ---------------------------------------------------------
# Console Logger
# ---------------------------------------------------------

logger.add(
    sys.stdout,
    level=settings.log_level,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# ---------------------------------------------------------
# File Logger
# ---------------------------------------------------------

logger.add(
    log_file,
    level=settings.log_level,
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    enqueue=True,
    encoding="utf-8",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level:<8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)


def get_logger():
    """
    Returns the configured Loguru logger.
    """
    return logger