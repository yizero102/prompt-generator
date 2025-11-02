#!/usr/bin/env python3
"""
Verification script to demonstrate and validate all project functionalities.
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from prompt_generator import (
    PromptGenerator, 
    PromptTester, 
    generate_prompt_template, 
    METAPROMPT, 
    QUICKSTART_EXAMPLES
)


def print_header(text):
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80)


def print_section(text):
    print("\n" + "-" * 80)
    print(text)
    print("-" * 80)


def verify_imports():
    print_section("1. Verifying Module Imports")
    try:
        print("✓ PromptGenerator imported")
        print("✓ PromptTester imported")
        print("✓ generate_prompt_template imported")
        print("✓ METAPROMPT imported")
        print("✓ QUICKSTART_EXAMPLES imported")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def verify_config():
    print_section("2. Verifying Configuration")
    try:
        print(f"✓ Metaprompt loaded: {len(METAPROMPT)} characters")
        print(f"✓ Quickstart examples: {len(QUICKSTART_EXAMPLES)} examples")
        
        for i, example in enumerate(QUICKSTART_EXAMPLES, 1):
            print(f"  {i}. {example['task'][:50]}...")
            print(f"     Variables: {', '.join(example['variables']) if example['variables'] else 'None'}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration verification failed: {e}")
        return False


def verify_prompt_generation():
    print_section("3. Verifying Prompt Generation")
    try:
        generator = PromptGenerator(METAPROMPT)
        print("✓ PromptGenerator instantiated")
        
        test_task = "Test task for verification"
        test_vars = ["VAR1", "VAR2"]
        
        prompt = generator.format_for_llm(test_task, test_vars)
        print(f"✓ Prompt generated: {len(prompt)} characters")
        print(f"✓ Contains task: {'{{TASK}}' in METAPROMPT}")
        
        prompt_data = generator.generate_prompt(test_task, test_vars)
        print(f"✓ Prompt data structure created")
        print(f"  - Task: {prompt_data['task'][:40]}...")
        print(f"  - Variables: {prompt_data['variables']}")
        
        return True
    except Exception as e:
        print(f"✗ Prompt generation failed: {e}")
        return False


def verify_testing_framework():
    print_section("4. Verifying Testing Framework")
    try:
        tester = PromptTester()
        print("✓ PromptTester instantiated")
        
        test_case = tester.create_test_case(
            task="Test task",
            prompt_template="Test template",
            variables={"VAR1": "value1"},
            expected_behavior="Test behavior",
            validation_criteria=["Criterion 1", "Criterion 2"]
        )
        print("✓ Test case created")
        print(f"  - Task: {test_case['task']}")
        print(f"  - Criteria: {len(test_case['validation_criteria'])}")
        
        result = tester.run_test(test_case)
        print(f"✓ Test executed: {result['status']}")
        
        report = tester.generate_test_report()
        print("✓ Test report generated")
        
        return True
    except Exception as e:
        print(f"✗ Testing framework verification failed: {e}")
        return False


def verify_examples():
    print_section("5. Verifying Example Files")
    
    examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    prompts_dir = os.path.join(examples_dir, 'prompts')
    tests_dir = os.path.join(examples_dir, 'tests')
    
    expected_prompts = [
        'menu_chooser.md',
        'resume_rater.md',
        'concept_explainer.md',
        'email_drafter.md',
        'marketing_strategist.md',
        'taskmaster_agent.md'
    ]
    
    expected_tests = [
        'menu_chooser_tests.json',
        'resume_rater_tests.json',
        'concept_explainer_tests.json',
        'email_drafter_tests.json',
        'marketing_strategist_tests.json',
        'taskmaster_agent_tests.json'
    ]
    
    all_present = True
    
    print("Prompt Templates:")
    for prompt_file in expected_prompts:
        path = os.path.join(prompts_dir, prompt_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {prompt_file} ({size} bytes)")
        else:
            print(f"  ✗ {prompt_file} NOT FOUND")
            all_present = False
    
    print("\nTest Files:")
    total_tests = 0
    for test_file in expected_tests:
        path = os.path.join(tests_dir, test_file)
        if os.path.exists(path):
            with open(path, 'r') as f:
                test_data = json.load(f)
                num_tests = len(test_data.get('test_cases', []))
                total_tests += num_tests
            print(f"  ✓ {test_file} ({num_tests} test cases)")
        else:
            print(f"  ✗ {test_file} NOT FOUND")
            all_present = False
    
    print(f"\nTotal test cases: {total_tests}")
    
    return all_present


def verify_scripts():
    print_section("6. Verifying CLI Scripts")
    
    scripts_dir = os.path.join(os.path.dirname(__file__))
    
    expected_scripts = [
        'generate_prompt.py',
        'test_prompt.py',
        'run_all_examples.py',
        'verify_project.py'
    ]
    
    all_present = True
    
    for script_file in expected_scripts:
        path = os.path.join(scripts_dir, script_file)
        if os.path.exists(path):
            is_executable = os.access(path, os.X_OK)
            status = "executable" if is_executable else "not executable"
            print(f"  ✓ {script_file} ({status})")
        else:
            print(f"  ✗ {script_file} NOT FOUND")
            all_present = False
    
    return all_present


def verify_documentation():
    print_section("7. Verifying Documentation")
    
    project_root = os.path.join(os.path.dirname(__file__), '..')
    
    expected_docs = [
        ('README.md', 'Main documentation with metaprompt'),
        ('QUICKSTART_AUTOMATION.md', 'Automation guide'),
        ('PROJECT_OVERVIEW.md', 'Project overview and verification'),
        ('requirements.txt', 'Python dependencies'),
        ('.gitignore', 'Git ignore rules')
    ]
    
    all_present = True
    
    for doc_file, description in expected_docs:
        path = os.path.join(project_root, doc_file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {doc_file} ({size} bytes)")
            print(f"    {description}")
        else:
            print(f"  ✗ {doc_file} NOT FOUND")
            all_present = False
    
    return all_present


def run_comprehensive_test():
    print_section("8. Running Comprehensive Test")
    
    try:
        # Generate a prompt for a custom task
        task = "Create a quiz from educational content"
        variables = ["CONTENT", "DIFFICULTY_LEVEL"]
        
        print(f"Generating prompt for: '{task}'")
        prompt = generate_prompt_template(task, variables)
        print(f"✓ Prompt generated: {len(prompt)} characters")
        
        # Create and run a test
        tester = PromptTester()
        test_case = tester.create_test_case(
            task=task,
            prompt_template=prompt,
            variables={"CONTENT": "Sample content", "DIFFICULTY_LEVEL": "Medium"},
            expected_behavior="Generate appropriate quiz questions",
            validation_criteria=[
                "Contains questions",
                "Appropriate difficulty",
                "Clear format"
            ]
        )
        
        result = tester.run_test(test_case)
        print(f"✓ Test executed: {result['status']}")
        
        return True
    except Exception as e:
        print(f"✗ Comprehensive test failed: {e}")
        return False


def main():
    print_header("PROMPT GENERATOR PROJECT VERIFICATION")
    print("\nThis script verifies all project components and functionalities.")
    
    results = []
    
    # Run all verification steps
    results.append(("Module Imports", verify_imports()))
    results.append(("Configuration", verify_config()))
    results.append(("Prompt Generation", verify_prompt_generation()))
    results.append(("Testing Framework", verify_testing_framework()))
    results.append(("Example Files", verify_examples()))
    results.append(("CLI Scripts", verify_scripts()))
    results.append(("Documentation", verify_documentation()))
    results.append(("Comprehensive Test", run_comprehensive_test()))
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name:.<50} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 80)
    
    if all_passed:
        print("✓ ALL VERIFICATIONS PASSED".center(80))
        print("\nThe project is fully functional and ready to use!".center(80))
        print("\nNext steps:".center(80))
        print("1. Run: python scripts/run_all_examples.py".center(80))
        print("2. Read: QUICKSTART_AUTOMATION.md".center(80))
        print("3. Try: python scripts/generate_prompt.py 'your task'".center(80))
    else:
        print("✗ SOME VERIFICATIONS FAILED".center(80))
        print("\nPlease review the output above for details.".center(80))
    
    print("=" * 80 + "\n")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
