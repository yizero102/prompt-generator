from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator.anthropic_client import LLMClient, ensure_llm_client, get_client
from prompt_generator.generation import _collect_content_blocks


@pytest.fixture(autouse=True)
def clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure provider detection starts from a clean slate for each test."""

    for key in (
        "_LLM_PROVIDER",
        "_OPENAI_API_KEY",
        "_OPENAI_BASE_URL",
        "_ANTHROPIC_API_KEY",
        "_ANTHROPIC_BASE_URL",
        "_MODEL_NAME",
    ):
        monkeypatch.delenv(key, raising=False)


def test_get_client_returns_openai_when_openai_env_present(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("_OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("_MODEL_NAME", "gpt-test")
    monkeypatch.setenv("_OPENAI_BASE_URL", "https://example.com")

    openai_mock = MagicMock()
    monkeypatch.setattr("prompt_generator.anthropic_client.OpenAI", openai_mock)

    llm_client = get_client()

    openai_mock.assert_called_once_with(api_key="sk-test", base_url="https://example.com")
    assert llm_client.provider == "openai"
    assert llm_client.model_name == "gpt-test"
    assert llm_client.client is openai_mock.return_value


def test_llm_client_openai_create_message_adds_reasoning_split() -> None:
    openai_client = MagicMock()
    llm_client = LLMClient.from_components(openai_client, "gpt-test", "openai")

    messages = [{"role": "user", "content": "hello"}]
    result = llm_client.create_message(messages=messages, max_tokens=12)

    openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-test",
        messages=messages,
        extra_body={"reasoning_split": True},
        max_tokens=12,
    )
    assert result is openai_client.chat.completions.create.return_value


def test_collect_content_blocks_openai_handles_reasoning_details() -> None:
    message = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content="Hello world",
                    reasoning_details=[{"text": "thinking aloud"}],
                )
            )
        ]
    )

    thinking = _collect_content_blocks(message, "thinking", "openai")
    text = _collect_content_blocks(message, "text", "openai")

    assert thinking == ["thinking aloud"]
    assert text == ["Hello world"]


def test_ensure_llm_client_accepts_raw_openai_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    create_mock = MagicMock(return_value="ok")

    class DummyOpenAI:
        def __init__(self) -> None:
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create_mock))

    dummy_instance = DummyOpenAI()
    monkeypatch.setattr("prompt_generator.anthropic_client.OpenAI", DummyOpenAI)

    llm_client = ensure_llm_client(dummy_instance, "gpt-test", provider="openai")

    assert llm_client.provider == "openai"
    assert llm_client.client is dummy_instance

    response = llm_client.create_message(messages=[], max_tokens=1)

    assert response == "ok"
    create_mock.assert_called_once_with(
        model="gpt-test", messages=[], extra_body={"reasoning_split": True}, max_tokens=1
    )
