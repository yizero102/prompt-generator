#!/usr/bin/env python3
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from prompt_generator import generate_prompt_template, METAPROMPT


def main():
    parser = argparse.ArgumentParser(description='Generate a prompt template from a task description')
    parser.add_argument('task', type=str, help='The task description')
    parser.add_argument('--variables', type=str, nargs='*', help='Optional list of input variables')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    prompt_query = generate_prompt_template(args.task, args.variables)
    
    if args.format == 'json':
        output = json.dumps({
            'task': args.task,
            'variables': args.variables or [],
            'prompt_query': prompt_query
        }, indent=2)
    else:
        output = prompt_query
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Prompt template query saved to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()
