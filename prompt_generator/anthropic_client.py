"""LLM client configuration helpers for Anthropic and OpenAI providers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterator, Literal, Optional, Union, cast

if TYPE_CHECKING:  # pragma: no cover - import solely for static type checking
    from anthropic import Anthropic  # pragma: no cover
else:  # pragma: no cover - executed at runtime
    try:
        from anthropic import Anthropic  # type: ignore
    except ImportError as exc:  # pragma: no cover - handled gracefully below
        Anthropic = None  # type: ignore
        _ANTHROPIC_IMPORT_ERROR: Optional[ImportError] = exc
    else:
        _ANTHROPIC_IMPORT_ERROR = None

if TYPE_CHECKING:  # pragma: no cover - import solely for static type checking
    from openai import OpenAI  # pragma: no cover
else:  # pragma: no cover - executed at runtime
    try:
        from openai import OpenAI  # type: ignore
    except ImportError as exc:  # pragma: no cover - handled gracefully below
        OpenAI = None  # type: ignore
        _OPENAI_IMPORT_ERROR: Optional[ImportError] = exc
    else:
        _OPENAI_IMPORT_ERROR = None

Provider = Literal["anthropic", "openai"]


def _normalize_env_value(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _ensure_anthropic_available() -> None:
    if Anthropic is None:
        message = (
            "The Anthropic SDK is not installed. Install it with 'pip install anthropic' "
            "or configure `_LLM_PROVIDER=openai`."
        )
        raise RuntimeError(message) from _ANTHROPIC_IMPORT_ERROR


def _ensure_openai_available() -> None:
    if OpenAI is None:
        message = (
            "The OpenAI SDK is not installed. Install it with 'pip install openai' "
            "or configure `_LLM_PROVIDER=anthropic`."
        )
        raise RuntimeError(message) from _OPENAI_IMPORT_ERROR


@dataclass(frozen=True)
class AnthropicConfig:
    """Container for Anthropic connection settings."""

    api_key: str
    model_name: str
    base_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> "AnthropicConfig":
        """Build a configuration instance using environment variables.

        Expected variables:
        - _ANTHROPIC_API_KEY: required API key
        - _MODEL_NAME: required Anthropic model identifier
        - _ANTHROPIC_BASE_URL: optional custom base URL (defaults to Anthropic API)
        """

        api_key = os.getenv("_ANTHROPIC_API_KEY")
        model_name = os.getenv("_MODEL_NAME")
        base_url = _normalize_env_value(os.getenv("_ANTHROPIC_BASE_URL"))

        if not api_key:
            raise RuntimeError("_ANTHROPIC_API_KEY environment variable is not set.")
        if not model_name:
            raise RuntimeError("_MODEL_NAME environment variable is not set.")

        return cls(api_key=api_key, model_name=model_name, base_url=base_url)

    def create_client(self):  # -> Anthropic:
        """Instantiate an Anthropic client using the stored configuration."""

        _ensure_anthropic_available()
        assert Anthropic is not None  # Placate type checkers
        return Anthropic(api_key=self.api_key, base_url=self.base_url)


@dataclass(frozen=True)
class OpenAIConfig:
    """Container for OpenAI connection settings."""

    api_key: str
    model_name: str
    base_url: Optional[str] = None

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        """Build a configuration instance using environment variables.

        Expected variables:
        - _OPENAI_API_KEY: required API key
        - _MODEL_NAME: required model identifier
        - _OPENAI_BASE_URL: optional custom base URL
        """

        api_key = os.getenv("_OPENAI_API_KEY")
        model_name = os.getenv("_MODEL_NAME")
        base_url = _normalize_env_value(os.getenv("_OPENAI_BASE_URL"))

        if not api_key:
            raise RuntimeError("_OPENAI_API_KEY environment variable is not set.")
        if not model_name:
            raise RuntimeError("_MODEL_NAME environment variable is not set.")

        return cls(api_key=api_key, model_name=model_name, base_url=base_url)

    def create_client(self):  # -> OpenAI:
        """Instantiate an OpenAI client using the stored configuration."""

        _ensure_openai_available()
        assert OpenAI is not None  # Placate type checkers
        return OpenAI(api_key=self.api_key, base_url=self.base_url)


@dataclass(frozen=True)
class LLMClient:
    """Wrapper that normalizes chat completion calls across providers."""

    client: Any
    model_name: str
    provider: Provider

    def __iter__(self) -> Iterator[Any]:
        """Allow tuple-style unpacking (client, model_name)."""

        yield self.client
        yield self.model_name

    @classmethod
    def from_components(
        cls,
        client: Any,
        model_name: str,
        provider: Provider,
    ) -> "LLMClient":
        return cls(client=client, model_name=model_name, provider=provider)

    def create_message(self, *, messages, extra_body=None, **kwargs):
        """Dispatch a chat completion request for the configured provider."""

        if self.provider == "anthropic":
            return self.client.messages.create(
                model=self.model_name,
                messages=messages,
                **kwargs,
            )

        openai_kwargs = dict(kwargs)
        if extra_body is None:
            extra_body = {"reasoning_split": True}
        return self.client.chat.completions.create(  # type: ignore[attr-defined]
            model=self.model_name,
            messages=messages,
            extra_body=extra_body,
            **openai_kwargs,
        )


def _normalize_provider(explicit: Optional[str]) -> Provider:
    if explicit:
        candidate = explicit.strip().lower()
    else:
        env_provider = os.getenv("_LLM_PROVIDER")
        if env_provider:
            candidate = env_provider.strip().lower()
        elif os.getenv("_OPENAI_API_KEY"):
            candidate = "openai"
        elif os.getenv("_ANTHROPIC_API_KEY"):
            candidate = "anthropic"
        else:
            raise RuntimeError(
                "No supported LLM provider configured. Set _LLM_PROVIDER, "
                "_OPENAI_API_KEY, or _ANTHROPIC_API_KEY."
            )

    if candidate not in {"anthropic", "openai"}:
        raise RuntimeError(f"Unsupported LLM provider: {candidate!r}")

    return cast(Provider, candidate)


def get_client(
    config: Optional[Union[AnthropicConfig, OpenAIConfig, LLMClient]] = None,
    *,
    provider: Optional[str] = None,
) -> LLMClient:
    """Return an LLM client wrapper and model name for the configured provider."""

    if isinstance(config, LLMClient):
        return config

    resolved_provider = _normalize_provider(provider)

    if resolved_provider == "anthropic":
        if config is None:
            cfg = AnthropicConfig.from_env()
        elif isinstance(config, AnthropicConfig):
            cfg = config
        elif isinstance(config, OpenAIConfig):
            raise TypeError(
                "Received OpenAIConfig while requesting an Anthropic client."
            )
        else:
            raise TypeError(
                "Unsupported configuration type for Anthropic provider: "
                f"{type(config)!r}"
            )
        client = cfg.create_client()
        return LLMClient.from_components(client, cfg.model_name, "anthropic")

    if config is None:
        cfg = OpenAIConfig.from_env()
    elif isinstance(config, OpenAIConfig):
        cfg = config
    elif isinstance(config, AnthropicConfig):
        raise TypeError(
            "Received AnthropicConfig while requesting an OpenAI client."
        )
    else:
        raise TypeError(
            "Unsupported configuration type for OpenAI provider: "
            f"{type(config)!r}"
        )

    client = cfg.create_client()
    return LLMClient.from_components(client, cfg.model_name, "openai")


def ensure_llm_client(
    client: Optional[Any] = None,
    model_name: Optional[str] = None,
    *,
    provider: Optional[str] = None,
) -> LLMClient:
    """Normalize various client inputs into an ``LLMClient`` instance."""

    if isinstance(client, LLMClient):
        return client

    if client is None and model_name is None:
        return get_client(provider=provider)

    if client is None or model_name is None:
        raise ValueError(
            "Both 'client' and 'model_name' must be provided when supplying a raw SDK client."
        )

    detected_provider: Optional[str] = None
    if Anthropic is not None and isinstance(client, Anthropic):
        detected_provider = "anthropic"
    elif OpenAI is not None and isinstance(client, OpenAI):
        detected_provider = "openai"

    target_provider = provider or detected_provider
    if not target_provider:
        raise TypeError(
            "Unsupported client type. Provide an Anthropic/OpenAI client or specify 'provider'."
        )

    resolved_provider = _normalize_provider(target_provider)
    if resolved_provider == "openai":
        _ensure_openai_available()
    elif resolved_provider == "anthropic":
        _ensure_anthropic_available()

    return LLMClient.from_components(client, model_name, resolved_provider)
