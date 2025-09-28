from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    """Configure application-wide logging outputs for FastAPI."""
    log_dir = Path(settings.LOG_DIR)
    file_logging_enabled = False

    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        file_logging_enabled = True
    except OSError:
        # Read-only deployment targets (e.g. Vercel) reject writes next to the code package.
        fallback_dir = Path("/tmp/logs")
        try:
            fallback_dir.mkdir(parents=True, exist_ok=True)
            log_dir = fallback_dir
            file_logging_enabled = True
        except OSError:
            # Fall back to console-only logging to keep the app booting.
            file_logging_enabled = False

    log_file = log_dir / "fastapi.log"

    handlers: dict[str, dict[str, object]] = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": settings.LOG_LEVEL,
        }
    }

    root_handlers = ["console"]

    if file_logging_enabled:
        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": settings.LOG_LEVEL,
            "filename": str(log_file),
            "maxBytes": settings.LOG_MAX_BYTES,
            "backupCount": settings.LOG_BACKUP_COUNT,
            "encoding": "utf-8",
        }
        root_handlers.append("file")

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            },
        },
        "handlers": handlers,
        "root": {
            "handlers": root_handlers,
            "level": settings.LOG_LEVEL,
        },
    }

    logging.config.dictConfig(logging_config)


__all__ = ["setup_logging"]
