"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for tests."""
    return Path(tmp_path)


@pytest.fixture
def sample_docs_url():
    """Sample documentation URL for testing."""
    return "https://docs.example.com/"


@pytest.fixture
def sample_page_data():
    """Sample page data for testing."""
    return {
        "url": "https://docs.example.com/page1.html",
        "title": "Test Page",
        "content": "This is test content for the page.",
    }


@pytest.fixture
def mock_httpx_client():
    """Mock httpx client for testing."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.text = "<html><body>Test content</body></html>"
    mock_response.status_code = 200
    mock_client.get = AsyncMock(return_value=mock_response)
    return mock_client
