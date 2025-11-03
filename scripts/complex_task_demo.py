#!/usr/bin/env python3
"""Generate and exercise the prompt generator on a complex coordination task using the configured LLM."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import generate_prompt_template, pretty_print, run_prompt_test

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_DIR = PROJECT_ROOT / "generated_prompts"
TEST_OUTPUT_DIR = PROMPT_DIR / "tests"

COMPLEX_TASK = (
    "Coordinate a multinational crisis-response war room that must triage "
    "customer-impacting incidents, assign cross-functional owners, and "
    "produce executive-ready situation reports under rapidly changing "
    "constraints."
)
COMPLEX_VARIABLES = [
    "INCIDENT_FEED",
    "RESPONSE_DIRECTORY",
    "EXECUTIVE_CONSTRAINTS",
]

TEST_CASE = {
    "$INCIDENT_FEED": (
        "<incident>\n"
        "Company-wide authentication outages reported in Americas and EMEA regions.\n"
        "Root cause suspected to be certificate expiration in identity provider.\n"
        "Customer impact: inability to log in to SaaS dashboard; mobile apps degraded.\n"
        "</incident>\n"
        "<incident>\n"
        "Payment retries piling up for EU customers; finance reports risk of missed SLAs.\n"
        "</incident>"
    ),
    "$RESPONSE_DIRECTORY": (
        "<teams>\n"
        "<team name=\"Identity Platform\" leader=\"H. Patel\" escalation=\"+1-415-555-1010\" />\n"
        "<team name=\"SRE-Global\" leader=\"C. Alvarez\" escalation=\"chat://sre-global\" />\n"
        "<team name=\"Finance Ops\" leader=\"M. Lavigne\" escalation=\"+33-555-2233\" />\n"
        "</teams>"
    ),
    "$EXECUTIVE_CONSTRAINTS": (
        "Daily executive briefing due at 14:00 UTC; maintain regulator-safe language and "
        "cite validated data sources only."
    ),
}


def slugify(text: str) -> str:
    import re

    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def save_payload(slug: str, payload: dict, suffix: str = "") -> None:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    destination = PROMPT_DIR / f"{slug}{suffix}.json"
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> None:
    slug = slugify("complex war room coordination")
    print("Generating prompt for complex task...\n")
    result = generate_prompt_template(COMPLEX_TASK, COMPLEX_VARIABLES)

    payload = {
        "task": COMPLEX_TASK,
        "slug": slug,
        "requested_variables": COMPLEX_VARIABLES,
        "identified_variables": result.identified_variables,
        "floating_variables": result.floating_variables,
        "metaprompt_thinking": result.metaprompt_thinking,
        "metaprompt_response": result.metaprompt_response,
        "floating_variable_analysis": result.floating_variable_analysis,
        "raw_prompt_template": result.raw_prompt_template,
        "final_prompt_template": result.final_prompt_template,
    }
    save_payload(slug, payload)

    print("Prompt template:\n")
    print(pretty_print(result.prompt))
    print("\nVariables identified:", ", ".join(result.identified_variables) or "(none)")

    print("\nRunning sample test case...\n")
    test_result = run_prompt_test(result.prompt, TEST_CASE, max_tokens=2048)
    print("Prompt sent to model:\n")
    print(pretty_print(test_result.prompt_with_variables))
    if test_result.thinking:
        print("\nModel thinking:\n")
        print(pretty_print(test_result.thinking))
    print("\nModel output:\n")
    print(pretty_print(test_result.output))

    TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    save_payload(
        slug,
        {
            "slug": slug,
            "task": COMPLEX_TASK,
            "test_case_name": "demo",
            "variables": TEST_CASE,
            "prompt_with_variables": test_result.prompt_with_variables,
            "thinking": test_result.thinking,
            "output": test_result.output,
        },
        suffix="__test-demo",
    )
    print("\nComplex task demo complete. Results saved to generated_prompts/.")


if __name__ == "__main__":
    main()
