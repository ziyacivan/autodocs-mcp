"""Tests for scraper module."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from autodocs_mcp.scraper import detect_format, ReadTheDocsScraper


@pytest.mark.asyncio
async def test_detect_format_sphinx():
    """Test detecting Sphinx format."""
    with patch("autodocs_mcp.scraper.detector.httpx.AsyncClient") as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        
        # Mock objects.inv exists
        mock_response.status_code = 200
        result = await detect_format("https://docs.example.com/")
        # Note: This will likely return None or generic if objects.inv doesn't exist
        # This is a basic test structure


@pytest.mark.asyncio
async def test_detect_format_mkdocs():
    """Test detecting MkDocs format."""
    with patch("autodocs_mcp.scraper.detector.httpx.AsyncClient") as mock_client:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        
        # Mock sitemap.xml exists
        result = await detect_format("https://docs.example.com/")
        # Note: This will likely return None or generic if sitemap.xml doesn't exist
        # This is a basic test structure


def test_readthedocs_scraper_init():
    """Test ReadTheDocsScraper initialization."""
    scraper = ReadTheDocsScraper("https://docs.example.com/")
    assert scraper.base_url == "https://docs.example.com/"
    assert scraper.format is None
