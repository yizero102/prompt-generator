#!/usr/bin/env python3
"""Execute test cases for generated prompt templates."""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Sequence

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import pretty_print, run_prompt_test

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = PROJECT_ROOT / "generated_prompts"
TEST_OUTPUT_DIR = PROMPT_DIR / "tests"
DEFAULT_TEST_CASES = PROJECT_ROOT / "data" / "test_cases.json"

_TOOL_CALL_PATTERN = re.compile(r"<tool_call\b[^>]*>.*?</tool_call>", re.DOTALL)
FORMAT_RETRY_LIMIT = 2


def load_prompt(slug: str) -> dict:
    path = PROMPT_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found for slug '{slug}' at {path}")
    return json.loads(path.read_text())


def load_test_cases(path: Path) -> Dict[str, List[dict]]:
    return json.loads(path.read_text())


def save_test_result(slug: str, name: str, payload: dict) -> None:
    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}__{name}.json"
    (TEST_OUTPUT_DIR / filename).write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=DEFAULT_TEST_CASES,
        help="Path to the JSON file containing prompt test cases.",
    )
    return parser.parse_args(argv)


def _indent(text: str, level: int = 0, indent: str = "  ") -> str:
    dedented = textwrap.dedent(text).strip()
    if not dedented:
        return ""
    return "\n".join(f"{indent * level}{line}" if line else "" for line in dedented.splitlines())


def _wrap_cdata(text: str) -> str:
    if not text:
        return "<![CDATA[]]>"
    return "<![CDATA[" + text.replace("]]>", "]]]><![CDATA[>") + "]]>"


TEXTUAL_FIELD_TAGS = (
    "summary",
    "handoff",
    "success_criteria",
    "status",
    "message",
    "audience",
    "open_questions",
    "next_action",
)


def _preprocess_tool_xml(tool_xml: str) -> str:
    for tag in TEXTUAL_FIELD_TAGS:
        pattern = re.compile(rf"<{tag}>(.*?)</{tag}>", re.DOTALL)

        def _wrap(match) -> str:
            content = match.group(1)
            if "<![CDATA[" in content:
                return match.group(0)
            return f"<{tag}>{_wrap_cdata(content)}</{tag}>"

        tool_xml = pattern.sub(_wrap, tool_xml)
    return tool_xml


def _render_history(initial_turns: List[str], dynamic_turns: List[str]) -> str:
    blocks: List[str] = []
    for block in initial_turns + dynamic_turns:
        cleaned = block.strip()
        if cleaned:
            blocks.append(_indent(cleaned, 1))
    if not blocks:
        return "<history />"
    return "<history>\n" + "\n".join(blocks) + "\n</history>"


def _sanitize_for_format(value: str) -> str:
    return value.replace("{", "{{").replace("}", "}}")


def _render_observation(entry, context: Dict[str, str]) -> str:
    if entry is None:
        return "<observation role=\"system\">No scripted observation available.</observation>"
    if isinstance(entry, str):
        template = entry
    else:
        template = entry.get("text") or entry.get("template")
        if template is None:
            return "<observation role=\"system\">No scripted observation available.</observation>"
    safe_context = {key: _sanitize_for_format(str(value)) for key, value in context.items()}
    try:
        return template.format(**safe_context)
    except KeyError as exc:  # pragma: no cover - defensive branch
        missing = exc.args[0]
        raise KeyError(f"Observation template expected value for '{missing}'.") from exc


def _parse_tool_call(output: str) -> dict:
    cleaned = output.strip()
    matches = list(_TOOL_CALL_PATTERN.finditer(cleaned))
    if not matches:
        raise ValueError("Response must contain a <tool_call> element.")
    if len(matches) > 1:
        raise ValueError("Response must contain exactly one <tool_call> element.")

    match = matches[0]
    prefix = cleaned[: match.start()].strip()
    suffix = cleaned[match.end() :].strip()

    if prefix:
        raise ValueError("Response must not contain text before the <tool_call> element.")
    if suffix:
        if "<tool_call" in suffix:
            raise ValueError("Response must contain exactly one <tool_call> element.")
        normalized_suffix = suffix.replace("</tool_call>", "").strip()
        if normalized_suffix:
            raise ValueError("Response must not contain text after the </tool_call> element.")

    tool_xml = match.group(0).strip()
    sanitized_tool_xml = _preprocess_tool_xml(tool_xml)
    try:
        element = ET.fromstring(sanitized_tool_xml)
    except ET.ParseError as err:
        raise ValueError(f"Tool call XML not well formed: {err}") from err
    tool_name_attr = element.attrib.get("name")
    if not tool_name_attr:
        raise ValueError("tool_call element is missing the required 'name' attribute.")

    fields: Dict[str, str] = {}
    arguments: Dict[str, str] = {}
    for child in list(element):
        if child.tag == "arguments":
            for arg in list(child):
                key = arg.tag
                value = (arg.text or "").strip()
                arguments[key] = value
        else:
            if list(child):
                fields[child.tag] = ET.tostring(child, encoding="unicode")
            else:
                fields[child.tag] = (child.text or "").strip()

    explicit_user_tool = fields.get("tool_name", "").strip()
    return {
        "name": tool_name_attr,
        "xml": sanitized_tool_xml,
        "fields": fields,
        "arguments": arguments,
        "tool_name": explicit_user_tool,
    }


