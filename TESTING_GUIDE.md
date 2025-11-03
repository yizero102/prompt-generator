# Testing Guide for Agent X

This guide explains how to test the Agent X prompt template with real LLM calls.

## Prerequisites

1. Set up Python environment:
```bash
python3 -m venv .venv
.venv/bin/pip install anthropic
```

2. Configure API credentials:
```bash
export _ANTHROPIC_API_KEY="your-api-key-here"
export _MODEL_NAME="claude-3-5-sonnet-20241022"
export _ANTHROPIC_BASE_URL="https://api.anthropic.com"  # optional
```

## Running Tests

### Quick Test - Agent X Native Tools
This is the main test script that validates all Agent X functionality:

```bash
.venv/bin/python scripts/test_agent_x_native_tools.py
```

**What it tests:**
- ✓ Single tool per turn enforcement
- ✓ Multi-turn execution with history tracking
- ✓ Proper termination with 'finish' tool
- ✓ 4 different scenarios (calculation, multi-step, search, file ops)

**Expected output:**
```
================================================================================
TESTING AGENT X WITH NATIVE TOOL CALLING
================================================================================
...
TEST SUMMARY
================================================================================
Passed: 4/4
✓ simple_calculation
✓ multi_step_calculation
✓ search_and_summarize
✓ file_operations

🎉 ALL TESTS PASSED! 🎉
```

### Test Scenarios

#### 1. Simple Calculation
**Task:** Calculate 15 * 23 + 47
**Expected behavior:**
- Turn 1: Call `calculate` with expression "15 * 23 + 47"
- Turn 2: Call `finish` with result summary
**Tool sequence:** calculate → finish

#### 2. Multi-Step Calculation
**Task:** Calculate average of 10, 20, 30, 40 in two separate calculations
**Expected behavior:**
- Turn 1: Call `calculate` to sum: "10+20+30+40"
- Turn 2: Call `calculate` to divide: "100/4"
- Turn 3: Call `finish` with final result
**Tool sequence:** calculate → calculate → finish

#### 3. Search and Summarize
**Task:** Search for information about Python programming
**Expected behavior:**
- Turn 1: Call `search_web` with query about Python
- Turn 2 (optional): More searches if needed
- Final turn: Call `finish` with summary
**Tool sequence:** search_web → [search_web...] → finish

#### 4. File Operations
**Task:** Read 'data.txt' and write summary to 'summary.txt'
**Expected behavior:**
- Turn 1: Call `read_file` with filepath "data.txt"
- Turn 2: Call `write_file` with filepath "summary.txt" and content
- Turn 3: Call `finish` with completion summary
**Tool sequence:** read_file → write_file → finish

## Test Results

Results are saved to: `generated_prompts/agent_x_native_test_results.json`

Example output:
```json
{
  "all_passed": true,
  "tests": [
    {
      "name": "simple_calculation",
      "passed": true,
      "turns": 2,
      "tool_calls": ["calculate", "finish"],
      "error": null
    },
    ...
  ]
}
```

## Validation Criteria

Each test validates:

### 1. One Tool Per Turn
```python
if len(tool_uses) != 1:
    # FAIL: Must call exactly one tool
```

### 2. History Maintenance
```python
# Each turn adds to message history:
messages.append({"role": "assistant", "content": response.content})
messages.append({"role": "user", "content": [{"type": "tool_result", ...}]})
```

### 3. Proper Termination
```python
if tool_use.name == "finish":
    # SUCCESS: Agent signaled completion
    break
```

### 4. Maximum Turns
```python
if turn >= max_turns and not finished:
    # FAIL: Did not finish within turn limit
```

## Debugging Failed Tests

If a test fails, the script provides detailed information:

```
✗ FAILED - No tool call found in turn 1
```

Common issues:
- **No tool call found**: Agent returned text instead of calling a tool
- **Multiple tool calls found**: Agent tried to call more than one tool
- **Did not call 'finish'**: Agent didn't terminate properly

### Debugging Steps

1. Check the response output (printed during test):
```
Turn 1 response:
----------------------------------------
<scratchpad>I need to calculate...</scratchpad>
<function_call>calculate(expression="15 * 23 + 47")</function_call>
----------------------------------------
```

2. Review the system prompt in the script to ensure it's clear

3. Check tool definitions are correct

4. Verify API credentials are set correctly

## Adding New Test Cases

To add a new test case, edit `scripts/test_agent_x_native_tools.py`:

```python
TEST_CASES.append(
    TestCase(
        name="my_new_test",
        task="Description of what to do",
        expected_tools=["tool1", "tool2", "finish"],
        max_turns=10,
        description="What this tests"
    )
)
```

Also add corresponding tool simulation in `simulate_tool_execution()` if needed.

## Continuous Testing

Run multiple times to check consistency:

```bash
for i in {1..5}; do
    echo "=== Run $i ==="
    .venv/bin/python scripts/test_agent_x_native_tools.py 2>&1 | grep "Passed:"
done
```

Expected output:
```
=== Run 1 ===
Passed: 4/4
=== Run 2 ===
Passed: 4/4
...
```

## Interpreting Results

### All Tests Passed ✓
- The Agent X prompt is working correctly
- All constraints are being followed
- History tracking is functioning
- Termination is proper

### Some Tests Failed ✗
- Review the error messages
- Check which turn failed
- Look at the agent's response
- May need to adjust system prompt clarity

### Tests Inconsistent
- Some runs pass, some fail
- May indicate prompt ambiguity
- Need to make instructions more explicit
- Consider adding more examples to the prompt

## Performance Metrics

Track these metrics across test runs:

- **Success rate**: % of tests that pass
- **Average turns**: How many turns to complete tasks
- **Tool diversity**: Which tools are being used
- **Finish rate**: % of tests that call 'finish'

## Best Practices

1. **Always test with real API calls** - Don't rely on mocks
2. **Test multiple scenarios** - Cover edge cases
3. **Run tests multiple times** - Check for consistency
4. **Log detailed output** - Enable debugging when needed
5. **Version control results** - Track improvements over time

## Troubleshooting

### API Connection Issues
```bash
# Verify API credentials
.venv/bin/python scripts/verify_llm.py
```

### Import Errors
```bash
# Reinstall dependencies
.venv/bin/pip install --upgrade anthropic
```

### Model Not Available
```bash
# Check model name
echo $_MODEL_NAME

# Try alternative model
export _MODEL_NAME="claude-3-5-sonnet-20241022"
```

## Further Reading

- [AGENT_X_IMPLEMENTATION.md](AGENT_X_IMPLEMENTATION.md) - Detailed implementation notes
- [README.md](README.md) - Full Agent X documentation with examples
- [generated_prompts/agent_x_prompt_native.txt](generated_prompts/agent_x_prompt_native.txt) - The actual prompt template
