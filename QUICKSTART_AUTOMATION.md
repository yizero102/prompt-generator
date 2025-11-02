# Prompt Generator Automation Project

This project provides automated tools for generating prompt templates from task descriptions and testing them systematically.

## Project Structure

```
prompt-generator/
├── README.md                          # Original metaprompt documentation
├── QUICKSTART_AUTOMATION.md          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore file
├── prompt_generator/                 # Core library
│   ├── __init__.py
│   ├── config.py                     # Metaprompt and example configurations
│   ├── generator.py                  # Prompt template generation logic
│   └── tester.py                     # Testing framework
├── examples/                         # Generated examples
│   ├── prompts/                      # Generated prompt templates
│   │   ├── menu_chooser.md
│   │   ├── resume_rater.md
│   │   ├── concept_explainer.md
│   │   ├── email_drafter.md
│   │   ├── marketing_strategist.md
│   │   └── taskmaster_agent.md
│   └── tests/                        # Test cases for each prompt
│       ├── menu_chooser_tests.json
│       ├── resume_rater_tests.json
│       ├── concept_explainer_tests.json
│       ├── email_drafter_tests.json
│       ├── marketing_strategist_tests.json
│       └── taskmaster_agent_tests.json
└── scripts/                          # CLI tools
    ├── generate_prompt.py            # Generate prompt for custom task
    ├── test_prompt.py                # Test a prompt with test cases
    └── run_all_examples.py           # Run all quickstart examples
```

## Features

### 1. Automated Prompt Generation

Generate prompt templates from task descriptions using the metaprompt:

```bash
python scripts/generate_prompt.py "Your task description" --variables VAR1 VAR2
```

### 2. Systematic Testing Framework

Test generated prompts with structured test cases:

```bash
python scripts/test_prompt.py examples/tests/menu_chooser_tests.json --report
```

### 3. Quickstart Examples

Six complete examples with prompts and tests:
- **Menu Chooser**: Select menu items based on preferences
- **Resume Rater**: Evaluate resumes against rubrics
- **Concept Explainer**: Explain scientific concepts simply
- **Email Drafter**: Respond to customer complaints
- **Marketing Strategist**: Create product launch strategies
- **TaskMaster Agent**: Planning and execution agent with tools

## Quick Start

### Run All Examples

```bash
python scripts/run_all_examples.py
```

This will:
1. Generate prompt templates for all quickstart examples
2. Run all test cases
3. Display a summary report

### Generate a Custom Prompt

```bash
# Basic usage
python scripts/generate_prompt.py "Translate technical documentation to non-technical language"

# With variables
python scripts/generate_prompt.py "Summarize meeting notes" --variables MEETING_TRANSCRIPT --output my_prompt.txt

# JSON format
python scripts/generate_prompt.py "Review code for security issues" --variables CODE --format json
```

### Test a Prompt

```bash
# Run tests from a test file
python scripts/test_prompt.py examples/tests/resume_rater_tests.json

# Generate a report
python scripts/test_prompt.py examples/tests/email_drafter_tests.json --report

# Save results
python scripts/test_prompt.py examples/tests/menu_chooser_tests.json --output results.json
```

## Prompt Template Examples

### Example 1: Menu Chooser

**Task**: Choose an item from a menu for me given user preferences

**Variables**: 
- `{$MENU}`: The menu with available items
- `{$PREFERENCES}`: User's dietary preferences and restrictions

**Test Cases**:
- Vegetarian preference with Italian food preference
- Multiple dietary restrictions (vegan + gluten-free)
- Budget constraint preference

[See full template](examples/prompts/menu_chooser.md)

### Example 2: Resume Rater

**Task**: Rate a resume according to a rubric

**Variables**:
- `{$RESUME}`: The resume text to evaluate
- `{$RUBRIC}`: Evaluation criteria and scoring guidelines

**Test Cases**:
- Mid-level software engineer evaluation
- Entry-level candidate evaluation
- Overqualified candidate evaluation

[See full template](examples/prompts/resume_rater.md)

### Example 3: Concept Explainer

**Task**: Explain a complex scientific concept in simple terms

**Variables**:
- `{$CONCEPT}`: The scientific concept to explain

**Test Cases**:
- Quantum entanglement
- Photosynthesis
- Black holes and event horizons
- DNA and genetic code

[See full template](examples/prompts/concept_explainer.md)

### Example 4: Email Drafter

**Task**: Draft an email responding to a customer complaint

**Variables**:
- `{$CUSTOMER_COMPLAINT}`: The complaint text
- `{$COMPANY_NAME}`: Company name

**Test Cases**:
- Shipping delay complaint
- Product quality complaint
- Service experience complaint
- Billing error complaint

[See full template](examples/prompts/email_drafter.md)

### Example 5: Marketing Strategist

**Task**: Design a marketing strategy for launching a new product

**Variables**:
- `{$PRODUCT_DESCRIPTION}`: Product details
- `{$TARGET_AUDIENCE}`: Target market description
- `{$BUDGET}`: Available marketing budget

**Test Cases**:
- Tech product for young professionals
- Local service business
- B2B software product

