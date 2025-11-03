#!/usr/bin/env python3
"""Quick health check to confirm the Anthropic client is working."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import get_client
from prompt_generator.generation import pretty_print


def main() -> None:
    client, model_name = get_client()
    message = client.messages.create(
        model=model_name,
        max_tokens=256,
        system="You are a helpful assistant.",
        messages=[{"role": "user", "content": "Hi"}],
    )

    thinking = "\n\n".join(
        block.thinking
        for block in message.content
        if getattr(block, "type", None) == "thinking" and getattr(block, "thinking", None)
    )
    output = "\n\n".join(
        block.text
        for block in message.content
        if getattr(block, "type", None) == "text" and getattr(block, "text", None)
    )

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
