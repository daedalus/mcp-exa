"""Tests for mcp-exa server."""

from unittest.mock import MagicMock, patch

import pytest

from mcp_exa import get_exa_client


class TestGetExaClient:
    """Tests for get_exa_client function."""

    def test_get_exa_client_success(self, monkeypatch):
        """Test successful Exa client creation."""
        monkeypatch.setenv("EXA_API_KEY", "test-key")
        client = get_exa_client()
        assert client is not None

    def test_get_exa_client_missing_api_key(self, monkeypatch):
        """Test ValueError when API key is missing."""
        monkeypatch.delenv("EXA_API_KEY", raising=False)
        with pytest.raises(ValueError, match="EXA_API_KEY"):
            get_exa_client()


class TestSearch:
    """Tests for search tool."""

    def test_search_success(self, mock_api_key, mock_exa_results):
        """Test successful search."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(query="test query", num_results=5)
            assert "results" in result
            assert len(result["results"]) == 1

    def test_search_empty_query(self, mock_api_key):
        """Test ValueError for empty query."""
        from mcp_exa._server import search

        with pytest.raises(ValueError, match="Query cannot be empty"):
            search(query="")

    def test_search_with_contents(self, mock_api_key, mock_exa_results):
        """Test search with contents options."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(query="test", contents={"text": {"maxCharacters": 5000}})
            assert "results" in result


class TestFindSimilar:
    """Tests for find_similar tool."""

    def test_find_similar_success(self, mock_api_key, mock_exa_results):
        """Test successful find_similar."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.find_similar.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import find_similar

            result = find_similar(url="https://example.com", num_results=5)
            assert "results" in result

    def test_find_similar_empty_url(self, mock_api_key):
        """Test ValueError for empty URL."""
        from mcp_exa._server import find_similar

        with pytest.raises(ValueError, match="URL cannot be empty"):
            find_similar(url="")


class TestGetContents:
    """Tests for get_contents tool."""

    def test_get_contents_single_url(self, mock_api_key, mock_exa_results):
        """Test get_contents with single URL."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get_contents.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import get_contents

            result = get_contents(urls="https://example.com")
            assert "results" in result

    def test_get_contents_multiple_urls(self, mock_api_key, mock_exa_results):
        """Test get_contents with multiple URLs."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get_contents.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import get_contents

            result = get_contents(urls=["https://example.com", "https://test.com"])
            assert "results" in result

    def test_get_contents_empty_urls(self, mock_api_key):
        """Test ValueError for empty URLs."""
        from mcp_exa._server import get_contents

        with pytest.raises(ValueError, match="URLs cannot be empty"):
            get_contents(urls=[])


class TestAnswer:
    """Tests for answer tool."""

    def test_answer_success(self, mock_api_key, mock_answer_result):
        """Test successful answer."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.answer.return_value = mock_answer_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import answer

            result = answer(query="What is test?")
            assert "answer" in result
            assert result["answer"] == "Test answer"

    def test_answer_empty_query(self, mock_api_key):
        """Test ValueError for empty query."""
        from mcp_exa._server import answer

        with pytest.raises(ValueError, match="Query cannot be empty"):
            answer(query="")


class TestResearchCreate:
    """Tests for research_create tool."""

    def test_research_create_success(self, mock_api_key, mock_research_result):
        """Test successful research create."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.create.return_value = mock_research_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_create

            result = research_create(instructions="Test research")
            assert "research_id" in result
            assert result["research_id"] == "test-123"

    def test_research_create_empty_instructions(self, mock_api_key):
        """Test ValueError for empty instructions."""
        from mcp_exa._server import research_create

        with pytest.raises(ValueError, match="Instructions cannot be empty"):
            research_create(instructions="")


class TestResearchGet:
    """Tests for research_get tool."""

    def test_research_get_success(self, mock_api_key, mock_research_result):
        """Test successful research get."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.get.return_value = mock_research_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_get

            result = research_get(research_id="test-123")
            assert result["research_id"] == "test-123"
            assert result["status"] == "completed"

    def test_research_get_empty_id(self, mock_api_key):
        """Test ValueError for empty research ID."""
        from mcp_exa._server import research_get

        with pytest.raises(ValueError, match="Research ID cannot be empty"):
            research_get(research_id="")


