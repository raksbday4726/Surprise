from __future__ import annotations

import os

from app.config import DevelopmentConfig, ProductionConfig, TestingConfig


def get_config_from_env() -> type:
    """Configuration factory based on FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'development').lower()
    if env == 'production':
        return ProductionConfig
    if env == 'testing':
        return TestingConfig
    return DevelopmentConfig

