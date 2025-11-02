#!/usr/bin/env python3
"""
CLI tool to generate prompt templates from task descriptions.
"""
import argparse
import json
import os
import sys
from prompt_generator import PromptGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Generate a prompt template from a task description'
    )
    parser.add_argument(
        'task',
        type=str,
        help='Description of the task'
    )
    parser.add_argument(
        '--variables',
        nargs='*',
        default=[],
        help='Optional list of variable names (e.g., CUSTOMER_COMPLAINT COMPANY_NAME)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='claude-3-5-sonnet-20241022',
        help='Claude model to use (default: claude-3-5-sonnet-20241022)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path for the generated prompt (JSON format)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output including raw response'
    )
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: API key required. Set ANTHROPIC_API_KEY env var or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    print(f"Generating prompt for task: {args.task}")
    if args.variables:
        print(f"Using variables: {', '.join(args.variables)}")
    else:
        print("Variables will be automatically determined by Claude")
    
    print("\nGenerating prompt template (this may take 20-30 seconds)...")
    
    generator = PromptGenerator(api_key, args.model)
    result = generator.generate_prompt(args.task, args.variables)
    
    print("\n" + "="*80)
    print("GENERATED PROMPT TEMPLATE")
    print("="*80)
    
    print("\nVariables:")
    for var in sorted(result['variables']):
        print(f"  - {var}")
    
    print("\nPrompt Template:")
    print("-" * 80)
    print(PromptGenerator.pretty_print(result['prompt_template']))
    print("-" * 80)
    
    if args.verbose:
        print("\nRaw Response:")
        print("-" * 80)
        print(PromptGenerator.pretty_print(result['raw_response']))
        print("-" * 80)
    
    if args.output:
        output_data = {
            'task': args.task,
            'variables': list(result['variables']),
            'prompt_template': result['prompt_template']
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nPrompt template saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
