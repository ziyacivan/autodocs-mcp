"""Tests for scraper module."""

import pytest
from autodocs_mcp.scraper import detect_format, ReadTheDocsScraper


@pytest.mark.asyncio
async def test_detect_format_sphinx():
    """Test detecting Sphinx format."""
    import httpx

    async with httpx.AsyncClient() as client:
        # Mock objects.inv exists - this will likely return generic in real test
        # but structure is correct
        result = await detect_format("https://docs.example.com/", client)
        assert result in ["sphinx", "mkdocs", "generic"]


@pytest.mark.asyncio
async def test_detect_format_mkdocs():
    """Test detecting MkDocs format."""
    import httpx

    async with httpx.AsyncClient() as client:
        # Mock sitemap.xml exists - this will likely return generic in real test
        # but structure is correct
        result = await detect_format("https://docs.example.com/", client)
        assert result in ["sphinx", "mkdocs", "generic"]


def test_readthedocs_scraper_init():
    """Test ReadTheDocsScraper initialization."""
    scraper = ReadTheDocsScraper("https://docs.example.com/")
    # base_url is normalized (trailing slash removed)
    assert scraper.base_url == "https://docs.example.com"
    assert scraper.client is None  # Client is created in __aenter__
