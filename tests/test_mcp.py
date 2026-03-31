from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_exa._mcp import (
    crawling_exa,
    get_api_key,
    get_code_context_exa,
    web_search_advanced_exa,
    web_search_exa,
)


@pytest.fixture
def mock_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXA_API_KEY", "test-api-key")


@pytest.fixture
def sample_search_response() -> dict[str, Any]:
    return {
        "results": [
            {
                "title": "Test Result",
                "url": "https://example.com",
                "content": "Test content",
            }
        ]
    }


class TestGetApiKey:
    def test_get_api_key_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("EXA_API_KEY", "test-key")
        assert get_api_key() == "test-key"

    def test_get_api_key_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("EXA_API_KEY", raising=False)
        assert get_api_key() is None


class TestWebSearchExa:
    @pytest.mark.asyncio
    async def test_web_search_success(
        self,
        mock_api_key: None,
        sample_search_response: dict[str, Any],
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_search_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await web_search_exa("test query")

            assert "results" in result
            assert len(result["results"]) == 1

    @pytest.mark.asyncio
    async def test_web_search_empty_query(self, mock_api_key: None) -> None:
        result = await web_search_exa("")
        assert result["results"] == []
        assert "empty" in result["message"].lower()


class TestGetCodeContextExa:
    @pytest.mark.asyncio
    async def test_code_context_success(
        self,
        mock_api_key: None,
        sample_search_response: dict[str, Any],
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_search_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await get_code_context_exa("Python asyncio")

            assert "results" in result


class TestCrawlingExa:
    @pytest.mark.asyncio
    async def test_crawling_success(
        self,
        mock_api_key: None,
        sample_search_response: dict[str, Any],
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_search_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await crawling_exa("https://example.com")

            assert "results" in result

    @pytest.mark.asyncio
    async def test_crawling_empty_url(self, mock_api_key: None) -> None:
        result = await crawling_exa("")
        assert result["results"] == []
        assert "empty" in result["message"].lower()


class TestWebSearchAdvancedExa:
    @pytest.mark.asyncio
    async def test_advanced_search_success(
        self,
        mock_api_key: None,
        sample_search_response: dict[str, Any],
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_search_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await web_search_advanced_exa(
                query="AI companies",
                category="company",
                num_results=20,
            )

            assert "results" in result

    @pytest.mark.asyncio
    async def test_advanced_search_empty_query(self, mock_api_key: None) -> None:
        result = await web_search_advanced_exa("")
        assert result["results"] == []
        assert "empty" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_advanced_search_with_dates(
        self,
        mock_api_key: None,
        sample_search_response: dict[str, Any],
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_search_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await web_search_advanced_exa(
                query="machine learning",
                start_published_date="2024-01-01",
                end_published_date="2024-12-31",
            )

            assert "results" in result

    @pytest.mark.asyncio
    async def test_advanced_search_with_summary(
        self,
        mock_api_key: None,
        sample_search_response: dict[str, Any],
    ) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = sample_search_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=mock_response)
            mock_client.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_client.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await web_search_advanced_exa(
                query="Python best practices",
                enable_summary=True,
                summary_query="What are the main takeaways?",
            )

            assert "results" in result