class TestResearchPollUntilFinished:
    """Tests for research_poll_until_finished tool."""

    def test_poll_success(self, mock_api_key, mock_research_result):
        """Test successful poll."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.poll_until_finished.return_value = mock_research_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_poll_until_finished

            result = research_poll_until_finished(research_id="test-123")
            assert result["status"] == "completed"


class TestResearchList:
    """Tests for research_list tool."""

    def test_research_list_success(self, mock_api_key):
        """Test successful research list."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_response = MagicMock()
            mock_response.data = []
            mock_response.has_more = False
            mock_response.next_cursor = None
            mock_client = MagicMock()
            mock_client.research.list.return_value = mock_response
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_list

            result = research_list()
            assert "data" in result
            assert result["has_more"] is False

    def test_research_list_with_pagination(self, mock_api_key):
        """Test research list with cursor and limit."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_response = MagicMock()
            mock_response.data = []
            mock_response.has_more = True
            mock_response.next_cursor = "next-cursor"
            mock_client = MagicMock()
            mock_client.research.list.return_value = mock_response
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_list

            result = research_list(cursor="cursor", limit=10)
            assert result["has_more"] is True
            assert result["next_cursor"] == "next-cursor"


class TestStreamAnswer:
    """Tests for stream_answer tool."""

    @pytest.mark.asyncio
    async def test_stream_answer_success(self, mock_api_key):
        """Test successful stream_answer."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()

            mock_chunk = MagicMock()
            mock_chunk.content = "Test"
            mock_chunk.citations = []

            async def mock_stream(*args, **kwargs):
                yield mock_chunk

            mock_client.stream_answer.return_value = mock_stream()
            mock_get_client.return_value = mock_client

            from mcp_exa._server import stream_answer

            result = await stream_answer(query="test query")
            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_stream_answer_empty_query(self, mock_api_key):
        """Test ValueError for empty query in stream_answer."""
        from mcp_exa._server import stream_answer

        with pytest.raises(ValueError, match="Query cannot be empty"):
            await stream_answer(query="")


class TestSearchWithAllOptions:
    """Tests for search with various options."""

    def test_search_with_category(self, mock_api_key, mock_exa_results):
        """Test search with category option."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(query="test", category="news")
            assert "results" in result

    def test_search_with_date_filters(self, mock_api_key, mock_exa_results):
        """Test search with date filters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(
                query="test",
                start_published_date="2024-01-01",
                end_published_date="2024-12-31",
            )
            assert "results" in result

    def test_search_with_exclude_text(self, mock_api_key, mock_exa_results):
        """Test search with exclude text."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(query="test", exclude_text=["spam"])
            assert "results" in result

    def test_search_error_handling(self, mock_api_key):
        """Test search error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(query="test")
            assert "error" in result


class TestFindSimilarWithOptions:
    """Tests for find_similar with various options."""

    def test_find_similar_with_exclude(self, mock_api_key, mock_exa_results):
        """Test find_similar with exclude source domain."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.find_similar.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import find_similar

            result = find_similar(url="https://example.com", exclude_source_domain=True)
            assert "results" in result

    def test_find_similar_with_category(self, mock_api_key, mock_exa_results):
        """Test find_similar with category."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.find_similar.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import find_similar

            result = find_similar(url="https://example.com", category="github")
            assert "results" in result


class TestMain:
    """Tests for __main__.py"""

    def test_main_calls_mcp_run(self):
        """Test that main calls mcp.run()."""
        with patch("mcp_exa.__main__.mcp") as mock_mcp:
            from mcp_exa.__main__ import main

            main()
            mock_mcp.run.assert_called_once()

    def test_main_returns_zero(self):
        """Test that main returns 0."""
        with patch("mcp_exa.__main__.mcp"):
            from mcp_exa.__main__ import main

            result = main()
            assert result == 0


