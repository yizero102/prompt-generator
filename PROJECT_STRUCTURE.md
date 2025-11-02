# Project Structure

This document describes the organization and purpose of each directory and file in the prompt-generator project.

## Directory Structure

```
prompt-generator/
├── README.md                          # Main documentation with metaprompt and guidance
├── PROJECT_STRUCTURE.md               # This file - explains project organization
├── examples/                          # Generated prompt templates and their tests
│   ├── menu-selection/
│   │   ├── prompt-template.md        # Prompt for menu selection task
│   │   └── test-cases.md             # Test cases for menu selection
│   ├── resume-rating/
│   │   ├── prompt-template.md        # Prompt for resume rating task
│   │   └── test-cases.md             # Test cases for resume rating
│   ├── explain-concept/
│   │   ├── prompt-template.md        # Prompt for explaining concepts
│   │   └── test-cases.md             # Test cases for concept explanation
│   ├── customer-complaint/
│   │   ├── prompt-template.md        # Prompt for complaint responses
│   │   └── test-cases.md             # Test cases for complaint handling
│   ├── marketing-strategy/
│   │   ├── prompt-template.md        # Prompt for marketing strategy
│   │   └── test-cases.md             # Test cases for marketing plans
│   └── agent-design/
│       ├── prompt-template.md        # Prompt for agent design
│       └── test-cases.md             # Test cases for agent systems
├── templates/
│   └── metaprompt.txt                # The core metaprompt template
├── scripts/
│   ├── generate_prompt.py            # Generate prompts from task descriptions
│   ├── generate_tests.py             # Generate test frameworks
│   └── run_all.py                    # Main orchestration script
└── tests/                             # Future: automated test runner

```

## Component Descriptions

### `/examples/`

Contains real-world examples of prompt templates generated using the metaprompt. Each subdirectory represents one task type and includes:

- **prompt-template.md**: The complete prompt template with:
  - Task description
  - Input variables
  - Full instructions for the AI
  - Example usage showing expected input/output

- **test-cases.md**: Comprehensive test suite with:
  - Multiple test scenarios (happy path, edge cases, errors)
  - Expected behaviors for each test
  - Success criteria
  - Test metrics and passing criteria

**Purpose**: These serve as:
1. Templates you can use directly for similar tasks
2. Examples showing how to structure prompts
3. Reference implementations demonstrating best practices
4. Test coverage patterns for different task types

### `/templates/`

Contains the core metaprompt that generates all other prompts.

- **metaprompt.txt**: The long-form metaprompt with multiple examples teaching an AI how to write good prompts for any task

**Purpose**: This is the "prompt that generates prompts" - the foundation of the entire system.

### `/scripts/`

Automation tools for generating and testing prompts.

- **generate_prompt.py**: 
  - Takes a task description as input
  - Combines it with the metaprompt
  - Outputs a complete prompt ready to send to an AI
  - The AI then generates your custom prompt template

- **generate_tests.py**:
  - Takes a task name and variables
  - Generates a test framework and template
  - Provides guidance on creating comprehensive tests
  - Outputs markdown template for test cases

- **run_all.py**:
  - Main orchestration script
  - Guides you through the entire workflow
  - Generates prompts AND tests together
  - Creates proper directory structure
  - Interactive, step-by-step process

**Purpose**: Automate the repetitive parts of prompt creation and testing, letting you focus on the specifics of your task.

### `/tests/`

Reserved for future automated testing infrastructure.

**Future Plans**:
- Automated test runner that executes test cases
- Integration with AI APIs to run tests automatically
- Test result reporting and analysis
- Regression testing for prompt modifications

## Workflows

### 1. Create a New Prompt Template (Manual Process)

```bash
# Generate the metaprompt for your task
python scripts/generate_prompt.py "Your task description" "VAR1,VAR2"

# Copy output and send to AI (Claude, GPT-4)
# Save AI's <Instructions> as examples/your-task/prompt-template.md

# Generate test framework
python scripts/generate_tests.py "Your Task" "VAR1,VAR2"

# Create tests based on framework
# Save as examples/your-task/test-cases.md
```

### 2. Create a New Prompt Template (Guided Process)

```bash
# Run the interactive script
python scripts/run_all.py

# Follow prompts to:
# 1. Enter task description
# 2. Generate and save prompt template
# 3. Generate and save test cases
# 4. Test your prompt
```

### 3. Use an Existing Example

```bash
# Browse examples/ directory
# Copy relevant prompt-template.md
# Modify input variables to match your needs
# Reference test-cases.md to understand expected behavior
```

## File Naming Conventions

- **Directories**: lowercase with hyphens (e.g., `menu-selection`, `resume-rating`)
- **Markdown files**: lowercase with hyphens (e.g., `prompt-template.md`, `test-cases.md`)
- **Python scripts**: lowercase with underscores (e.g., `generate_prompt.py`)

## Adding New Examples

When adding a new example prompt template:

1. Create directory: `examples/your-task-name/`
2. Add `prompt-template.md` with:
   - Clear task description
   - Input variables defined
   - Complete instructions
   - At least one example usage
3. Add `test-cases.md` with:
   - Minimum 5 test cases
   - Mix of happy path, edge cases, and error scenarios
   - Clear success criteria
   - Test metrics defined
4. Ensure both files follow the format of existing examples

## Best Practices

### For Prompt Templates

- ✓ Use descriptive variable names in ALL_CAPS
- ✓ Wrap variables in XML tags
- ✓ Include examples of expected output
- ✓ Specify output format clearly (XML tags, sections, etc.)
- ✓ Add guidance for edge cases
- ✓ Keep instructions clear and specific

### For Test Cases

- ✓ Cover normal usage (happy path)
- ✓ Include edge cases (empty, very large, ambiguous input)
- ✓ Test error handling (invalid input, impossible requests)
- ✓ Define specific, measurable success criteria
- ✓ Include expected outputs, not just behaviors
- ✓ Test with realistic data

### For Documentation

- ✓ Keep README.md focused on the metaprompt and getting started
- ✓ Use this file (PROJECT_STRUCTURE.md) for organizational details
- ✓ Comment code in scripts for maintainability
- ✓ Update docs when adding new features

## Future Enhancements

Potential additions to the project:

1. **Automated Testing**
   - Script to run test cases against AI APIs
   - Automated success criteria checking
   - Test result reporting

2. **Prompt Versioning**
   - Track iterations of prompts
   - A/B testing different versions
   - Performance comparison

3. **Prompt Library**
   - Searchable database of prompts
   - Tags and categories
   - Community contributions

4. **Integration Tools**
   - CLI tool for quick prompt generation
   - API for programmatic access
   - IDE extensions

5. **Analytics**
   - Track which prompts perform best
   - Common failure patterns
   - Optimization suggestions
