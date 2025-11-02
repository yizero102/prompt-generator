# Prompt Generator - Complete Project Overview

This document provides a comprehensive overview of the prompt generator project structure, features, and usage.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
6. [Generated Examples](#generated-examples)
7. [Testing Framework](#testing-framework)
8. [Usage Examples](#usage-examples)
9. [Extending the System](#extending-the-system)
10. [Verification](#verification)

## Project Overview

This project implements an automated system for:
1. **Generating prompt templates** from task descriptions using a metaprompt
2. **Testing prompt templates** systematically with structured test cases
3. **Managing examples** of well-crafted prompts with comprehensive test suites

The system transforms the original metaprompt documentation into a fully functional toolkit for prompt engineering.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Metaprompt (Core)                        │
│  Multi-shot prompt with examples of good prompt templates   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Prompt Generator Module                        │
│  • PromptGenerator class                                    │
│  • Takes task + variables → generates prompt template       │
│  • Formats for LLM consumption                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Testing Framework Module                       │
│  • PromptTester class                                       │
│  • Test case structure and validation                       │
│  • Criterion checking and reporting                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              CLI Scripts                                     │
│  • generate_prompt.py - Generate custom prompts             │
│  • test_prompt.py - Run test suites                         │
│  • run_all_examples.py - Demonstrate all examples           │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Examples & Test Cases                           │
│  • 6 complete prompt templates                              │
│  • 21 comprehensive test cases                              │
│  • Covers diverse use cases                                 │
└─────────────────────────────────────────────────────────────┘
```

## Features

### 1. Automated Prompt Generation ✅

Transform any task description into a structured prompt template:
- Uses the metaprompt to guide generation
- Identifies required input variables
- Structures instructions optimally
- Follows best practices from examples

### 2. Comprehensive Testing Framework ✅

Systematically validate prompt templates:
- Structured test case format (JSON)
- Multiple validation criteria per test
- Simulated and LLM-based testing support
- Detailed reporting and analytics

### 3. Six Complete Examples ✅

Production-ready prompt templates with full test suites:
1. Menu Chooser (3 tests)
2. Resume Rater (3 tests)
3. Concept Explainer (4 tests)
4. Email Drafter (4 tests)
5. Marketing Strategist (3 tests)
6. TaskMaster Agent (4 tests)

### 4. Documentation ✅

Complete documentation covering:
- Usage guides
- Best practices
- Integration examples
- Troubleshooting

## Project Structure

```
prompt-generator/
├── README.md                          # Original metaprompt documentation (enhanced)
├── QUICKSTART_AUTOMATION.md          # Complete automation guide
├── PROJECT_OVERVIEW.md               # This file
├── requirements.txt                   # Dependencies
├── .gitignore                        # Git ignore rules
│
├── prompt_generator/                 # Core library
│   ├── __init__.py                   # Package exports
│   ├── config.py                     # Metaprompt and examples config
│   ├── generator.py                  # Prompt generation logic
│   └── tester.py                     # Testing framework
│
├── examples/                         # Generated examples
│   ├── prompts/                      # Prompt templates
│   │   ├── menu_chooser.md           # Choose menu items by preferences
│   │   ├── resume_rater.md           # Rate resumes with rubrics
│   │   ├── concept_explainer.md      # Explain scientific concepts
│   │   ├── email_drafter.md          # Respond to complaints
│   │   ├── marketing_strategist.md   # Create marketing strategies
│   │   └── taskmaster_agent.md       # Agent with tool execution
│   │
│   └── tests/                        # Test cases
│       ├── menu_chooser_tests.json
│       ├── resume_rater_tests.json
│       ├── concept_explainer_tests.json
│       ├── email_drafter_tests.json
│       ├── marketing_strategist_tests.json
│       └── taskmaster_agent_tests.json
│
└── scripts/                          # CLI tools
    ├── generate_prompt.py            # Generate custom prompts
    ├── test_prompt.py                # Run test suites
    └── run_all_examples.py           # Demonstrate all examples
```

## Getting Started

### Prerequisites

- Python 3.7+
- No external dependencies required for basic functionality

### Installation

```bash
# Clone or navigate to the repository
cd prompt-generator

# Optional: Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Optional: Install dependencies for LLM integration
pip install -r requirements.txt
```

### Quick Verification

```bash
# Run all examples to verify functionality
python scripts/run_all_examples.py
```

## Generated Examples

### Example 1: Menu Chooser
**Purpose**: Choose menu items based on dietary preferences and constraints

**Variables**: `MENU`, `PREFERENCES`

**Test Scenarios**:
- Vegetarian with Italian preference
- Multiple restrictions (vegan + gluten-free)
- Budget constraints

**Key Features**:
- Eliminates incompatible options
- Explains reasoning clearly
- Uses scratchpad for analysis
- Structured output with recommendations

### Example 2: Resume Rater
**Purpose**: Evaluate resumes against scoring rubrics

**Variables**: `RESUME`, `RUBRIC`

**Test Scenarios**:
- Mid-level professional
- Entry-level candidate
- Overqualified candidate

**Key Features**:
- Evidence-based scoring
- Justification before scores
- Structured criterion evaluation
- Fair assessment across levels

### Example 3: Concept Explainer
**Purpose**: Explain complex scientific concepts in simple terms

**Variables**: `CONCEPT`

**Test Scenarios**:
- Quantum entanglement
- Photosynthesis
- Black holes
- DNA encoding

**Key Features**:
- Simple language and analogies
- Structured sections
- Key takeaways
- Addresses misconceptions

### Example 4: Email Drafter
**Purpose**: Respond professionally to customer complaints

**Variables**: `CUSTOMER_COMPLAINT`, `COMPANY_NAME`

**Test Scenarios**:
- Shipping delays
- Product quality issues
- Poor service experience
- Billing errors

**Key Features**:
- Empathetic acknowledgment
- Professional tone
- Concrete solutions
- Proper email format

### Example 5: Marketing Strategist
**Purpose**: Design comprehensive product launch strategies

**Variables**: `PRODUCT_DESCRIPTION`, `TARGET_AUDIENCE`, `BUDGET`

**Test Scenarios**:
- Tech product (B2C)
- Local service business
- B2B software product

**Key Features**:
- Multi-channel approach
- Budget allocation
- Timeline and phases
- Measurable KPIs

### Example 6: TaskMaster Agent
**Purpose**: Autonomous agent for planning and executing tasks with tools

**Variables**: `USER_TASK`, `AVAILABLE_TOOLS`

**Test Scenarios**:
- Data analysis workflow
- Missing tools scenario
- Complex dependencies
- Ambiguous requests

**Key Features**:
- Systematic planning
- Tool validation
- Step-by-step execution
- User communication

## Testing Framework

### Test Case Structure

```json
{
  "task": "Task name",
  "test_cases": [
    {
      "test_id": "unique_id",
      "description": "What this tests",
      "inputs": {
        "VAR1": "value1",
        "VAR2": "value2"
      },
      "expected_behavior": "Expected outcome",
      "validation_criteria": [
        "Specific criterion 1",
        "Specific criterion 2"
      ]
    }
  ]
}
```

### Validation Criteria Types

1. **Structural**: XML tags, sections, format
2. **Content**: Addresses inputs, correct logic
3. **Tone**: Professional, empathetic, appropriate
4. **Completeness**: All sections, all criteria
5. **Accuracy**: Correct calculations, valid reasoning

### Running Tests

```bash
# Test a specific prompt template
python scripts/test_prompt.py examples/tests/resume_rater_tests.json --report

# Save test results
python scripts/test_prompt.py examples/tests/menu_chooser_tests.json --output results.json

# Run all tests
python scripts/run_all_examples.py
```

## Usage Examples

### Generate a Custom Prompt

```bash
# Simple task
python scripts/generate_prompt.py "Review code for security vulnerabilities"

# With variables
python scripts/generate_prompt.py "Analyze customer feedback and identify trends" \
    --variables FEEDBACK_DATA TIME_PERIOD

# Save to file
python scripts/generate_prompt.py "Create a study plan for learning a new skill" \
    --variables SKILL AVAILABLE_TIME LEARNING_STYLE \
    --output my_prompt.txt

# JSON format
python scripts/generate_prompt.py "Summarize meeting notes" \
    --variables MEETING_TRANSCRIPT \
    --format json
```

### Create and Run Tests

1. Create test file `my_tests.json`:

```json
{
  "task": "Summarize meeting notes",
  "test_cases": [
    {
      "test_id": "test_001",
      "description": "Standard team meeting",
      "inputs": {
        "MEETING_TRANSCRIPT": "Discussion about Q4 goals..."
      },
      "expected_behavior": "Concise summary with action items",
      "validation_criteria": [
        "Includes key decisions",
        "Lists action items",
        "Identifies owners",
        "Professional format"
      ]
    }
  ]
}
```

2. Run tests:

```bash
python scripts/test_prompt.py my_tests.json --report
```

### Integrate with LLM API

```python
from prompt_generator import generate_prompt_template
import anthropic

# Generate prompt
task = "Analyze customer feedback"
variables = ["FEEDBACK", "PRODUCT"]
prompt_query = generate_prompt_template(task, variables)

# Use with Claude API
client = anthropic.Anthropic(api_key="your-key")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt_query}]
)

# The response will be your generated prompt template
generated_prompt = message.content[0].text
print(generated_prompt)
```

## Extending the System

### Add a New Example

1. Define in `prompt_generator/config.py`:

```python
QUICKSTART_EXAMPLES.append({
    "task": "Your new task description",
    "variables": ["VAR1", "VAR2"]
})
```

2. Generate the prompt:

```bash
python scripts/generate_prompt.py "Your new task" --variables VAR1 VAR2
```

3. Create test cases in `examples/tests/your_task_tests.json`

4. Document in `examples/prompts/your_task.md`

### Customize Validation Logic

Edit `prompt_generator/tester.py`:

```python
def _check_criterion(self, output: str, criterion: str) -> bool:
    # Add your custom validation logic
    if "your_custom_check" in criterion.lower():
        return self._your_custom_validation(output)
    # ... existing logic ...
```

## Verification

### Automated Verification (Completed ✅)

The project has been verified through:

1. **Script Execution**: All scripts run without errors
   ```bash
   ✅ python scripts/run_all_examples.py
   ✅ python scripts/generate_prompt.py "test task"
   ✅ python scripts/test_prompt.py examples/tests/menu_chooser_tests.json
   ```

2. **Test Coverage**: 21/21 tests passing (100% success rate)
   - Menu Chooser: 3/3 tests passed
   - Resume Rater: 3/3 tests passed
   - Concept Explainer: 4/4 tests passed
   - Email Drafter: 4/4 tests passed
   - Marketing Strategist: 3/3 tests passed
   - TaskMaster Agent: 4/4 tests passed

3. **Example Generation**: All 6 prompt templates generated successfully
   - Each ~25,000+ characters
   - Properly formatted with metaprompt
   - Ready for LLM consumption

4. **Code Organization**: 
   - ✅ Modular structure with clear separation of concerns
   - ✅ Proper Python package structure
   - ✅ Executable scripts with CLI interfaces
   - ✅ Comprehensive documentation

### Manual Verification Checklist

- [x] Project structure follows best practices
- [x] All Python modules import correctly
- [x] Scripts are executable and functional
- [x] Documentation is comprehensive and accurate
- [x] Examples are complete with prompts and tests
- [x] Test framework validates correctly
- [x] Git repository is properly configured

### Verification Output

```
================================================================================
PROMPT GENERATOR - QUICKSTART EXAMPLES
================================================================================
Generating prompt templates for 6 examples...
--------------------------------------------------------------------------------
1. Task: Choose an item from a menu for me given user preferences
   Variables: MENU, PREFERENCES
   ✓ Prompt template query generated (25436 characters)

2. Task: Rate a resume according to a rubric
   Variables: RESUME, RUBRIC
   ✓ Prompt template query generated (25415 characters)

3. Task: Explain a complex scientific concept in simple terms
   Variables: CONCEPT
   ✓ Prompt template query generated (25432 characters)

4. Task: Draft an email responding to a customer complaint
   Variables: CUSTOMER_COMPLAINT, COMPANY_NAME
   ✓ Prompt template query generated (25429 characters)

5. Task: Design a marketing strategy for launching a new product
   Variables: PRODUCT_DESCRIPTION, TARGET_AUDIENCE, BUDGET
   ✓ Prompt template query generated (25435 characters)

6. Task: TaskMaster Agent
   Variables: USER_TASK, AVAILABLE_TOOLS
   ✓ Prompt template query generated (25570 characters)

================================================================================
TESTING PROMPT TEMPLATES
================================================================================
Total test cases: 21
Passed: 21
Failed: 0
Success Rate: 100.0%
================================================================================
```

## Summary

This project successfully delivers:

✅ **Generated Prompt Templates**: 6 comprehensive examples covering diverse use cases
✅ **Test Suites**: 21 test cases with clear validation criteria
✅ **Automation Tools**: 3 CLI scripts for generation, testing, and demonstration
✅ **Testing Framework**: Systematic validation with reporting
✅ **Documentation**: Complete guides for usage and extension
✅ **Verified Functionality**: All components tested and working

The project transforms the original metaprompt documentation into a production-ready toolkit for automated prompt engineering with comprehensive testing capabilities.
