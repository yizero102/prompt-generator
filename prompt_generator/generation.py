"""Core prompt generation logic extracted from the notebook workflow."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, List, Optional, Sequence, Tuple

from .anthropic_client import LLMClient, ensure_llm_client
from .metaprompt_text import METAPROMPT, REMOVE_FLOATING_VARIABLES_PROMPT


def pretty_print(message: str, line_length: int = 100) -> str:
    """Return the message with simple word wrapping for readability."""

    paragraphs = re.split(r"\n\n+", message.strip())
    wrapped_paragraphs: List[str] = []
    for paragraph in paragraphs:
        lines = re.findall(rf".{{1,{line_length}}}(?:\s+|$)", paragraph.strip())
        wrapped_paragraphs.append("\n".join(line.strip() for line in lines if line.strip()))
    return "\n\n".join(wrapped_paragraphs)


@dataclass
class GeneratedPrompt:
    """Container describing a generated prompt template."""

    task: str
    requested_variables: List[str]
    raw_prompt_template: str
    final_prompt_template: str
    identified_variables: List[str]
    metaprompt_response: str
    metaprompt_thinking: str
    floating_variables: List[str] = field(default_factory=list)
    floating_variable_analysis: Optional[str] = None

    @property
    def prompt(self) -> str:
        """Expose the final prompt template after floating-variable cleanup."""

        return self.final_prompt_template


def _collect_openai_blocks(message: Any, block_type: str) -> List[str]:
    blocks: List[str] = []
    choices = getattr(message, "choices", None) or []
    for choice in choices:
        chat_message = getattr(choice, "message", None)
        if chat_message is None:
            continue

        if block_type == "thinking":
            reasoning_details = getattr(chat_message, "reasoning_details", None)
            if reasoning_details:
                for detail in reasoning_details:
                    if isinstance(detail, dict):
                        text = detail.get("text")
                    else:
                        text = getattr(detail, "text", None)
                    if text:
                        blocks.append(text)
            else:
                reasoning = getattr(chat_message, "reasoning", None)
                if isinstance(reasoning, str) and reasoning:
                    blocks.append(reasoning)
                elif isinstance(reasoning, list):
                    for segment in reasoning:
                        if isinstance(segment, dict):
                            text = segment.get("text")
                        else:
                            text = getattr(segment, "text", None)
                        if text:
                            blocks.append(text)
            continue

        content = getattr(chat_message, "content", None)
        if not content:
            continue
        if isinstance(content, str):
            blocks.append(content)
        elif isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text")
                else:
                    text = getattr(part, "text", None)
                if text:
                    blocks.append(text)
        else:
            text = getattr(content, "text", None)
            if text:
                blocks.append(text)
    return blocks


def _collect_content_blocks(message: Any, block_type: str, provider: str) -> List[str]:
    if provider == "anthropic":
        blocks: List[str] = []
        for block in getattr(message, "content", []) or []:
            if getattr(block, "type", None) != block_type:
                continue
            if block_type == "thinking":
                value = getattr(block, "thinking", None)
            else:
                value = getattr(block, "text", None)
            if value:
                blocks.append(value)
        return blocks

    if provider == "openai":
        return _collect_openai_blocks(message, block_type)

    raise ValueError(f"Unsupported provider for content extraction: {provider!r}")


def _extract_between_tags(tag: str, string: str, strip: bool = False) -> List[str]:
    pattern = rf"<{tag}>(.+?)</{tag}>"
    matches = re.findall(pattern, string, flags=re.DOTALL | re.IGNORECASE)
    if strip:
        matches = [match.strip() for match in matches]
    return matches


def _remove_empty_tags(text: str) -> str:
    return re.sub(r"\n<(\w+)>\s*</\1>\n", "", text, flags=re.DOTALL)


def _strip_last_sentence(text: str) -> str:
    sentences = text.split(". ")
    if sentences and sentences[-1].startswith("Let me know"):
        sentences = sentences[:-1]
        result = ". ".join(sentences)
        if result and not result.endswith('.'):
            result += "."
        return result
    return text


def _extract_prompt(metaprompt_response: str) -> str:
    instructions = _extract_between_tags("Instructions", metaprompt_response)[0]
    head = instructions[:1000]
    tail = instructions[1000:]
    cleaned_tail = _strip_last_sentence(_remove_empty_tags(_remove_empty_tags(tail).strip()).strip())
    return head + cleaned_tail


def _extract_variables(prompt: str) -> List[str]:
    pattern = r"\{([^}]+)\}"
    return sorted(set(re.findall(pattern, prompt)))


def _find_free_floating_variables(prompt: str) -> List[str]:
    variable_usages = re.findall(r"\{\$[A-Z0-9_]+\}", prompt)
    free_floating_variables: List[str] = []

    for variable in variable_usages:
        preceding_text = prompt[: prompt.index(variable)]
        open_tags = set()
        i = 0
        while i < len(preceding_text):
            if preceding_text[i] == "<":
                if i + 1 < len(preceding_text) and preceding_text[i + 1] == "/":
                    closing_tag = preceding_text[i + 2 :].split(">", 1)[0]
                    open_tags.discard(closing_tag)
                    i += len(closing_tag) + 3
                else:
                    opening_tag = preceding_text[i + 1 :].split(">", 1)[0]
                    open_tags.add(opening_tag)
                    i += len(opening_tag) + 2
            else:
                i += 1
        if not open_tags:
            free_floating_variables.append(variable)
    return free_floating_variables


def _remove_inapt_floating_variables(prompt: str, llm_client: LLMClient) -> Tuple[Optional[str], str]:
    message = llm_client.create_message(
        messages=[
            {
                "role": "user",
                "content": REMOVE_FLOATING_VARIABLES_PROMPT.replace("{$PROMPT}", prompt),
            }
        ],
        max_tokens=4096,
        temperature=0,
    )

    text_blocks = _collect_content_blocks(message, "text", llm_client.provider)
    response_text = "\n\n".join(text_blocks)
    rewritten = _extract_between_tags("rewritten_prompt", response_text)[0]
    normalized = rewritten.strip().lower()
    if normalized in {"no changes.", "no changes", "no change", "no edits needed", "no edit needed"}:
        return None, response_text
    if normalized == prompt.strip().lower():
        return None, response_text
    return rewritten, response_text


def generate_prompt_template(
    task: str,
    requested_variables: Optional[Sequence[str]] = None,
    *,
    client: Optional[Any] = None,
    model_name: Optional[str] = None,
) -> GeneratedPrompt:
    """Generate a prompt template for the provided task."""

    llm_client = ensure_llm_client(client, model_name)

    normalized_variables = [var.upper() for var in (requested_variables or [])]
    variable_string = ""
    for variable in normalized_variables:
        variable_string += f"\n{{$" + variable + "}}"

    prompt = METAPROMPT.replace("{{TASK}}", task)
    assistant_partial = "<Inputs>"
    if variable_string:
        assistant_partial += variable_string
    assistant_partial += "\n</Inputs>\n<Instructions Structure>"

    message = llm_client.create_message(
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_partial},
        ],
        max_tokens=4096,
        temperature=0,
    )

    thinking_blocks = _collect_content_blocks(message, "thinking", llm_client.provider)
    text_blocks = _collect_content_blocks(message, "text", llm_client.provider)
    metaprompt_thinking = "\n\n".join(thinking_blocks)
    metaprompt_response = "\n\n".join(text_blocks)

    raw_prompt_template = _extract_prompt(metaprompt_response)
    final_prompt_template = raw_prompt_template
    identified_variables = _extract_variables(final_prompt_template)
    floating_variables = _find_free_floating_variables(final_prompt_template)

    floating_analysis = None
    if floating_variables:
        rewritten_prompt, floating_analysis = _remove_inapt_floating_variables(
            final_prompt_template, llm_client
        )
        if rewritten_prompt:
            final_prompt_template = rewritten_prompt
            identified_variables = _extract_variables(final_prompt_template)

    return GeneratedPrompt(
        task=task,
        requested_variables=normalized_variables,
        raw_prompt_template=raw_prompt_template,
        final_prompt_template=final_prompt_template,
        identified_variables=identified_variables,
        metaprompt_response=metaprompt_response,
        metaprompt_thinking=metaprompt_thinking,
        floating_variables=floating_variables,
        floating_variable_analysis=floating_analysis,
    )
