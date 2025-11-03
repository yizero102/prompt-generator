#!/usr/bin/env python3
"""
Test script to verify the basic functionality of the prompt generator scripts.
This tests the structure and helper functions without requiring API calls.
"""
import sys
from prompt_generator import PromptGenerator


def test_extract_between_tags():
    """Test XML tag extraction."""
    print("Testing extract_between_tags...")
    test_string = "<test>content1</test> and <test>content2</test>"
    result = PromptGenerator.extract_between_tags("test", test_string)
    assert result == ["content1", "content2"], f"Expected ['content1', 'content2'], got {result}"
    print("  ✓ extract_between_tags works correctly")


def test_remove_empty_tags():
    """Test empty tag removal."""
    print("Testing remove_empty_tags...")
    test_string = "text\n<empty></empty>\nmore text"
    result = PromptGenerator.remove_empty_tags(test_string)
    assert "<empty>" not in result, "Empty tags should be removed"
    print("  ✓ remove_empty_tags works correctly")


def test_extract_variables():
    """Test variable extraction."""
    print("Testing extract_variables...")
    test_prompt = "This is a {$VARIABLE1} and {$VARIABLE2} test"
    result = PromptGenerator.extract_variables(test_prompt)
    assert "$VARIABLE1" in result and "$VARIABLE2" in result, f"Variables not extracted correctly: {result}"
    print("  ✓ extract_variables works correctly")


def test_find_free_floating_variables():
    """Test floating variable detection."""
    print("Testing find_free_floating_variables...")
    
    # Test with floating variable
    test_prompt1 = "Check the {$VARIABLE} please"
    result1 = PromptGenerator.find_free_floating_variables(test_prompt1)
    assert len(result1) > 0, "Should detect floating variable"
    print("  ✓ Detects floating variables")
    
    # Test with properly tagged variable
    test_prompt2 = "<tag>{$VARIABLE}</tag>"
    result2 = PromptGenerator.find_free_floating_variables(test_prompt2)
    assert len(result2) == 0, "Should not detect variable inside tags"
    print("  ✓ Ignores properly tagged variables")


def test_pretty_print():
    """Test pretty print formatting."""
    print("Testing pretty_print...")
    test_string = "This is a very long line that should be wrapped properly when printed to make it more readable for users who are viewing the output in a terminal window.\n\nThis is a new paragraph."
    result = PromptGenerator.pretty_print(test_string)
    assert len(result) > 0, "Pretty print should return formatted text"
    print("  ✓ pretty_print works correctly")


def test_metaprompt_constant():
    """Test that metaprompt is defined and has expected content."""
    print("Testing metaprompt constant...")
    assert len(PromptGenerator.METAPROMPT) > 1000, "Metaprompt should be substantial"
    assert "{{TASK}}" in PromptGenerator.METAPROMPT, "Metaprompt should have task placeholder"
    assert "<Task Instruction Example>" in PromptGenerator.METAPROMPT, "Metaprompt should have examples"
    print("  ✓ Metaprompt is properly defined")


def test_remove_floating_variables_prompt():
    """Test that the floating variables prompt is defined."""
    print("Testing remove_floating_variables_prompt constant...")
    assert len(PromptGenerator.REMOVE_FLOATING_VARIABLES_PROMPT) > 500, "Prompt should be substantial"
    assert "{$PROMPT}" in PromptGenerator.REMOVE_FLOATING_VARIABLES_PROMPT, "Should have prompt placeholder"
    print("  ✓ Remove floating variables prompt is properly defined")


def test_class_initialization():
    """Test that the class can be initialized (without API key for now)."""
    print("Testing class initialization...")
    try:
        # This should work even with a fake API key since we're not making calls
        generator = PromptGenerator("fake-api-key-for-testing")
        assert generator.model_name == "claude-3-5-sonnet-20241022", "Default model should be set"
        assert generator.client is not None, "Client should be initialized"
        print("  ✓ PromptGenerator class initializes correctly")
    except Exception as e:
        print(f"  ✗ Error initializing class: {e}")
        raise


def main():
    print("="*80)
    print("TESTING PROMPT GENERATOR SCRIPTS")
    print("="*80)
    print()
    
    tests = [
        test_extract_between_tags,
        test_remove_empty_tags,
        test_extract_variables,
        test_find_free_floating_variables,
        test_pretty_print,
        test_metaprompt_constant,
        test_remove_floating_variables_prompt,
        test_class_initialization,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
    
    print()
    print("="*80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*80)
    
    if failed == 0:
        print("\n✓ All tests passed! The scripts are working correctly.")
        print("\nTo test with the API:")
        print("1. Set ANTHROPIC_API_KEY environment variable")
        print("2. Run: ./generate_quickstart_examples.py")
        print("3. Run: ./generate_test_cases.py")
        print("4. Run: ./complex_task_verification.py")
        return 0
    else:
        print(f"\n✗ {failed} test(s) failed. Please fix the issues.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
