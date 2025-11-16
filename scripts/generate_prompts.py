#!/usr/bin/env python3
"""Generate prompt templates for the Quickstart examples using Anthropic."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import generate_prompt_template, pretty_print

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TASKS_FILE = PROJECT_ROOT / "data" / "quickstart_tasks.json"
OUTPUT_DIR = PROJECT_ROOT / "generated_prompts"
INDEX_FILE = OUTPUT_DIR / "index.json"


@dataclass
class TaskDefinition:
    name: str
    variables: Sequence[str]


def load_tasks(path: Path) -> List[TaskDefinition]:
    data = json.loads(path.read_text())
    tasks: List[TaskDefinition] = []
    for entry in data:
        name = entry.get("task")
        if not name:
            raise ValueError(f"Task entry is missing a 'task' field: {entry!r}")
        variables = entry.get("variables", [])
        tasks.append(TaskDefinition(name=name, variables=list(variables)))
    return tasks


def slugify(text: str) -> str:
    import re

    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def save_prompt(slug: str, payload: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{slug}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def update_index(entries: List[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tasks",
        type=Path,
        default=DEFAULT_TASKS_FILE,
        help="Path to the JSON file describing tasks to generate prompts for.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv or sys.argv[1:])
    tasks = load_tasks(args.tasks)

    index_entries: List[dict] = []

    for task in tasks:
        print("=" * 80)
        print(f"Generating prompt for task: {task.name}")
        result = generate_prompt_template(task.name, task.variables)

        slug = slugify(task.name)
        payload = {
            "task": task.name,
            "slug": slug,
            "requested_variables": list(task.variables),
            "identified_variables": result.identified_variables,
            "floating_variables": result.floating_variables,
            "metaprompt_thinking": result.metaprompt_thinking,
            "metaprompt_response": result.metaprompt_response,
            "floating_variable_analysis": result.floating_variable_analysis,
            "raw_prompt_template": result.raw_prompt_template,
            "final_prompt_template": result.final_prompt_template,
        }

        save_prompt(slug, payload)

        index_entries.append(
            {
                "task": task.name,
                "slug": slug,
                "requested_variables": list(task.variables),
                "identified_variables": result.identified_variables,
            }
        )

        print("\nFinal prompt template:\n")
        print(pretty_print(result.prompt))
        print("\nVariables identified:", ", ".join(result.identified_variables) or "(none)")

    update_index(index_entries)
    print("\nPrompt generation complete. Output saved to", OUTPUT_DIR)


if __name__ == "__main__":
    main()
