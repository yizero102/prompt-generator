"""Anthropic client configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

from anthropic import Anthropic


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
        base_url = os.getenv("_ANTHROPIC_BASE_URL")

        if not api_key:
            raise RuntimeError("_ANTHROPIC_API_KEY environment variable is not set.")
        if not model_name:
            raise RuntimeError("_MODEL_NAME environment variable is not set.")

        return cls(api_key=api_key, model_name=model_name, base_url=base_url or None)

    def create_client(self) -> Anthropic:
        """Instantiate an Anthropic client using the stored configuration."""

        return Anthropic(api_key=self.api_key, base_url=self.base_url)


def get_client(config: Optional[AnthropicConfig] = None) -> Tuple[Anthropic, str]:
    """Return an Anthropic client and model name.

    Args:
        config: Optional explicit configuration. When omitted, environment
            variables are used.

    Returns:
        Tuple of (Anthropic client, model name)
    """

    cfg = config or AnthropicConfig.from_env()
    return cfg.create_client(), cfg.model_name
