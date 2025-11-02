# Prompt Generator Scripts

This directory contains Python scripts converted from the original `Prompt_Generator.ipynb` Jupyter notebook.

## Overview

The scripts provide a command-line interface for:
1. Generating prompt templates from task descriptions
2. Testing prompt templates with sample data
3. Batch processing of quickstart examples
4. Automated test case generation

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

## Core Module

### `prompt_generator.py`

The main module containing the `PromptGenerator` class with all core functionality:
- Metaprompt text and logic
- Prompt generation from task descriptions
- Variable extraction and validation
- Floating variable detection and fixing
- Prompt testing capabilities

## Command-Line Scripts

### `generate_prompt.py`

Generate a single prompt template from a task description.

**Usage:**
```bash
./generate_prompt.py "Your task description here" [options]
```

**Options:**
- `--variables VAR1 VAR2 ...` - Specify variables (optional)
- `--api-key KEY` - API key (or use ANTHROPIC_API_KEY env var)
- `--model MODEL` - Claude model to use (default: claude-3-5-sonnet-20241022)
- `--output FILE` - Save output to JSON file
- `--verbose` - Show detailed output including raw response

**Examples:**
```bash
# Basic usage
./generate_prompt.py "Draft an email responding to a customer complaint"

# With specific variables
./generate_prompt.py "Rate a resume" --variables RESUME RUBRIC

# Save to file
./generate_prompt.py "Explain a concept" --output my_prompt.json
```

### `test_prompt.py`

Test a generated prompt template with specific variable values.

**Usage:**
```bash
./test_prompt.py PROMPT_FILE [options]
```

**Options:**
- `--values JSON` - Variable values as JSON string or file path
- `--interactive` - Interactively prompt for variable values
- `--api-key KEY` - API key (or use ANTHROPIC_API_KEY env var)
- `--model MODEL` - Claude model to use
- `--output FILE` - Save test results to JSON file

**Examples:**
```bash
# Interactive mode
./test_prompt.py examples/customer_complaint_email.json --interactive

# With JSON file
./test_prompt.py examples/resume_rating.json --values test_values.json

# With inline JSON
./test_prompt.py examples/menu_item_chooser.json --values '{"$MENU": "...", "$PREFERENCES": "..."}'
```

### `generate_quickstart_examples.py`

Generate prompt templates for all quickstart examples from the README.

**Usage:**
```bash
./generate_quickstart_examples.py
```

This will generate prompt templates for:
- Customer complaint email response
- Menu item chooser
- Resume rating
- Scientific concept explainer
- Marketing strategy designer

Output files are saved to the `examples/` directory.

### `generate_test_cases.py`

Generate test cases for all prompt templates in the examples directory.

**Usage:**
```bash
./generate_test_cases.py
```

**Prerequisites:**
- Run `generate_quickstart_examples.py` first to create prompt templates
- Predefined test data for each example

Output files are saved to the `test_results/` directory.

### `complex_task_verification.py`

Verify the prompt generator with a complex, multi-faceted task.

**Usage:**
```bash
./complex_task_verification.py
```

This script:
1. Defines a complex code review task
2. Generates a prompt template
3. Tests it with sample code
4. Saves results for verification

## Workflow

### Complete End-to-End Example

```bash
# 1. Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY='your-key-here'

# 2. Generate all quickstart example prompts
./generate_quickstart_examples.py

# 3. Test all generated prompts
./generate_test_cases.py

# 4. Verify with a complex task
./complex_task_verification.py

# 5. Generate a custom prompt
./generate_prompt.py "Your custom task" --output custom_prompt.json

# 6. Test your custom prompt
./test_prompt.py custom_prompt.json --interactive
```

## Output Structure

### Prompt Template JSON Format

```json
{
  "name": "example_name",
  "task": "Task description",
  "variables": ["$VARIABLE1", "$VARIABLE2"],
  "prompt_template": "The full prompt template with {$VARIABLE1} placeholders"
}
```

### Test Result JSON Format

```json
{
  "prompt_data": { /* prompt template data */ },
  "test_values": {
    "$VARIABLE1": "test value 1",
    "$VARIABLE2": "test value 2"
  },
  "response": "Claude's response to the prompt"
}
```

## Directory Structure

```
.
├── prompt_generator.py              # Core module
├── generate_prompt.py               # CLI for single prompt generation
├── test_prompt.py                   # CLI for prompt testing
├── generate_quickstart_examples.py  # Batch generate quickstart examples
├── generate_test_cases.py           # Batch generate test cases
├── complex_task_verification.py     # Complex task verification
├── examples/                        # Generated prompt templates
│   ├── customer_complaint_email.json
│   ├── menu_item_chooser.json
│   └── ...
└── test_results/                    # Test results
    ├── customer_complaint_email_test.json
    ├── menu_item_chooser_test.json
    └── ...
```

## Troubleshooting

### API Key Issues

If you get an API key error:
```bash
export ANTHROPIC_API_KEY='your-key-here'
```

Or pass it directly:
```bash
./generate_prompt.py "Task" --api-key your-key-here
```

### Import Errors

Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Floating Variables

The prompt generator automatically detects and fixes "floating variables" (variables not properly enclosed in XML tags). If you see warnings about this, the system will attempt to fix them automatically.

## Differences from Notebook

The scripts provide the same functionality as the Jupyter notebook but with:
- Command-line interface for automation
- Better error handling
- File-based input/output
- Batch processing capabilities
- Easier integration into workflows

## API Rate Limits

Be aware of Anthropic API rate limits when running batch scripts. The quickstart examples script generates 5 prompts, which may take 2-3 minutes to complete.

## Support

For issues or questions:
1. Check the main README.md
2. Review the code comments in prompt_generator.py
3. Ensure your API key is valid and has sufficient credits
