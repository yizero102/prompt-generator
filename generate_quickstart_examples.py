#!/usr/bin/env python3
"""
Generate prompt templates for all Quickstart examples.
This script generates prompts for the examples mentioned in the README.
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
    
    output_dir = Path('examples')
    output_dir.mkdir(exist_ok=True)
    
    quickstart_examples = [
        {
            'name': 'customer_complaint_email',
            'task': 'Draft an email responding to a customer complaint',
            'variables': []
        },
        {
            'name': 'menu_item_chooser',
            'task': 'Choose an item from a menu for me given user preferences',
            'variables': []
        },
        {
            'name': 'resume_rating',
            'task': 'Rate a resume according to a rubric',
            'variables': []
        },
        {
            'name': 'scientific_explainer',
            'task': 'Explain a complex scientific concept in simple terms',
            'variables': []
        },
        {
            'name': 'marketing_strategy',
            'task': 'Design a marketing strategy for launching a new product',
            'variables': []
        }
    ]
    
    generator = PromptGenerator(api_key)
    
    for example in quickstart_examples:
        print(f"\nGenerating prompt for: {example['name']}")
        print(f"Task: {example['task']}")
        print("This may take 20-30 seconds...")
        
        try:
            result = generator.generate_prompt(example['task'], example['variables'])
            
            output_data = {
                'name': example['name'],
                'task': example['task'],
                'variables': list(result['variables']),
                'prompt_template': result['prompt_template']
            }
            
            output_file = output_dir / f"{example['name']}.json"
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"✓ Generated and saved to {output_file}")
            print(f"  Variables: {', '.join(sorted(result['variables']))}")
            
        except Exception as e:
            print(f"✗ Error generating prompt: {e}", file=sys.stderr)
            continue
    
    print("\n" + "="*80)
    print("All prompt templates generated successfully!")
    print(f"Output directory: {output_dir.absolute()}")
    print("="*80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
