#!/usr/bin/env python3
"""
Script to generate prompt templates using the metaprompt.
This simulates what would happen if you send the task to an AI with the metaprompt.
"""

import os
import sys
from pathlib import Path

def load_metaprompt():
    """Load the metaprompt template"""
    template_path = Path(__file__).parent.parent / "templates" / "metaprompt.txt"
    with open(template_path, 'r') as f:
        return f.read()

def generate_prompt_template(task, variables=None):
    """
    Generate a prompt template for a given task.
    
    Args:
        task: Description of the task to create a prompt for
        variables: Optional list of variable names to use (if None, AI should determine)
    
    Returns:
        The metaprompt with the task inserted
    """
    metaprompt = load_metaprompt()
    
    prompt_with_task = metaprompt.replace("{{TASK}}", task)
    
    if variables:
        variables_note = f"\n\nNote: Please use these input variables: {', '.join(variables)}"
        prompt_with_task += variables_note
    
    return prompt_with_task

def save_generated_prompt(output_path, content):
    """Save the generated prompt template to a file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"✓ Saved generated prompt to: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_prompt.py '<task_description>' [variable1,variable2,...]")
        print("\nExamples:")
        print("  python generate_prompt.py 'Summarize a research paper'")
        print("  python generate_prompt.py 'Rate a resume' 'RESUME,RUBRIC'")
        sys.exit(1)
    
    task = sys.argv[1]
    variables = sys.argv[2].split(',') if len(sys.argv) > 2 else None
    
    print(f"Generating prompt template for task: {task}")
    if variables:
        print(f"Using variables: {', '.join(variables)}")
    
    prompt_for_ai = generate_prompt_template(task, variables)
    
    print("\n" + "="*80)
    print("METAPROMPT READY FOR AI")
    print("="*80)
    print("\nCopy the following prompt and send it to an AI (like Claude):")
    print("\n" + "-"*80 + "\n")
    print(prompt_for_ai)
    print("\n" + "-"*80 + "\n")
    print("\nThe AI will respond with:")
    print("  <Inputs> - The input variables")
    print("  <Instructions Structure> - Planning for the structure")
    print("  <Instructions> - The complete prompt template")
    print("\nSave the <Instructions> section as your prompt template.")

if __name__ == "__main__":
    main()
