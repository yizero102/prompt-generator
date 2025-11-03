"""Helpers for executing generated prompt templates against supported LLMs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from .anthropic_client import ensure_llm_client
from .generation import _collect_content_blocks, _extract_variables


@dataclass
class PromptTestResult:
    """Outcome of executing a prompt template with concrete variables."""

    prompt_with_variables: str
    variables: Dict[str, str]
    thinking: str
    output: str
    raw_response: str


def _fill_template(template: str, variables: Mapping[str, str]) -> str:
    prompt = template
    for name, value in variables.items():
        variants = {name}
        if name.startswith("$"):
            variants.add(name[1:])
        else:
            variants.add("$" + name)
        for variant in variants:
            prompt = prompt.replace("{" + variant + "}", value)
    return prompt


def _assert_all_variables_filled(template: str, filled_prompt: str) -> None:
    missing = _extract_variables(filled_prompt)
    if missing:
        raise ValueError(
            "Some variables were not replaced in the prompt: " + ", ".join(sorted(missing))
        )


def run_prompt_test(
    template: str,
    variables: Mapping[str, str],
    *,
    client: Optional[Any] = None,
    model_name: Optional[str] = None,
    max_tokens: int = 1024,
) -> PromptTestResult:
    """Execute a prompt template against the configured LLM provider."""

    llm_client = ensure_llm_client(client, model_name)

    filled_prompt = _fill_template(template, variables)
    _assert_all_variables_filled(template, filled_prompt)

    message = llm_client.create_message(
        messages=[{"role": "user", "content": filled_prompt}],
        max_tokens=max_tokens,
    )

    thinking_blocks = _collect_content_blocks(message, "thinking", llm_client.provider)
    text_blocks = _collect_content_blocks(message, "text", llm_client.provider)

    thinking = "\n\n".join(thinking_blocks)
    output_text = "\n\n".join(text_blocks)
    raw_response = thinking + ("\n\n" if thinking and output_text else "") + output_text

    return PromptTestResult(
        prompt_with_variables=filled_prompt,
        variables=dict(variables),
        thinking=thinking,
        output=output_text,
        raw_response=raw_response,
    )
