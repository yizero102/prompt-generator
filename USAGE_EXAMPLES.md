# Usage Examples

This document provides practical, copy-paste examples for using the prompt generator automation system.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Generation](#advanced-generation)
3. [Testing Examples](#testing-examples)
4. [Integration Examples](#integration-examples)
5. [Creating Custom Templates](#creating-custom-templates)

## Basic Usage

### Example 1: Generate a Simple Prompt

```bash
python scripts/generate_prompt.py "Translate text from English to Spanish"
```

This generates a prompt template query that you can send to an LLM to get a complete prompt template.

### Example 2: Generate with Variables

```bash
python scripts/generate_prompt.py \
    "Analyze customer reviews and extract sentiment" \
    --variables REVIEWS PRODUCT_NAME
```

### Example 3: Save to File

```bash
python scripts/generate_prompt.py \
    "Create a study guide from lecture notes" \
    --variables LECTURE_NOTES SUBJECT DIFFICULTY_LEVEL \
    --output study_guide_prompt.txt
```

### Example 4: JSON Output

```bash
python scripts/generate_prompt.py \
    "Debug code and suggest fixes" \
    --variables CODE ERROR_MESSAGE \
    --format json > debug_prompt.json
```

## Advanced Generation

### Example 5: Complex Task with Multiple Variables

```bash
python scripts/generate_prompt.py \
    "Analyze financial data and generate investment recommendations" \
    --variables FINANCIAL_DATA RISK_TOLERANCE TIME_HORIZON INVESTMENT_GOALS
```

### Example 6: Agent-Style Prompt

```bash
python scripts/generate_prompt.py \
    "Act as a code review assistant that analyzes pull requests" \
    --variables CODE_DIFF CODING_STANDARDS PROJECT_CONTEXT
```

### Example 7: Content Generation Task

```bash
python scripts/generate_prompt.py \
    "Write blog posts optimized for SEO" \
    --variables TOPIC TARGET_KEYWORDS AUDIENCE TONE
```

## Testing Examples

### Example 8: Test Menu Chooser

```bash
python scripts/test_prompt.py \
    examples/tests/menu_chooser_tests.json \
    --report
```

Expected output:
```
Running tests for: Choose an item from a menu for me given user preferences
============================================================
Test ID: menu_001
Description: Vegetarian preference with Italian food preference
Status: passed
Passed criteria: 5
Failed criteria: 0
...
```

### Example 9: Test Resume Rater with Results Saved

```bash
python scripts/test_prompt.py \
    examples/tests/resume_rater_tests.json \
    --report \
    --output resume_test_results.json
```

### Example 10: Run All Tests

```bash
python scripts/run_all_examples.py
```

This runs all 21 test cases across 6 prompt templates.

## Integration Examples

### Example 11: Python Integration - Generate and Use

```python
from prompt_generator import generate_prompt_template

# Generate prompt template query
task = "Analyze meeting transcripts and extract action items"
variables = ["MEETING_TRANSCRIPT"]
prompt_query = generate_prompt_template(task, variables)

print(f"Generated prompt query: {len(prompt_query)} characters")
```

### Example 12: Testing Framework Integration

```python
from prompt_generator import PromptTester

# Create tester
tester = PromptTester()

# Create test case
test_case = tester.create_test_case(
    task="Summarize articles",
    prompt_template="...",
    variables={"ARTICLE": "Long article text..."},
    expected_behavior="Concise summary with key points",
    validation_criteria=[
        "Summary is under 200 words",
        "Includes main points",
        "Maintains factual accuracy"
    ]
)

# Run test
result = tester.run_test(test_case)
print(f"Test status: {result['status']}")
```

### Example 13: With Anthropic Claude

```python
from prompt_generator import generate_prompt_template
import anthropic

# Step 1: Generate the prompt template query
task = "Analyze user feedback and identify common themes"
variables = ["FEEDBACK_DATA", "TIME_PERIOD"]
prompt_query = generate_prompt_template(task, variables)

# Step 2: Send to Claude to get the actual prompt template
client = anthropic.Anthropic(api_key="your-api-key")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt_query}]
)

# Step 3: Extract the generated prompt template
generated_prompt_template = message.content[0].text
print("Generated Prompt Template:")
print(generated_prompt_template)

# Step 4: Now you can use this template with actual data
actual_feedback = "Users love feature X but find feature Y confusing..."
actual_timeframe = "Q3 2024"

# Fill in the template
filled_prompt = generated_prompt_template.replace(
    "{$FEEDBACK_DATA}", actual_feedback
).replace(
    "{$TIME_PERIOD}", actual_timeframe
)

# Step 5: Use the filled prompt
final_response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2000,
    messages=[{"role": "user", "content": filled_prompt}]
)

print("Analysis Result:")
print(final_response.content[0].text)
```

### Example 14: With OpenAI

```python
from prompt_generator import generate_prompt_template
import openai

# Generate prompt template query
task = "Create quiz questions from educational content"
variables = ["CONTENT", "DIFFICULTY", "QUESTION_COUNT"]
prompt_query = generate_prompt_template(task, variables)

# Get prompt template from GPT-4
client = openai.OpenAI(api_key="your-api-key")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt_query}]
)

generated_prompt = response.choices[0].message.content
print(generated_prompt)
```

### Example 15: Batch Processing

```python
from prompt_generator import generate_prompt_template
import json

# Define multiple tasks
tasks = [
    {
        "name": "sentiment_analyzer",
        "task": "Analyze sentiment of customer reviews",
        "variables": ["REVIEW_TEXT", "RATING"]
    },
    {
        "name": "email_classifier",
        "task": "Classify emails by urgency and category",
        "variables": ["EMAIL_CONTENT", "SENDER"]
    },
    {
        "name": "code_documenter",
        "task": "Generate documentation for code functions",
        "variables": ["CODE", "LANGUAGE"]
    }
]

# Generate all prompts
for task_config in tasks:
    print(f"\nGenerating prompt for: {task_config['name']}")
    
    prompt_query = generate_prompt_template(
        task_config['task'],
        task_config['variables']
    )
    
    # Save to file
    filename = f"prompts/{task_config['name']}_query.txt"
    with open(filename, 'w') as f:
        f.write(prompt_query)
    
    print(f"Saved to {filename}")
```

## Creating Custom Templates

### Example 16: Create New Template and Tests

**Step 1**: Generate the prompt
```bash
python scripts/generate_prompt.py \
    "Analyze code quality and suggest improvements" \
    --variables CODE_SNIPPET LANGUAGE FOCUS_AREAS \
    --output examples/prompts/code_analyzer.txt
```

**Step 2**: Create test file `examples/tests/code_analyzer_tests.json`:
```json
{
  "task": "Analyze code quality and suggest improvements",
  "test_cases": [
    {
      "test_id": "code_001",
      "description": "Python code with performance issues",
      "inputs": {
        "CODE_SNIPPET": "def slow_function():\n    result = []\n    for i in range(1000):\n        result.append(i**2)\n    return result",
        "LANGUAGE": "Python",
        "FOCUS_AREAS": "Performance, readability"
      },
      "expected_behavior": "Identifies inefficiency, suggests list comprehension",
      "validation_criteria": [
        "Identifies performance issue",
        "Suggests specific improvement",
        "Provides example code",
        "Explains why improvement is better"
      ]
    }
  ]
}
```

**Step 3**: Test it
```bash
python scripts/test_prompt.py \
    examples/tests/code_analyzer_tests.json \
    --report
```

### Example 17: Add to Quickstart Examples

Edit `prompt_generator/config.py`:
```python
QUICKSTART_EXAMPLES.append({
    "task": "Analyze code quality and suggest improvements",
    "variables": ["CODE_SNIPPET", "LANGUAGE", "FOCUS_AREAS"]
})
```

Then run:
```bash
python scripts/run_all_examples.py
```

### Example 18: Custom Validation Logic

Edit `prompt_generator/tester.py` to add custom validation:

```python
def _check_criterion(self, output: str, criterion: str) -> bool:
    # Existing logic...
    
    # Add your custom validation
    if "code example" in criterion.lower():
        # Check if output contains code blocks
        return "```" in output or "<code>" in output
    
    if "performance improvement" in criterion.lower():
        # Check for performance-related keywords
        keywords = ["faster", "efficient", "optimize", "reduce", "improve"]
        return any(keyword in output.lower() for keyword in keywords)
    
    # Continue with existing logic...
```

## Real-World Workflow Examples

### Example 19: Complete Workflow for New Use Case

```bash
# 1. Generate prompt template query
python scripts/generate_prompt.py \
    "Create user stories from product requirements" \
    --variables REQUIREMENTS PERSONAS ACCEPTANCE_CRITERIA \
    --format json \
    --output user_story_query.json

# 2. (Send to LLM to get actual template)

# 3. Create test cases
cat > examples/tests/user_story_tests.json << 'EOF'
{
  "task": "Create user stories from product requirements",
  "test_cases": [
    {
      "test_id": "story_001",
      "description": "E-commerce checkout feature",
      "inputs": {
        "REQUIREMENTS": "Users should be able to checkout with saved payment methods",
        "PERSONAS": "Returning customer, values convenience",
        "ACCEPTANCE_CRITERIA": "Payment completes in under 3 clicks"
      },
      "expected_behavior": "Well-formed user story with acceptance criteria",
      "validation_criteria": [
        "Follows user story format",
        "Includes acceptance criteria",
        "References persona",
        "Specific and testable"
      ]
    }
  ]
}
EOF

# 4. Run tests
python scripts/test_prompt.py \
    examples/tests/user_story_tests.json \
    --report

# 5. Verify everything
python scripts/verify_project.py
```

### Example 20: Iterative Refinement

```bash
# Test current version
python scripts/test_prompt.py examples/tests/email_drafter_tests.json --report

# If tests fail, review output and refine the prompt template

# Re-test
python scripts/test_prompt.py examples/tests/email_drafter_tests.json --report

# Continue until all tests pass
```

## Tips and Tricks

### Tip 1: View Generated Prompt Query
```bash
python scripts/generate_prompt.py "Your task" | less
```

### Tip 2: Count Characters
```bash
python scripts/generate_prompt.py "Your task" | wc -c
```

### Tip 3: Quick Test
```bash
# Test just one test file
python scripts/test_prompt.py examples/tests/menu_chooser_tests.json

# With detailed report
python scripts/test_prompt.py examples/tests/menu_chooser_tests.json --report
```

### Tip 4: Pipe Output
```bash
python scripts/generate_prompt.py "Your task" | \
    python -c "import sys; print(len(sys.stdin.read()), 'characters')"
```

### Tip 5: Multiple Formats
```bash
# Text format for reading
python scripts/generate_prompt.py "Task" > prompt.txt

# JSON format for processing
python scripts/generate_prompt.py "Task" --format json > prompt.json
```

## Common Patterns

### Pattern 1: Analysis Tasks
```bash
python scripts/generate_prompt.py \
    "Analyze [DATA TYPE] and identify [INSIGHTS]" \
    --variables DATA CONTEXT
```

### Pattern 2: Generation Tasks
```bash
python scripts/generate_prompt.py \
    "Generate [OUTPUT TYPE] based on [INPUT TYPE]" \
    --variables INPUT OUTPUT_REQUIREMENTS
```

### Pattern 3: Transformation Tasks
```bash
python scripts/generate_prompt.py \
    "Transform [SOURCE FORMAT] to [TARGET FORMAT]" \
    --variables SOURCE_DATA TARGET_SPECIFICATION
```

### Pattern 4: Evaluation Tasks
```bash
python scripts/generate_prompt.py \
    "Evaluate [SUBJECT] against [CRITERIA]" \
    --variables SUBJECT CRITERIA RUBRIC
```

### Pattern 5: Interactive Tasks
```bash
python scripts/generate_prompt.py \
    "Act as [ROLE] and help with [TASK]" \
    --variables USER_INPUT CONTEXT
```

## Troubleshooting Examples

### Issue 1: Import Errors
```bash
# Make sure you're in the project root
cd /path/to/prompt-generator
python scripts/generate_prompt.py "test"
```

### Issue 2: Verify Installation
```bash
python scripts/verify_project.py
```

### Issue 3: Check Test Results
```bash
# Run with detailed output
python scripts/test_prompt.py examples/tests/menu_chooser_tests.json --report
```

### Issue 4: Debug Generation
```python
from prompt_generator import PromptGenerator, METAPROMPT

gen = PromptGenerator(METAPROMPT)
result = gen.generate_prompt("Test task", ["VAR1"])
print(result)
```

## Next Steps

After trying these examples:
1. Read `QUICKSTART_AUTOMATION.md` for detailed documentation
2. Explore `examples/prompts/` for template inspiration
3. Review `examples/tests/` for test case patterns
4. Create your own custom prompts and tests

---

**More Examples**: See `QUICKSTART_AUTOMATION.md`  
**Full Documentation**: See `PROJECT_OVERVIEW.md`  
**Quick Start**: See `QUICK_START.md`
