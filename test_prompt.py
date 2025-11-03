#!/usr/bin/env python3
"""
CLI tool to test prompt templates with specific variable values.
"""
import argparse
import json
import os
import sys
from prompt_generator import PromptGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Test a prompt template with specific variable values'
    )
    parser.add_argument(
        'prompt_file',
        type=str,
        help='Path to JSON file containing the prompt template'
    )
    parser.add_argument(
        '--values',
        type=str,
        help='JSON string or file path containing variable values'
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
        help='Output file path for the test result'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactively prompt for variable values'
    )
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: API key required. Set ANTHROPIC_API_KEY env var or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    with open(args.prompt_file, 'r') as f:
        prompt_data = json.load(f)
    
    prompt_template = prompt_data['prompt_template']
    variables = prompt_data['variables']
    
    print(f"Loaded prompt template with variables: {', '.join(variables)}")
    
    variable_values = {}
    
    if args.interactive:
        print("\nEnter values for each variable:")
        for var in sorted(variables):
            value = input(f"{var}: ")
            variable_values[var] = value
    elif args.values:
        if os.path.isfile(args.values):
            with open(args.values, 'r') as f:
                variable_values = json.load(f)
        else:
            variable_values = json.loads(args.values)
    else:
        print("Error: Either --values or --interactive must be specified", file=sys.stderr)
        sys.exit(1)
    
    missing_vars = set(variables) - set(variable_values.keys())
    if missing_vars:
        print(f"Error: Missing values for variables: {', '.join(missing_vars)}", file=sys.stderr)
        sys.exit(1)
    
    print("\nTesting prompt with provided values...")
    
    generator = PromptGenerator(api_key, args.model)
    result = generator.test_prompt(prompt_template, variable_values)
    
    print("\n" + "="*80)
    print("CLAUDE'S RESPONSE")
    print("="*80)
    print(PromptGenerator.pretty_print(result))
    print("="*80)
    
    if args.output:
        output_data = {
            'prompt_data': prompt_data,
            'variable_values': variable_values,
            'response': result
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nTest result saved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
