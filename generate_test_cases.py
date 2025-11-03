#!/usr/bin/env python3
"""
Generate test cases for each prompt template according to the Testing section.
"""
import os
import sys
import json
from pathlib import Path
from prompt_generator import PromptGenerator


def get_test_values_for_example(example_name: str, variables: list) -> dict:
    """Get test variable values for each example."""
    test_cases = {
        'customer_complaint_email': {
            '$CUSTOMER_COMPLAINT': 'I ordered a laptop from your website 3 weeks ago (Order #12345) and it still hasn\'t arrived. The tracking number shows no updates for the past 10 days. I\'ve tried calling customer service multiple times but keep getting disconnected. This is extremely frustrating and unprofessional.',
            '$COMPANY_NAME': 'TechGadgets Inc.'
        },
        'menu_item_chooser': {
            '$MENU': '''
Appetizers:
- Caesar Salad ($8)
- Buffalo Wings ($12)
- Spinach Artichoke Dip ($10)

Main Courses:
- Grilled Salmon with vegetables ($24)
- Beef Burger with fries ($16)
- Vegetarian Pasta Primavera ($18)
- Chicken Tikka Masala with rice ($20)

Desserts:
- Chocolate Lava Cake ($8)
- Fresh Fruit Platter ($6)
- Tiramisu ($9)
''',
            '$PREFERENCES': 'I am vegetarian, prefer healthy options, and I love pasta dishes. I have a moderate appetite and a budget of around $25.'
        },
        'resume_rating': {
            '$RESUME': '''
John Smith
Email: john.smith@email.com | Phone: (555) 123-4567

EDUCATION
Bachelor of Science in Computer Science, State University (2019-2023)
GPA: 3.7/4.0

EXPERIENCE
Software Engineering Intern, Tech Corp (Summer 2022)
- Developed REST APIs using Python and Flask
- Implemented automated testing with pytest
- Collaborated with team of 5 engineers

SKILLS
Programming: Python, JavaScript, Java, SQL
Tools: Git, Docker, AWS
''',
            '$RUBRIC': '''
1. Education (0-25 points): Relevant degree, GPA, coursework
2. Experience (0-35 points): Relevant work experience, internships, projects
3. Skills (0-25 points): Technical skills relevant to software engineering
4. Communication (0-15 points): Clear, professional presentation
Total: 100 points
'''
        },
        'scientific_explainer': {
            '$CONCEPT': 'Quantum Entanglement',
            '$AUDIENCE': 'a curious 10-year-old child'
        },
        'marketing_strategy': {
            '$PRODUCT': 'A new smartphone app that uses AI to help people organize their daily tasks and improve productivity',
            '$TARGET_MARKET': 'Young professionals aged 25-40 who work in fast-paced environments',
            '$BUDGET': '$50,000',
            '$TIMELINE': '3 months'
        }
    }
    
    if example_name not in test_cases:
        return {}
    
    test_data = test_cases[example_name]
    result = {}
    
    for var in variables:
        for key in test_data.keys():
            if var in key:
                result[var] = test_data[key]
                break
    
    return result


def main():
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("Please set your API key: export ANTHROPIC_API_KEY='your-key-here'", file=sys.stderr)
        sys.exit(1)
    
    examples_dir = Path('examples')
    if not examples_dir.exists():
        print(f"Error: {examples_dir} directory not found", file=sys.stderr)
        print("Please run generate_quickstart_examples.py first", file=sys.stderr)
        sys.exit(1)
    
    test_results_dir = Path('test_results')
    test_results_dir.mkdir(exist_ok=True)
    
    generator = PromptGenerator(api_key)
    
    prompt_files = list(examples_dir.glob('*.json'))
    if not prompt_files:
        print(f"Error: No prompt templates found in {examples_dir}", file=sys.stderr)
        sys.exit(1)
    
    for prompt_file in prompt_files:
        print(f"\nTesting prompt: {prompt_file.stem}")
        
        try:
            with open(prompt_file, 'r') as f:
                prompt_data = json.load(f)
            
            example_name = prompt_data['name']
            variables = prompt_data['variables']
            prompt_template = prompt_data['prompt_template']
            
            test_values = get_test_values_for_example(example_name, variables)
            
            if not test_values:
                print(f"  No test values defined for {example_name}, skipping...")
                continue
            
            print(f"  Variables: {', '.join(sorted(variables))}")
            print(f"  Testing with sample data...")
            
            result = generator.test_prompt(prompt_template, test_values)
            
            output_data = {
                'prompt_data': prompt_data,
                'test_values': test_values,
                'response': result
            }
            
            output_file = test_results_dir / f"{example_name}_test.json"
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"  ✓ Test completed and saved to {output_file}")
            print(f"  Response length: {len(result)} characters")
            
        except Exception as e:
            print(f"  ✗ Error testing prompt: {e}", file=sys.stderr)
            continue
    
    print("\n" + "="*80)
    print("All test cases generated successfully!")
    print(f"Output directory: {test_results_dir.absolute()}")
    print("="*80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
