"""Core prompt generation logic extracted from the notebook workflow."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence, Tuple

from anthropic import Anthropic

from .anthropic_client import get_client
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


def _collect_content_blocks(message, block_type: str) -> List[str]:
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


def _remove_inapt_floating_variables(
    prompt: str, client: Anthropic, model_name: str
) -> Tuple[Optional[str], str]:
    message = client.messages.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": REMOVE_FLOATING_VARIABLES_PROMPT.replace("{$PROMPT}", prompt),
            }
        ],
        max_tokens=4096,
        temperature=0,
    )
    text_blocks = _collect_content_blocks(message, "text")
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
    client: Optional[Anthropic] = None,
    model_name: Optional[str] = None,
) -> GeneratedPrompt:
    """Generate a prompt template for the provided task."""

    anthropic_client, resolved_model_name = (
        (client, model_name)
        if client and model_name
        else get_client()
    )
    assert anthropic_client is not None
    assert resolved_model_name is not None

    normalized_variables = [var.upper() for var in (requested_variables or [])]
    variable_string = ""
    for variable in normalized_variables:
        variable_string += f"\n{{$" + variable + "}}"

    prompt = METAPROMPT.replace("{{TASK}}", task)
    assistant_partial = "<Inputs>"
    if variable_string:
        assistant_partial += variable_string
    assistant_partial += "\n</Inputs>\n<Instructions Structure>"

    message = anthropic_client.messages.create(
        model=resolved_model_name,
        max_tokens=4096,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_partial},
        ],
    )

    thinking_blocks = _collect_content_blocks(message, "thinking")
    text_blocks = _collect_content_blocks(message, "text")
    metaprompt_thinking = "\n\n".join(thinking_blocks)
    metaprompt_response = "\n\n".join(text_blocks)

    raw_prompt_template = _extract_prompt(metaprompt_response)
    final_prompt_template = raw_prompt_template
    identified_variables = _extract_variables(final_prompt_template)
    floating_variables = _find_free_floating_variables(final_prompt_template)

    floating_analysis = None
    if floating_variables:
        rewritten_prompt, floating_analysis = _remove_inapt_floating_variables(
            final_prompt_template, anthropic_client, resolved_model_name
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
