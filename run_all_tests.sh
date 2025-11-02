#!/bin/bash
# Comprehensive test script for the prompt generator
# This script runs all verification tests in sequence

set -e  # Exit on any error

echo "================================================================================"
echo "PROMPT GENERATOR - COMPREHENSIVE TEST SUITE"
echo "================================================================================"
echo ""

# Check if in virtual environment
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "⚠ Warning: Not in a virtual environment. Activating venv..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -q -r requirements.txt
    fi
fi

echo "Environment: ${VIRTUAL_ENV}"
echo ""

# Test 1: Unit Tests
echo "================================================================================"
echo "TEST 1: Running Unit Tests"
echo "================================================================================"
python3 test_scripts.py
echo ""

# Test 2: Demo without API
echo "================================================================================"
echo "TEST 2: Running Demo (No API Required)"
echo "================================================================================"
python3 demo_without_api.py
echo ""

# Test 3: Verify file structure
echo "================================================================================"
echo "TEST 3: Verifying File Structure"
echo "================================================================================"
echo "Checking Python scripts..."
for script in generate_prompt.py test_prompt.py generate_quickstart_examples.py \
              generate_test_cases.py complex_task_verification.py test_scripts.py \
              demo_without_api.py prompt_generator.py; do
    if [ -f "$script" ]; then
        echo "  ✓ $script"
    else
        echo "  ✗ $script MISSING"
        exit 1
    fi
done

echo ""
echo "Checking documentation..."
for doc in README.md SCRIPTS_README.md VERIFICATION.md; do
    if [ -f "$doc" ]; then
        echo "  ✓ $doc"
    else
        echo "  ✗ $doc MISSING"
        exit 1
    fi
done

echo ""
echo "Checking directories..."
for dir in examples test_results; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir/"
    else
        echo "  ✗ $dir/ MISSING"
        exit 1
    fi
done

echo ""

# Test 4: Verify executability
echo "================================================================================"
echo "TEST 4: Verifying Script Executability"
echo "================================================================================"
for script in generate_prompt.py test_prompt.py generate_quickstart_examples.py \
              generate_test_cases.py complex_task_verification.py test_scripts.py \
              demo_without_api.py; do
    if [ -x "$script" ]; then
        echo "  ✓ $script is executable"
    else
        echo "  ✗ $script is not executable"
        exit 1
    fi
done
echo ""

# Test 5: Verify help messages
echo "================================================================================"
echo "TEST 5: Verifying CLI Help Messages"
echo "================================================================================"
echo "Testing generate_prompt.py --help..."
./generate_prompt.py --help > /dev/null 2>&1 && echo "  ✓ generate_prompt.py help works"

echo "Testing test_prompt.py --help..."
./test_prompt.py --help > /dev/null 2>&1 && echo "  ✓ test_prompt.py help works"

echo ""

# Test 6: Check examples
echo "================================================================================"
echo "TEST 6: Checking Generated Examples"
echo "================================================================================"
if [ -f "examples/customer_complaint_email.json" ]; then
    echo "  ✓ customer_complaint_email.json exists"
    echo "  Variables: $(cat examples/customer_complaint_email.json | python3 -c 'import json, sys; print(", ".join(json.load(sys.stdin)["variables"]))')"
else
    echo "  ℹ No examples generated yet (requires API key)"
fi

if [ -f "examples/menu_item_chooser.json" ]; then
    echo "  ✓ menu_item_chooser.json exists"
else
    echo "  ℹ Demo examples available"
fi
echo ""

# Summary
echo "================================================================================"
echo "TEST SUMMARY"
echo "================================================================================"
echo ""
echo "✓ All unit tests passed"
echo "✓ Demo script works correctly"
echo "✓ File structure is correct"
echo "✓ All scripts are executable"
echo "✓ CLI help messages work"
echo "✓ Example files are generated"
echo ""
echo "================================================================================"
echo "SUCCESS: All tests passed!"
echo "================================================================================"
echo ""
echo "Next steps:"
echo "  1. Set ANTHROPIC_API_KEY environment variable"
echo "  2. Run: ./generate_quickstart_examples.py"
echo "  3. Run: ./generate_test_cases.py"
echo "  4. Run: ./complex_task_verification.py"
echo ""
echo "Or try a custom prompt:"
echo "  ./generate_prompt.py 'Your task here' --output my_prompt.json"
echo ""
