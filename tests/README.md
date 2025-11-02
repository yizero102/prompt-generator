# Test Infrastructure

This directory is reserved for automated testing infrastructure.

## Current Status

**Manual Testing Only**: Currently, all testing is manual. Test cases are defined in each example's `test-cases.md` file, and you run them by:

1. Taking test inputs
2. Replacing variables in prompt template
3. Sending to AI
4. Comparing output to expected behavior
5. Checking success criteria

## Future Plans

### Automated Test Runner

A test runner that could:
- Parse test cases from `test-cases.md` files
- Automatically replace variables in prompt templates
- Send prompts to AI APIs (Claude, GPT-4, etc.)
- Compare outputs against success criteria
- Generate test reports

### Example Future Usage

```bash
# Run all tests for an example
python tests/run_tests.py examples/menu-selection/

# Run specific test case
python tests/run_tests.py examples/menu-selection/ --test "Test Case 1"

# Run all examples
python tests/run_tests.py examples/

# Generate report
python tests/run_tests.py examples/ --report tests/results/report.html
```

### Proposed Test Runner Features

1. **Test Execution**
   - Automatic variable substitution
   - API integration (Claude, OpenAI, etc.)
   - Parallel test execution
   - Retry logic for API failures

2. **Result Validation**
   - Format checking (XML tags, sections)
   - Content validation (required elements present)
   - Success criteria evaluation
   - Consistency checking

3. **Reporting**
   - Pass/fail summary
   - Detailed failure reports
   - Performance metrics (response time, token usage)
   - Comparison across AI models
   - Trend analysis over time

4. **CI/CD Integration**
   - GitHub Actions workflow
   - Automated testing on prompt changes
   - Regression detection
   - Performance benchmarking

### Test Configuration Format

Proposed `test-config.yaml`:

```yaml
example: menu-selection
ai_provider: claude
model: claude-3-opus-20240229
test_cases:
  - name: "Test Case 1: Basic Vegetarian Preference"
    inputs:
      MENU: "1. Grilled Chicken Caesar Salad, 2. Margherita Pizza..."
      PREFERENCES: "I'm vegetarian and prefer lighter meals..."
    expected:
      format_valid: true
      contains_analysis: true
      contains_recommendation: true
      success_criteria:
        - "Recommendation is vegetarian"
        - "Reasoning mentions Italian preference"
        - "No non-vegetarian items suggested"
```

### Implementation Roadmap

**Phase 1: Basic Test Runner**
- Parse markdown test cases
- Manual input of AI responses
- Basic pass/fail validation

**Phase 2: API Integration**
- Connect to Claude/OpenAI APIs
- Automatic test execution
- Response capture

**Phase 3: Advanced Validation**
- Format validation (XML, structure)
- Content validation (required elements)
- Success criteria checking

**Phase 4: Reporting & Analysis**
- HTML report generation
- Comparison across models
- Performance tracking

**Phase 5: CI/CD**
- GitHub Actions integration
- Automated regression testing
- Deployment gates

## Contributing

Interested in building the automated test infrastructure? Here's how to help:

1. **Design**: Review and refine the proposed architecture
2. **Implement**: Build components of the test runner
3. **Test**: Validate with existing test cases
4. **Document**: Create usage guides and API docs

## Manual Testing Best Practices

Until automation is ready, follow these practices:

### Test Organization

1. Create a test log: `tests/logs/YYYY-MM-DD-example-name.md`
2. Document each test run:
   ```markdown
   ## Test Run: Menu Selection - 2024-01-15
   
   ### Test Case 1: Basic Vegetarian Preference
   - **Prompt Sent**: [copy of complete prompt]
   - **AI Response**: [full response]
   - **Status**: PASS ✓
   - **Notes**: Correctly identified vegetarian options
   
   ### Test Case 2: Allergy Restriction
   - **Status**: FAIL ✗
   - **Issue**: Didn't emphasize safety strongly enough
   - **Action**: Update prompt to prioritize allergies
   ```

### Test Tracking

Create `tests/logs/test-tracker.md`:

```markdown
# Test Tracker

| Example | Last Tested | Pass Rate | Status | Notes |
|---------|-------------|-----------|--------|-------|
| menu-selection | 2024-01-15 | 5/5 (100%) | ✓ | All tests pass |
| resume-rating | 2024-01-14 | 4/5 (80%) | ⚠ | Weighted scoring needs work |
| explain-concept | Not tested | - | ⏳ | Pending |
```

### Regression Testing

When updating prompts:
1. Run all existing tests before changes
2. Document baseline results
3. Make prompt changes
4. Re-run all tests
5. Compare results
6. Document improvements and regressions

## Test Data

Store reusable test data in `tests/data/`:

```
tests/data/
  ├── sample-resumes/
  ├── sample-menus/
  ├── sample-complaints/
  └── sample-research-papers/
```

This allows consistent testing across iterations.

## Questions or Ideas?

Open an issue or contribute to the test infrastructure design!
