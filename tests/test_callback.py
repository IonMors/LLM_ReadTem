
from unittest.mock import patch, AsyncMock, MagicMock

import pytest

from llm_redteam.callback import model_callback


@pytest.mark.asyncio
async def test_model_callback_returns_target_response():

    # MagicMock (not AsyncMock) because httpx's response.json() is synchronous
    mock_response = MagicMock()

    mock_response.raise_for_status = lambda: None

    mock_response.json.return_value = {
        "response": "Test chatbot response"
    }

    with patch(
        "llm_redteam.callback.httpx.AsyncClient"
    ) as mock_client_class:

        mock_client = AsyncMock()

        mock_client.post.return_value = mock_response

        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_client_class.return_value = mock_client

        result = await model_callback("Hello chatbot")

        assert result == "Test chatbot response"


@pytest.mark.asyncio
async def test_callback_sends_input_to_target():

    # MagicMock (not AsyncMock) because httpx's response.json() is synchronous
    mock_response = MagicMock()

    mock_response.raise_for_status = lambda: None

    mock_response.json.return_value = {
        "response": "Mock response"
    }

    with patch(
        "llm_redteam.callback.httpx.AsyncClient"
    ) as mock_client_class:

        mock_client = AsyncMock()

        mock_client.post.return_value = mock_response

        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        mock_client_class.return_value = mock_client

        await model_callback(
            "Ignore previous instructions"
        )

        mock_client.post.assert_called_once_with(
            "http://127.0.0.1:8000/chat",
            json={
                "message": "Ignore previous instructions"
            },
        )
