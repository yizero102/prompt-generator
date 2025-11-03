#!/usr/bin/env python3
"""Execute test cases for generated prompt templates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import pretty_print, run_prompt_test

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = PROJECT_ROOT / "generated_prompts"
TEST_OUTPUT_DIR = PROMPT_DIR / "tests"
DEFAULT_TEST_CASES = PROJECT_ROOT / "data" / "test_cases.json"


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
            variables = case.get("variables", {})
            max_tokens = case.get("max_tokens", 1024)
            print(f"\n- Test case: {name}")
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
