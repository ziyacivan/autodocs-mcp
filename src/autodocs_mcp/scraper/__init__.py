"""Scraper modules for different documentation formats."""

from .readthedocs import ReadTheDocsScraper
from .detector import detect_format

__all__ = ["ReadTheDocsScraper", "detect_format"]
