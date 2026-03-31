"""Pytest configuration and fixtures."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_exa_client():
    """Create a mock Exa client."""
    with patch("mcp_exa._server.Exa") as mock:
        yield mock


@pytest.fixture
def mock_exa_results():
    """Create mock search results."""
    mock_result = MagicMock()
    mock_result.results = [
        {
            "title": "Test Result",
            "url": "https://example.com",
            "id": "https://example.com",
            "published_date": "2024-01-01",
            "author": "Test Author",
        }
    ]
    return mock_result


@pytest.fixture
def mock_api_key(monkeypatch):
    """Set mock API key for testing."""
    monkeypatch.setenv("EXA_API_KEY", "test-api-key")


@pytest.fixture
def mock_answer_result():
    """Create a mock answer result."""
    mock_citation = MagicMock()
    mock_citation.id = "https://example.com"
    mock_citation.url = "https://example.com"
    mock_citation.title = "Test"
    mock_citation.published_date = "2024-01-01"
    mock_citation.author = "Test Author"
    mock_citation.text = "Test content"

    mock_result = MagicMock()
    mock_result.answer = "Test answer"
    mock_result.citations = [mock_citation]
    return mock_result


@pytest.fixture
def mock_research_result():
    """Create a mock research result."""
    mock_result = MagicMock()
    mock_result.research_id = "test-123"
    mock_result.status = "completed"
    mock_result.created_at = 1234567890.0
    mock_result.finished_at = 1234567990.0
    mock_result.model = "exa-research-fast"
    mock_result.output = {"result": "test"}
    mock_result.cost_dollars = MagicMock()
    mock_result.cost_dollars.neural = 0.01
    mock_result.cost_dollars.keyword = 0.001
    return mock_result
