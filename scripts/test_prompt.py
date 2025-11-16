#!/usr/bin/env python3
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from prompt_generator import PromptTester


def load_test_file(test_file):
    with open(test_file, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Test a prompt template with test cases')
    parser.add_argument('test_file', type=str, help='Path to test cases JSON file')
    parser.add_argument('--output', type=str, help='Output file for test results')
    parser.add_argument('--report', action='store_true', help='Generate and display test report')
    
    args = parser.parse_args()
    
    test_data = load_test_file(args.test_file)
    tester = PromptTester()
    
    print(f"\nRunning tests for: {test_data['task']}")
    print("=" * 60)
    
    for test_case in test_data['test_cases']:
        print(f"\nTest ID: {test_case['test_id']}")
        print(f"Description: {test_case['description']}")
        
        result = tester.run_test({
            'task': test_data['task'],
            'test_id': test_case['test_id'],
            'prompt_template': test_data.get('prompt_template', ''),
            'test_inputs': test_case['inputs'],
            'expected_behavior': test_case['expected_behavior'],
            'validation_criteria': test_case['validation_criteria']
        })
        
        print(f"Status: {result['status']}")
        if result.get('validation_result'):
            print(f"Passed criteria: {len(result['validation_result']['passed'])}")
            print(f"Failed criteria: {len(result['validation_result']['failed'])}")
    
    if args.report:
        print("\n" + "=" * 60)
        print(tester.generate_test_report())
    
    if args.output:
        tester.save_test_results(args.output)
        print(f"\nTest results saved to: {args.output}")


if __name__ == '__main__':
    main()