def _build_observation(tool_call: dict, multi_config: dict, turn_index: int) -> str:
    observations = multi_config.get("simulated_observations", {})
    entry = observations.get(tool_call["name"])

    if tool_call["name"] == "call_user_tool":
        user_map = observations.get("call_user_tool", {})
        entry = user_map.get(tool_call["tool_name"]) or user_map.get("default") or entry
    elif entry is None:
        entry = observations.get("default")

    context: Dict[str, str] = {
        "turn": str(turn_index),
        "agent_tool": tool_call["name"],
        "tool_name": tool_call["tool_name"] or tool_call["name"],
    }
    context.update({k: v for k, v in tool_call["fields"].items() if isinstance(v, str)})
    context.update({k: v for k, v in tool_call["arguments"].items()})
    return _render_observation(entry, context)


def _render_turn_entry(turn_index: int, tool_call_xml: str, observation: str) -> str:
    tool_block = _indent(tool_call_xml, 3)
    observation_block = _indent(observation, 3)
    return "\n".join(
        [
            f"  <turn index=\"{turn_index}\">",
            "    <agent>",
            tool_block,
            "    </agent>",
            "    <environment>",
            observation_block,
            "    </environment>",
            "  </turn>",
        ]
    )


def _render_format_violation(turn_index: int, raw_output: str, feedback: str, attempt: int) -> str:
    invalid_block = _indent(
        f"<invalid_output>{_wrap_cdata(raw_output)}</invalid_output>",
        3,
    )
    feedback_block = _indent(feedback, 3)
    return "\n".join(
        [
            f"  <turn index=\"{turn_index}\" type=\"format_violation\" attempt=\"{attempt}\">",
            "    <agent>",
            invalid_block,
            "    </agent>",
            "    <environment>",
            feedback_block,
            "    </environment>",
            "  </turn>",
        ]
    )


def _validate_multi_turn_requirements(requirements: dict, conversation: List[dict], used_user_tools: List[str], finish_call: dict) -> None:
    if not requirements:
        return

    if requirements.get("plan_first"):
        first_tool_entry = next((entry for entry in conversation if entry.get("tool_call")), None)
        if not first_tool_entry or first_tool_entry["tool_call"]["name"] != "plan":
            raise RuntimeError("The first turn must invoke the plan tool.")

    required_tools = requirements.get("must_call_user_tools", [])
    missing = [tool for tool in required_tools if tool not in used_user_tools]
    if missing:
        raise RuntimeError(
            "The conversation never invoked the required user tools: " + ", ".join(sorted(missing))
        )

    summary_keywords = requirements.get("finish_summary_keywords", [])
    if summary_keywords:
        summary = ""
        if finish_call:
            summary = finish_call["fields"].get("summary", "")
        summary_lower = summary.lower()
        missing_keywords = [kw for kw in summary_keywords if kw.lower() not in summary_lower]
        if missing_keywords:
            raise RuntimeError(
                "Finish summary missing required keywords: " + ", ".join(sorted(missing_keywords))
            )


