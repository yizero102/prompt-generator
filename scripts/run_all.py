#!/usr/bin/env python3
"""
Main orchestration script for automated prompt template generation and testing.
This script guides you through the entire process:
1. Generate a prompt template from a task description
2. Generate test cases for that template
3. Organize everything in a proper structure
"""

import os
import sys
from pathlib import Path
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(text.center(80))
    print("="*80 + "\n")

def print_step(step_num, text):
    """Print a step header"""
    print(f"\n{'─'*80}")
    print(f"STEP {step_num}: {text}")
    print(f"{'─'*80}\n")

def slugify(text):
    """Convert text to a slug suitable for directory names"""
    return text.lower().replace(' ', '-').replace('_', '-')

def ensure_directory(path):
    """Ensure a directory exists"""
    os.makedirs(path, exist_ok=True)
    return path

def main():
    print_header("AUTOMATED PROMPT TEMPLATE & TEST GENERATION")
    
    print("""
This tool will help you:
1. Generate a prompt template for any task using the metaprompt
2. Create a comprehensive test suite for that prompt
3. Organize everything in a clean project structure

Let's get started!
""")
    
    # Get task description
    if len(sys.argv) > 1:
        task_description = sys.argv[1]
        task_name = sys.argv[2] if len(sys.argv) > 2 else task_description
        variables = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    else:
        print("Enter your task description:")
        print("(e.g., 'Summarize research papers', 'Translate technical documentation')")
        task_description = input("> ").strip()
        
        if not task_description:
            print("Error: Task description cannot be empty")
            sys.exit(1)
        
        print("\nEnter a short name for this task (for directory naming):")
        print("(e.g., 'research-summary', 'tech-translation')")
        task_name = input("> ").strip()
        
        if not task_name:
            task_name = task_description
        
        print("\nEnter input variables (comma-separated), or press Enter to let AI decide:")
        print("(e.g., 'PAPER,AUDIENCE' or 'DOCUMENT,TARGET_LANGUAGE')")
        variables_input = input("> ").strip()
        variables = variables_input.split(',') if variables_input else None
    
    # Prepare directories
    project_root = Path(__file__).parent.parent
    task_slug = slugify(task_name)
    task_dir = ensure_directory(project_root / "examples" / task_slug)
    
    print_step(1, "GENERATE PROMPT TEMPLATE")
    
    print(f"Task: {task_description}")
    print(f"Directory: examples/{task_slug}/")
    if variables:
        print(f"Variables: {', '.join(variables)}")
    
    print("\nPreparing metaprompt...")
    
    # Run prompt generation
    script_path = project_root / "scripts" / "generate_prompt.py"
    cmd = [sys.executable, str(script_path), task_description]
    if variables:
        cmd.append(','.join(variables))
    
    subprocess.run(cmd)
    
    print("""
ACTION REQUIRED:
1. Copy the metaprompt output above
2. Send it to an AI assistant (Claude, GPT-4, etc.)
3. Save the <Instructions> section from AI's response
4. Save it as: """ + f"examples/{task_slug}/prompt-template.md")
    
    input("\nPress Enter when you've saved the prompt template...")
    
    print_step(2, "GENERATE TEST CASES")
    
    # Run test generation
    test_script = project_root / "scripts" / "generate_tests.py"
    test_cmd = [sys.executable, str(test_script), task_name]
    if variables:
        test_cmd.append(','.join(variables))
    
    subprocess.run(test_cmd)
    
    print(f"""
ACTION REQUIRED:
1. Review the test framework and template above
2. Create specific test cases for your prompt
3. Save them as: examples/{task_slug}/test-cases.md

Consider:
- What are typical inputs for this task?
- What edge cases might occur?
- What errors should be handled?
- What makes a successful output?
""")
    
    input("\nPress Enter when you've saved the test cases...")
    
    print_step(3, "TEST YOUR PROMPT")
    
    print(f"""
Now it's time to test your prompt template!

FOR EACH TEST CASE:
1. Take the input values from your test case
2. Insert them into your prompt template (replace {{$VARIABLE}} placeholders)
3. Send the complete prompt to an AI
4. Compare the output against expected behavior
5. Check success criteria

ITERATE IF NEEDED:
- If tests fail, refine your prompt template
- Add more specific instructions
- Adjust output format requirements
- Add examples if needed

Your files are in: examples/{task_slug}/
- prompt-template.md (the prompt)
- test-cases.md (the tests)
""")
    
    print_step(4, "SUMMARY")
    
    # Check if files exist
    prompt_file = task_dir / "prompt-template.md"
    test_file = task_dir / "test-cases.md"
    
    prompt_exists = prompt_file.exists()
    test_exists = test_file.exists()
    
    print("Project Status:")
    print(f"  Task: {task_description}")
    print(f"  Location: examples/{task_slug}/")
    print(f"  Prompt Template: {'✓ Created' if prompt_exists else '✗ Not yet created'}")
    print(f"  Test Cases: {'✓ Created' if test_exists else '✗ Not yet created'}")
    
    if prompt_exists and test_exists:
        print("\n🎉 SUCCESS! Your prompt template and tests are ready!")
        print(f"\nFiles created:")
        print(f"  - {prompt_file}")
        print(f"  - {test_file}")
    else:
        print("\n⚠ Remember to create the missing files to complete your prompt template.")
    
    print("\n" + "="*80)
    print("NEXT TASK?".center(80))
    print("="*80)
    print(f"\nRun again for a new task: python scripts/run_all.py")
    print("Or use individual scripts:")
    print("  - scripts/generate_prompt.py '<task>'")
    print("  - scripts/generate_tests.py '<task>'")

if __name__ == "__main__":
    main()
