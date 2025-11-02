# Quick Reference Guide

## One-Line Commands

### Setup
```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### Set API Key
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Generate a Single Prompt
```bash
./generate_prompt.py "Your task description" --output prompt.json
```

### Test a Prompt
```bash
./test_prompt.py prompt.json --interactive
```

### Run All Tests (No API Required)
```bash
./run_all_tests.sh
```

### Generate All Quickstart Examples
```bash
./generate_quickstart_examples.py
```

### Test All Generated Prompts
```bash
./generate_test_cases.py
```

### Verify with Complex Task
```bash
./complex_task_verification.py
```

## Common Use Cases

### 1. Quick Demo (No API Key)
```bash
python3 test_scripts.py && python3 demo_without_api.py
```

### 2. Generate Custom Prompt with Variables
```bash
./generate_prompt.py "Rate a resume" --variables RESUME RUBRIC --output resume_rater.json
```

### 3. Test with JSON Values
```bash
./test_prompt.py prompt.json --values '{"$VAR1":"value1","$VAR2":"value2"}'
```

### 4. Test with JSON File
```bash
./test_prompt.py prompt.json --values values.json --output result.json
```

### 5. Verbose Output
```bash
./generate_prompt.py "Task" --verbose
```

## File Locations

| Type | Location |
|------|----------|
| Generated Prompts | `examples/*.json` |
| Test Results | `test_results/*.json` |
| Main Module | `prompt_generator.py` |
| Documentation | `SCRIPTS_README.md` |

## Script Overview

| Script | Purpose | Requires API |
|--------|---------|--------------|
| `prompt_generator.py` | Core module | N/A |
| `generate_prompt.py` | Generate single prompt | Yes |
| `test_prompt.py` | Test prompt template | Yes |
| `generate_quickstart_examples.py` | Batch generate examples | Yes |
| `generate_test_cases.py` | Auto-test prompts | Yes |
| `complex_task_verification.py` | Complex task test | Yes |
| `test_scripts.py` | Unit tests | No |
| `demo_without_api.py` | Demo mode | No |
| `run_all_tests.sh` | Full test suite | No |

## Troubleshooting

### "No module named 'anthropic'"
```bash
pip install anthropic
```

### "Error: API key required"
```bash
export ANTHROPIC_API_KEY='your-key'
```

### "Permission denied"
```bash
chmod +x *.py *.sh
```

### Check if scripts work
```bash
./test_scripts.py
```

## Example JSON Formats

### Prompt Template
```json
{
  "name": "example_name",
  "task": "Task description",
  "variables": ["$VAR1", "$VAR2"],
  "prompt_template": "Template with {$VAR1} and {$VAR2}"
}
```

### Variable Values
```json
{
  "$VAR1": "value one",
  "$VAR2": "value two"
}
```

### Test Result
```json
{
  "prompt_data": { /* prompt template */ },
  "test_values": { /* values used */ },
  "response": "Claude's response"
}
```

## Help Commands

```bash
./generate_prompt.py --help
./test_prompt.py --help
```

## Quick Verification

```bash
# Check all files exist
ls -la *.py *.sh *.md

# Run unit tests
python3 test_scripts.py

# Run comprehensive tests
./run_all_tests.sh
```

## Environment Info

```bash
# Check Python version
python3 --version

# Check if in virtual environment
echo $VIRTUAL_ENV

# List installed packages
pip list
```