def _run_multi_turn_case(slug: str, template: str, case: dict) -> dict:
    multi = case["multi_turn"]
    history_var = multi.get("history_variable", "$HISTORY")
    max_turns = multi.get("max_turns", 6)
    finish_tool = multi.get("finish_tool", "finish")
    per_turn_max_tokens = multi.get("per_turn_max_tokens") or case.get("max_tokens") or 512
    initial_turns = list(multi.get("initial_turns", []))

    history_entries: List[str] = []
    conversation_log: List[dict] = []
    used_user_tools: List[str] = []
    finish_call = None

    for turn_index in range(1, max_turns + 1):
        format_retries = 0

        while True:
            history_string = _render_history(initial_turns, history_entries)
            variables = dict(case.get("variables", {}))
            variables[history_var] = history_string

            result = run_prompt_test(template, variables, max_tokens=per_turn_max_tokens)
            raw_output = result.output.strip()
            print("    raw model output:")
            print(pretty_print(raw_output) if raw_output else "(empty)")

            try:
                tool_call = _parse_tool_call(raw_output)
            except ValueError as err:
                format_retries += 1
                if format_retries >= FORMAT_RETRY_LIMIT:
                    raise RuntimeError(
                        f"Repeated format violation on turn {turn_index}: {err}"
                    ) from err

                feedback = (
                    "<observation role=\"system\">FORMAT ERROR: "
                    + str(err)
                    + " Respond with exactly one <tool_call> element and no surrounding narration.</observation>"
                )
                print("    format violation:", err)
                history_entries.append(
                    _render_format_violation(turn_index, raw_output, feedback, format_retries)
                )
                conversation_log.append(
                    {
                        "turn": turn_index,
                        "history_before": history_string,
                        "prompt_with_variables": result.prompt_with_variables,
                        "thinking": result.thinking,
                        "output": result.output,
                        "tool_call": None,
                        "observation": feedback,
                        "format_error": str(err),
                    }
                )
                continue

            successful_history_string = history_string
            break

        print(f"  Turn {turn_index}: tool -> {tool_call['name']}")
        if tool_call["name"] == "call_user_tool":
            if not tool_call["tool_name"]:
                raise RuntimeError("call_user_tool responses must include a <tool_name> element.")
            used_user_tools.append(tool_call["tool_name"])
            print(
                "    user tool:",
                tool_call["tool_name"],
                "arguments:",
                tool_call["arguments"],
            )

        if result.thinking:
            print("    model thinking:")
            print(pretty_print(result.thinking))

        observation = _build_observation(tool_call, multi, turn_index)
        print("    observation returned:")
        print(pretty_print(observation))

        history_entries.append(_render_turn_entry(turn_index, tool_call["xml"], observation))
        conversation_log.append(
            {
                "turn": turn_index,
                "history_before": successful_history_string,
                "prompt_with_variables": result.prompt_with_variables,
                "thinking": result.thinking,
                "output": result.output,
                "tool_call": tool_call,
                "observation": observation,
            }
        )

        if tool_call["name"] == finish_tool:
            finish_call = tool_call
            break

    if finish_call is None:
        raise RuntimeError(f"Finish tool '{finish_tool}' was not called within {max_turns} turns.")

    _validate_multi_turn_requirements(multi.get("requirements", {}), conversation_log, used_user_tools, finish_call)

    return {
        "conversation": conversation_log,
        "final_history": _render_history(initial_turns, history_entries),
        "used_user_tools": used_user_tools,
        "finish_call": finish_call,
    }


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])
    test_cases = load_test_cases(args.cases)

    for slug, cases in test_cases.items():
        prompt_payload = load_prompt(slug)
        template = prompt_payload["final_prompt_template"]
        print("=" * 80)
        print(f"Running tests for {slug} ({prompt_payload['task']})")
        for case in cases:
            name = case.get("name", "default")
            print(f"\n- Test case: {name}")

            if "multi_turn" in case:
                multi_turn_result = _run_multi_turn_case(slug, template, case)
                save_test_result(
                    slug,
                    name,
                    {
                        "slug": slug,
                        "task": prompt_payload["task"],
                        "test_case_name": name,
                        "variables": case.get("variables", {}),
                        "conversation": multi_turn_result["conversation"],
                        "final_history": multi_turn_result["final_history"],
                        "used_user_tools": multi_turn_result["used_user_tools"],
                        "finish_call": multi_turn_result["finish_call"],
                        "requirements": case.get("multi_turn", {}).get("requirements", {}),
                        "passes_requirements": True,
                    },
                )
            else:
                variables = case.get("variables", {})
                max_tokens = case.get("max_tokens", 1024)
                result = run_prompt_test(template, variables, max_tokens=max_tokens)
                print("Prompt sent to model:\n")
                print(pretty_print(result.prompt_with_variables))
                if result.thinking:
                    print("\nModel thinking:\n")
                    print(pretty_print(result.thinking))
                print("\nModel output:\n")
                print(pretty_print(result.output))

                save_test_result(
                    slug,
                    name,
                    {
                        "slug": slug,
                        "task": prompt_payload["task"],
                        "test_case_name": name,
                        "variables": variables,
                        "prompt_with_variables": result.prompt_with_variables,
                        "thinking": result.thinking,
                        "output": result.output,
                    },
                )

    print("\nAll prompt tests executed. Outputs saved to", TEST_OUTPUT_DIR)


if __name__ == "__main__":
    main()
