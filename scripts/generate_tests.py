#!/usr/bin/env python3
"""
Script to help generate test cases for prompt templates.
Provides a framework and guidance for creating comprehensive test cases.
"""

import sys
from pathlib import Path

TEST_CASE_TEMPLATE = """# Test Cases: {task_name}

## Test Case 1: [Descriptive Name]
**Inputs:**
- VARIABLE1: "Example input value"
- VARIABLE2: "Another example value"

**Expected Behavior:**
- Should [describe what the AI should do]
- Should [another expected behavior]
- Should [handle specific scenario]

**Success Criteria:**
- [Specific measurable criterion]
- [Another criterion]
- [Edge case handling]

## Test Case 2: [Another Scenario]
[Continue with similar structure...]

## Test Metrics

For each test case, evaluate:
1. **Accuracy**: Does the output match expected results?
2. **Format Compliance**: Does it follow the specified output format?
3. **Completeness**: Are all aspects of the task addressed?
4. **Edge Case Handling**: Does it handle unusual inputs gracefully?
5. **Consistency**: Are outputs consistent across similar inputs?

## Passing Criteria
- [X]/[Y] test cases must pass accuracy check
- All outputs must follow the specified format
- No critical errors or hallucinations
- Edge cases handled appropriately
"""

def generate_test_framework(task_name, input_variables):
    """Generate a test case framework"""
    framework = f"""
TEST CASE DESIGN FRAMEWORK FOR: {task_name}
{"="*80}

Input Variables: {', '.join(input_variables)}

RECOMMENDED TEST CATEGORIES:

1. HAPPY PATH TESTS
   - Basic, straightforward inputs
   - Expected typical use case
   - Should work perfectly

2. EDGE CASE TESTS
   - Unusual but valid inputs
   - Boundary conditions
   - Extreme values (very long/short, empty, etc.)

3. ERROR HANDLING TESTS
   - Invalid inputs
   - Missing required information
   - Conflicting requirements

4. VARIATION TESTS
   - Different tones/styles (if applicable)
   - Different complexity levels
   - Different domains/contexts

5. FORMAT VALIDATION TESTS
   - Output structure compliance
   - Required tags/sections present
   - Proper formatting

SUGGESTED TEST CASES:

Test 1: Basic Valid Input
- Purpose: Verify core functionality works
- Input: [Simple, clear, typical example]
- Expected: [Successful completion with correct format]

Test 2: Complex Scenario
- Purpose: Test with realistic complexity
- Input: [More detailed, multi-faceted example]
- Expected: [Handles complexity gracefully]

Test 3: Edge Case - Minimal Input
- Purpose: Test with minimal/sparse information
- Input: [Very short or minimal data]
- Expected: [Handles gracefully, asks for more if needed]

Test 4: Edge Case - Maximum Input
- Purpose: Test with large amounts of data
- Input: [Very long or complex data]
- Expected: [Processes without truncation or errors]

Test 5: Ambiguous Input
- Purpose: Test disambiguation capabilities
- Input: [Unclear or ambiguous information]
- Expected: [Asks clarifying questions or makes reasonable assumptions]

Test 6: Invalid/Impossible Request
- Purpose: Test error handling
- Input: [Request that cannot be fulfilled]
- Expected: [Politely explains why it cannot be done]

SUCCESS METRICS:

For each test, check:
✓ Correct output format (all required sections/tags)
✓ Accurate content (matches input data)
✓ Appropriate tone/style
✓ Handles edge cases without breaking
✓ No hallucinations (doesn't invent data)
✓ Follows all instructions from prompt template

PASSING CRITERIA:
- All critical tests (1-4) must pass
- At least 80% of all tests must pass
- Zero critical failures (security, data accuracy)
"""
    return framework

def create_test_file_template(task_name):
    """Create a markdown test file template"""
    return TEST_CASE_TEMPLATE.format(task_name=task_name)

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_tests.py '<task_name>' [variable1,variable2,...]")
        print("\nExamples:")
        print("  python generate_tests.py 'Menu Selection' 'MENU,PREFERENCES'")
        print("  python generate_tests.py 'Resume Rating' 'RESUME,RUBRIC'")
        print("\nThis will generate a test case framework to help you create comprehensive tests.")
        sys.exit(1)
    
    task_name = sys.argv[1]
    variables = sys.argv[2].split(',') if len(sys.argv) > 2 else ['VARIABLE1', 'VARIABLE2']
    
    print(f"\nGenerating test framework for: {task_name}")
    print(f"Input variables: {', '.join(variables)}\n")
    print("="*80)
    
    framework = generate_test_framework(task_name, variables)
    print(framework)
    
    print("\n" + "="*80)
    print("MARKDOWN TEMPLATE")
    print("="*80 + "\n")
    
    template = create_test_file_template(task_name)
    print(template)
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("""
1. Copy the markdown template above
2. Fill in specific test cases based on your prompt template
3. For each test case, provide:
   - Realistic input values
   - Clear expected behaviors
   - Specific success criteria
4. Aim for 5-8 test cases covering different scenarios
5. Include at least one edge case and one error case
6. Save the test file alongside your prompt template

TESTING YOUR PROMPT:
- Use each test case's inputs with your prompt template
- Compare AI output against expected behavior
- Check success criteria are met
- Document any failures and iterate on prompt template
""")

if __name__ == "__main__":
    main()
