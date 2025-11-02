#!/usr/bin/env python3
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from prompt_generator import QUICKSTART_EXAMPLES, generate_prompt_template, PromptTester


def main():
    print("=" * 80)
    print("PROMPT GENERATOR - QUICKSTART EXAMPLES")
    print("=" * 80)
    
    examples_dir = os.path.join(os.path.dirname(__file__), '..', 'examples')
    prompts_dir = os.path.join(examples_dir, 'prompts')
    tests_dir = os.path.join(examples_dir, 'tests')
    
    print(f"\nGenerating prompt templates for {len(QUICKSTART_EXAMPLES)} examples...")
    print("-" * 80)
    
    for i, example in enumerate(QUICKSTART_EXAMPLES, 1):
        task = example['task']
        variables = example['variables']
        
        print(f"\n{i}. Task: {task}")
        print(f"   Variables: {', '.join(variables) if variables else 'None'}")
        
        prompt_query = generate_prompt_template(task, variables)
        
        print(f"   ✓ Prompt template query generated ({len(prompt_query)} characters)")
    
    print("\n" + "=" * 80)
    print("TESTING PROMPT TEMPLATES")
    print("=" * 80)
    
    test_files = [
        'menu_chooser_tests.json',
        'resume_rater_tests.json',
        'concept_explainer_tests.json',
        'email_drafter_tests.json',
        'marketing_strategist_tests.json',
        'taskmaster_agent_tests.json'
    ]
    
    total_tests = 0
    total_passed = 0
    
    for test_file in test_files:
        test_path = os.path.join(tests_dir, test_file)
        
        if not os.path.exists(test_path):
            print(f"\n⚠ Test file not found: {test_file}")
            continue
        
        with open(test_path, 'r') as f:
            test_data = json.load(f)
        
        print(f"\n{test_data['task']}")
        print("-" * 80)
        
        tester = PromptTester()
        
        for test_case in test_data['test_cases']:
            total_tests += 1
            
            result = tester.run_test({
                'task': test_data['task'],
                'test_id': test_case['test_id'],
                'prompt_template': test_data.get('prompt_template', ''),
                'test_inputs': test_case['inputs'],
                'expected_behavior': test_case['expected_behavior'],
                'validation_criteria': test_case['validation_criteria']
            })
            
            if result['status'] == 'passed':
                total_passed += 1
                status_icon = '✓'
            else:
                status_icon = '✗'
            
            print(f"  {status_icon} {test_case['test_id']}: {test_case['description']}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total test cases: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    
    if total_tests > 0:
        success_rate = (total_passed / total_tests) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    print("\n" + "=" * 80)
    print("Note: This is a simulated test run.")
    print("For actual LLM testing, integrate with your preferred LLM API.")
    print("=" * 80)


if __name__ == '__main__':
    main()
