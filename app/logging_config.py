import logging
import os


def configure_logging() -> None:
    """Configure production-ready logging.

    No print(). No stack traces exposed to users here.
    """

    level_name = os.environ.get('LOG_LEVEL', 'INFO').upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    if root.handlers:
        # Avoid duplicate handlers when create_app is called multiple times.
        root.setLevel(level)
        return

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(name)s - %(message)s'
    )
    handler.setFormatter(formatter)

    root.addHandler(handler)
    root.setLevel(level)

