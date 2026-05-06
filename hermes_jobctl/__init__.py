"""Hermes cron job specs (Markdown + YAML front matter)."""

__version__ = "0.1.0"
from .plugin import register

__all__ = ["__version__", "register"]
