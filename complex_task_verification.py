#!/usr/bin/env python3
"""
Complex task verification for the prompt generator.
This script tests the prompt generator with a complex, multi-faceted task.
"""
import os
import sys
import json
from pathlib import Path
from prompt_generator import PromptGenerator


def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Please set your API key: export ANTHROPIC_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)
    
    complex_task = """Act as an expert code reviewer for a software development team. Review code submissions for quality, security, and best practices. For each code review:
1. Analyze the code for potential bugs, security vulnerabilities, and performance issues
2. Check adherence to coding standards and best practices
3. Suggest improvements and refactoring opportunities
4. Provide constructive feedback with specific examples
5. Rate the code quality on multiple dimensions (readability, maintainability, efficiency, security)
6. Give an overall assessment with actionable recommendations
The review should be thorough but constructive, helping developers improve their skills."""
    
    print("="*80)
    print("COMPLEX TASK VERIFICATION")
    print("="*80)
    print("\nTask Description:")
    print("-" * 80)
    print(complex_task)
    print("-" * 80)
    
    print("\nGenerating prompt template...")
    print("This may take 30-40 seconds due to task complexity...")
    
    generator = PromptGenerator(api_key)
    
    try:
        result = generator.generate_prompt(complex_task, [])
        
        print("\n✓ Prompt generation successful!")
        print("\nExtracted Variables:")
        for var in sorted(result['variables']):
            print(f"  - {var}")
        
        print("\nGenerated Prompt Template:")
        print("="*80)
        print(PromptGenerator.pretty_print(result['prompt_template']))
        print("="*80)
        
        output_dir = Path('examples')
        output_dir.mkdir(exist_ok=True)
        
        output_data = {
            'name': 'complex_code_reviewer',
            'task': complex_task,
            'variables': list(result['variables']),
            'prompt_template': result['prompt_template']
        }
        
        output_file = output_dir / 'complex_code_reviewer.json'
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\nPrompt template saved to: {output_file}")
        
        print("\n" + "="*80)
        print("Testing the generated prompt with sample code...")
        print("="*80)
        
        sample_code = '''
def calculate_average(numbers):
    total = 0
    for i in range(0, len(numbers)):
        total = total + numbers[i]
    avg = total / len(numbers)
    return avg

def process_user_data(user_input):
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    return execute_query(query)
'''
        
        test_values = {}
        for var in result['variables']:
            if 'CODE' in var:
                test_values[var] = sample_code
            elif 'LANGUAGE' in var:
                test_values[var] = 'Python'
            elif 'STANDARD' in var or 'GUIDELINE' in var:
                test_values[var] = 'PEP 8 style guide, security best practices, code efficiency'
        
        if test_values:
            print("\nTest input:")
            for var, value in test_values.items():
                print(f"  {var}: {value[:100]}..." if len(value) > 100 else f"  {var}: {value}")
            
            print("\nGenerating code review...")
            response = generator.test_prompt(result['prompt_template'], test_values)
            
            print("\nClaude's Code Review:")
            print("="*80)
            print(PromptGenerator.pretty_print(response))
            print("="*80)
            
            test_results_dir = Path('test_results')
            test_results_dir.mkdir(exist_ok=True)
            
            test_output = {
                'prompt_data': output_data,
                'test_values': test_values,
                'response': response
            }
            
            test_file = test_results_dir / 'complex_code_reviewer_test.json'
            with open(test_file, 'w') as f:
                json.dump(test_output, f, indent=2)
            
            print(f"\nTest results saved to: {test_file}")
        else:
            print("\nCould not determine appropriate test values for the variables.")
            print("Manual testing recommended.")
        
        print("\n" + "="*80)
        print("VERIFICATION COMPLETE")
        print("="*80)
        print("\nSummary:")
        print(f"  ✓ Complex task prompt generated successfully")
        print(f"  ✓ Variables extracted: {', '.join(sorted(result['variables']))}")
        print(f"  ✓ Prompt template saved")
        if test_values:
            print(f"  ✓ Test case executed successfully")
        print("\nThe prompt generator is working correctly with complex tasks!")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error during verification: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