[See full template](examples/prompts/marketing_strategist.md)

### Example 6: TaskMaster Agent

**Task**: Planning and execution agent with system tools

**Variables**:
- `{$USER_TASK}`: Task to accomplish
- `{$AVAILABLE_TOOLS}`: Tools available for execution

**Test Cases**:
- Data analysis and reporting task
- Task with missing required tools
- Multi-step workflow with dependencies
- Ambiguous task requiring clarification

[See full template](examples/prompts/taskmaster_agent.md)

## Testing Framework

### Test Case Structure

Test cases are defined in JSON format:

```json
{
  "task": "Task description",
  "test_cases": [
    {
      "test_id": "unique_id",
      "description": "What this test validates",
      "inputs": {
        "VARIABLE1": "value1",
        "VARIABLE2": "value2"
      },
      "expected_behavior": "What should happen",
      "validation_criteria": [
        "Criterion 1",
        "Criterion 2"
      ]
    }
  ]
}
```

### Validation Criteria

Each test case includes validation criteria such as:
- Output format requirements (e.g., "Uses <recommendation> XML tags")
- Content requirements (e.g., "Addresses all dietary restrictions")
- Tone requirements (e.g., "Maintains professional tone")
- Structure requirements (e.g., "Includes all required sections")

### Running Tests

The testing framework:
1. Loads test cases from JSON files
2. Validates outputs against criteria
3. Reports pass/fail status
4. Generates summary reports

## Integration with LLM APIs

To integrate with actual LLM APIs for testing:

### Option 1: Anthropic Claude

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

def test_with_claude(prompt, test_inputs):
    # Fill in variables
    filled_prompt = prompt
    for var, value in test_inputs.items():
        filled_prompt = filled_prompt.replace(f"{{${var}}}", value)
    
    # Call Claude
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[{"role": "user", "content": filled_prompt}]
    )
    
    return message.content[0].text
```

### Option 2: OpenAI

```python
import openai

client = openai.OpenAI(api_key="your-api-key")

def test_with_openai(prompt, test_inputs):
    # Fill in variables
    filled_prompt = prompt
    for var, value in test_inputs.items():
        filled_prompt = filled_prompt.replace(f"{{${var}}}", value)
    
    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": filled_prompt}]
    )
    
    return response.choices[0].message.content
```

## Extending the System

### Add a New Prompt Template

1. Define your task in `prompt_generator/config.py`:

```python
QUICKSTART_EXAMPLES.append({
    "task": "Your new task",
    "variables": ["VAR1", "VAR2"]
})
```

2. Generate the prompt template:

```bash
python scripts/generate_prompt.py "Your new task" --variables VAR1 VAR2 --output examples/prompts/new_task.md
```

3. Create test cases in `examples/tests/new_task_tests.json`

### Add New Test Cases

Add test cases to existing test files:

```json
{
  "test_id": "new_test_001",
  "description": "Test description",
  "inputs": {
    "VARIABLE": "test value"
  },
  "expected_behavior": "Expected behavior",
  "validation_criteria": [
    "Criterion 1",
    "Criterion 2"
  ]
}
```

## Development

### Code Structure

- `prompt_generator/config.py`: Configuration and constants
- `prompt_generator/generator.py`: Prompt generation logic
- `prompt_generator/tester.py`: Testing framework
- `scripts/`: Command-line interfaces

### Testing Philosophy

Following the Testing section from the original README:
1. Define clear, measurable validation criteria
2. Test with diverse inputs
3. Validate both structure and content
4. Include edge cases
5. Test error handling

## Best Practices

### When Creating Prompts

1. **Start with clear task definition**: Be specific about what the AI should accomplish
2. **Identify minimal variables**: Use the fewest variables needed
3. **Plan structure first**: Think about input placement and instruction flow
4. **Use XML tags**: Clearly demarcate variable boundaries and output sections
5. **Provide examples**: For complex tasks, include examples in the prompt
6. **Request reasoning first**: Ask for justification before final answers

### When Creating Tests

1. **Cover normal cases**: Test typical, expected inputs
2. **Include edge cases**: Test boundaries and unusual scenarios
3. **Test error handling**: Include invalid or ambiguous inputs
4. **Validate structure**: Check for required sections and formatting
5. **Validate content**: Verify the response addresses the task
6. **Make criteria specific**: Use concrete, measurable validation criteria

## Troubleshooting

### Common Issues

**Problem**: Generated prompt doesn't include all variables

**Solution**: Explicitly list all required variables when generating

**Problem**: Test validation always fails

**Solution**: Check that validation criteria are not too strict; review the criterion checking logic in `tester.py`

**Problem**: Script import errors

**Solution**: Ensure you're running scripts from the project root directory

## Contributing

To add new features:

1. Add functionality to appropriate module in `prompt_generator/`
2. Create example prompts in `examples/prompts/`
3. Add test cases in `examples/tests/`
4. Update this documentation
5. Test with `run_all_examples.py`

## License

This project extends the original prompt-generator repository. See main README.md for details.

## Resources

- [Original Metaprompt Documentation](README.md)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
