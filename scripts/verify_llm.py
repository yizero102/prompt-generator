#!/usr/bin/env python3
"""Quick health check to confirm the configured LLM client is working."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import get_client  # noqa: E402
from prompt_generator.generation import pretty_print, _collect_content_blocks  # noqa: E402


def main() -> None:
    llm_client = get_client()
    message = llm_client.create_message(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hi"},
        ],
        max_tokens=256,
        temperature=0,
    )

    thinking_blocks = _collect_content_blocks(message, "thinking", llm_client.provider)
    output_blocks = _collect_content_blocks(message, "text", llm_client.provider)

    thinking = "\n\n".join(thinking_blocks)
    output = "\n\n".join(output_blocks)

    if thinking:
        print("Thinking:\n")
        print(pretty_print(thinking))
        print("\n" + "-" * 80 + "\n")

    if output:
        print("Response:\n")
        print(pretty_print(output))
    else:
        print("No text response returned from the model.")


if __name__ == "__main__":
    main()