class TestAdditionalCoverage:
    """Additional tests for coverage."""

    def test_search_with_all_params(self, mock_api_key, mock_exa_results):
        """Test search with many parameters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.search.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import search

            result = search(
                query="test",
                num_results=10,
                include_domains=["example.com"],
                exclude_domains=["spam.com"],
                start_crawl_date="2024-01-01",
                end_crawl_date="2024-12-31",
                start_published_date="2024-01-01",
                end_published_date="2024-12-31",
                include_text=["python"],
                exclude_text=["advertisement"],
                type="deep",
                category="news",
                flags=["experimental"],
                moderation=True,
                user_location="US",
                additional_queries=["query1", "query2"],
                output_schema={"type": "object"},
            )
            assert "results" in result

    def test_find_similar_with_all_params(self, mock_api_key, mock_exa_results):
        """Test find_similar with many parameters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.find_similar.return_value = mock_exa_results
            mock_get_client.return_value = mock_client

            from mcp_exa._server import find_similar

            result = find_similar(
                url="https://example.com",
                num_results=10,
                include_domains=["example.com"],
                exclude_domains=["spam.com"],
                start_crawl_date="2024-01-01",
                end_crawl_date="2024-12-31",
                start_published_date="2024-01-01",
                end_published_date="2024-12-31",
                include_text=["python"],
                exclude_text=["advertisement"],
                exclude_source_domain=True,
                category="github",
                flags=["experimental"],
            )
            assert "results" in result

    def test_answer_with_all_params(self, mock_api_key, mock_answer_result):
        """Test answer with many parameters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.answer.return_value = mock_answer_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import answer

            result = answer(
                query="test",
                text=True,
                system_prompt="You are helpful",
                model="exa",
                output_schema={"type": "object"},
                user_location="US",
            )
            assert "answer" in result

    def test_research_create_with_all_params(self, mock_api_key, mock_research_result):
        """Test research_create with all parameters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.create.return_value = mock_research_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_create

            result = research_create(
                instructions="Test",
                model="exa-research",
                output_schema={"type": "object"},
            )
            assert "research_id" in result

    def test_research_get_with_all_params(self, mock_api_key, mock_research_result):
        """Test research_get with all parameters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.get.return_value = mock_research_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_get

            result = research_get(
                research_id="test-123",
                events=True,
            )
            assert "research_id" in result

    def test_research_poll_with_all_params(self, mock_api_key, mock_research_result):
        """Test research_poll_until_finished with all parameters."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.poll_until_finished.return_value = mock_research_result
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_poll_until_finished

            result = research_poll_until_finished(
                research_id="test-123",
                poll_interval=500,
                timeout_ms=300000,
                events=True,
            )
            assert "research_id" in result

    def test_research_list_error(self, mock_api_key):
        """Test research_list error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.list.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_list

            result = research_list()
            assert "error" in result

    def test_get_contents_error(self, mock_api_key):
        """Test get_contents error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get_contents.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            from mcp_exa._server import get_contents

            result = get_contents(urls="https://example.com")
            assert "error" in result

    def test_answer_error(self, mock_api_key):
        """Test answer error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.answer.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            from mcp_exa._server import answer

            result = answer(query="test")
            assert "error" in result

    def test_research_create_error(self, mock_api_key):
        """Test research_create error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.create.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_create

            result = research_create(instructions="test")
            assert "error" in result

    def test_research_get_error(self, mock_api_key):
        """Test research_get error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.get.side_effect = Exception("API Error")
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_get

            result = research_get(research_id="test")
            assert "error" in result

    def test_research_poll_error(self, mock_api_key):
        """Test research_poll error handling."""
        with patch("mcp_exa._server.get_exa_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.research.poll_until_finished.side_effect = Exception(
                "API Error"
            )
            mock_get_client.return_value = mock_client

            from mcp_exa._server import research_poll_until_finished

            result = research_poll_until_finished(research_id="test")
            assert "error" in result
