#!/usr/bin/env python3
"""
Test script for Agent X prompt generation with multi-turn tool execution and history.

This script:
1. Generates a prompt template for Agent X
2. Tests it with multiple scenarios
3. Validates multi-turn execution with tool calls and history
4. Regenerates if tests fail
5. Iterates until all tests pass
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import get_client, generate_prompt_template, pretty_print


# Tool definitions for Agent X
SYSTEM_TOOLS = """<function>
<function_name>search_web</function_name>
<function_description>Search the web for information</function_description>
<required_argument>query (str): The search query</required_argument>
<returns>str: Search results</returns>
</function>

<function>
<function_name>read_file</function_name>
<function_description>Read contents of a file</function_description>
<required_argument>filepath (str): Path to the file to read</required_argument>
<returns>str: File contents</returns>
</function>

<function>
<function_name>write_file</function_name>
<function_description>Write content to a file</function_description>
<required_argument>filepath (str): Path to the file to write</required_argument>
<required_argument>content (str): Content to write to the file</required_argument>
<returns>str: Success confirmation message</returns>
</function>

<function>
<function_name>calculate</function_name>
<function_description>Perform mathematical calculations</function_description>
<required_argument>expression (str): The mathematical expression to evaluate</required_argument>
<returns>float: Result of the calculation</returns>
</function>

<function>
<function_name>finish</function_name>
<function_description>Signal that the task is complete and terminate the turn</function_description>
<required_argument>summary (str): Summary of what was accomplished</required_argument>
<returns>str: Completion acknowledgment</returns>
</function>"""


@dataclass
class ToolCall:
    """Represents a tool call extracted from agent output."""
    tool_name: str
    arguments: Dict[str, Any]
    raw_call: str


@dataclass
class TestCase:
    """Test case for Agent X."""
    name: str
    task: str
    expected_tool_sequence: List[str]  # Expected sequence of tool names
    max_turns: int
    description: str


@dataclass
class TestResult:
    """Result of running a test case."""
    test_name: str
    passed: bool
    turns_taken: int
    tool_calls: List[str]
    error_message: Optional[str] = None
    transcript: Optional[List[Dict]] = None


# Define test cases
TEST_CASES = [
    TestCase(
        name="simple_calculation",
        task="Calculate the result of 15 * 23 + 47",
        expected_tool_sequence=["calculate", "finish"],
        max_turns=5,
        description="Simple task requiring one calculation"
    ),
    TestCase(
        name="multi_step_calculation",
        task="Calculate the average of 10, 20, 30, and 40. First sum them, then divide by the count.",
        expected_tool_sequence=["calculate", "calculate", "finish"],
        max_turns=8,
        description="Multi-step calculation requiring multiple tool calls"
    ),
    TestCase(
        name="search_and_summarize",
        task="Search for information about Python programming and summarize the key points",
        expected_tool_sequence=["search_web", "finish"],
        max_turns=6,
        description="Search task requiring web search and summary"
    ),
    TestCase(
        name="file_operations",
        task="Read the file 'data.txt', analyze the content, and write a summary to 'summary.txt'",
        expected_tool_sequence=["read_file", "write_file", "finish"],
        max_turns=8,
        description="File operations requiring read and write"
    ),
]


def extract_tool_calls(response: str) -> List[ToolCall]:
    """Extract tool calls from agent response."""
    tool_calls = []
    
    # Pattern 1: <function_call>function_name(arg1="value1", arg2="value2")</function_call>
    pattern1 = r'<function_call>\s*(\w+)\((.*?)\)\s*</function_call>'
    matches1 = re.findall(pattern1, response, re.DOTALL)
    
    for tool_name, args_str in matches1:
        # Parse arguments
        arguments = {}
        if args_str.strip():
            # Simple parsing for key="value" patterns
            arg_pattern = r'(\w+)\s*=\s*"([^"]*)"'
            arg_matches = re.findall(arg_pattern, args_str)
            for key, value in arg_matches:
                arguments[key] = value
            
            # Also try without quotes for single arg
            if not arg_matches and args_str.strip():
                # Try pattern: arg="value" or arg='value'
                alt_pattern = r"(\w+)\s*=\s*['\"]([^'\"]*)['\"]"
                arg_matches = re.findall(alt_pattern, args_str)
                for key, value in arg_matches:
                    arguments[key] = value
        
        tool_calls.append(ToolCall(
            tool_name=tool_name,
            arguments=arguments,
            raw_call=f"{tool_name}({args_str})"
        ))
    
    # Pattern 2: <tool_call><name>function_name</name><args>...</args></tool_call>
    pattern2 = r'<tool_call>\s*<name>(\w+)</name>\s*<args>(.*?)</args>\s*</tool_call>'
    matches2 = re.findall(pattern2, response, re.DOTALL)
    
    for tool_name, args_str in matches2:
        arguments = {}
        # Try to parse as key-value pairs
        arg_pattern = r'<(\w+)>(.*?)</\1>'
        arg_matches = re.findall(arg_pattern, args_str)
        for key, value in arg_matches:
            arguments[key] = value.strip()
        
        tool_calls.append(ToolCall(
            tool_name=tool_name,
            arguments=arguments,
            raw_call=f"{tool_name}: {args_str}"
        ))
    
    # Pattern 3: Look for common function call patterns outside tags
    if not tool_calls:
        # Try: function_name(arg="value") without tags
        pattern3 = r'\b(search_web|read_file|write_file|calculate|finish)\s*\(([^)]*)\)'
        matches3 = re.findall(pattern3, response, re.IGNORECASE)
        for tool_name, args_str in matches3:
            arguments = {}
            if args_str.strip():
                arg_pattern = r'(\w+)\s*=\s*["\']([^"\']*)["\']'
                arg_matches = re.findall(arg_pattern, args_str)
                for key, value in arg_matches:
                    arguments[key] = value
            
            tool_calls.append(ToolCall(
                tool_name=tool_name.lower(),
                arguments=arguments,
                raw_call=f"{tool_name}({args_str})"
            ))
    
    return tool_calls


def simulate_tool_execution(tool_call: ToolCall) -> str:
    """Simulate tool execution and return mock results."""
    tool_name = tool_call.tool_name
    args = tool_call.arguments
    
    if tool_name == "calculate":
        expression = args.get("expression", "")
        try:
            # Simple evaluation (in production, use a safe evaluator)
            result = eval(expression, {"__builtins__": {}}, {})
            return f"Calculation result: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    elif tool_name == "search_web":
        query = args.get("query", "")
        return f"Search results for '{query}': Python is a high-level programming language known for its simplicity and readability. Key features include dynamic typing, automatic memory management, and extensive standard library."
    
    elif tool_name == "read_file":
        filepath = args.get("filepath", "")
        return f"Contents of {filepath}: Sample data with numbers: 10, 20, 30, 40, 50. Analysis shows positive trend."
    
    elif tool_name == "write_file":
        filepath = args.get("filepath", "")
        content = args.get("content", "")
        return f"Successfully wrote {len(content)} characters to {filepath}"
    
    elif tool_name == "finish":
        summary = args.get("summary", "")
        return f"Task completed: {summary}"
    
    else:
        return f"Unknown tool: {tool_name}"


def run_agent_conversation(
    prompt_template: str,
    task: str,
    max_turns: int,
    client,
    model_name: str
) -> TestResult:
    """Run a multi-turn conversation with the agent."""
    
    history = []
    tool_calls_made = []
    finished = False
    
    # Fill in the prompt template
    filled_prompt = prompt_template.replace("{$TASK}", task)
    filled_prompt = filled_prompt.replace("{$TOOLS}", SYSTEM_TOOLS)
    
    for turn in range(max_turns):
        # Build history context
        if history:
            history_str = "\n\n".join([
                f"Previous turn {i+1}:\nYour response: {h['response']}\nTool result: {h['result']}"
                for i, h in enumerate(history)
            ])
            current_prompt = filled_prompt + f"\n\n<conversation_history>\n{history_str}\n</conversation_history>"
        else:
            current_prompt = filled_prompt
        
        # Call the LLM
        try:
            message = client.messages.create(
                model=model_name,
                max_tokens=2048,
                temperature=0,
                messages=[{"role": "user", "content": current_prompt}]
            )
            
            # Extract response
            response_text = "\n\n".join(
                block.text for block in message.content
                if getattr(block, "type", None) == "text" and getattr(block, "text", None)
            )
            
        except Exception as e:
            return TestResult(
                test_name="",
                passed=False,
                turns_taken=turn + 1,
                tool_calls=tool_calls_made,
                error_message=f"LLM call failed: {str(e)}",
                transcript=history
            )
        
        # Debug: print response
        print(f"\nTurn {turn + 1} response:")
        print("-" * 40)
        print(response_text[:500] if len(response_text) > 500 else response_text)
        if len(response_text) > 500:
            print("...")
        print("-" * 40)
        
        # Extract tool calls
        tool_calls = extract_tool_calls(response_text)
        
        # Validate: should call exactly ONE tool per turn
        if len(tool_calls) == 0:
            return TestResult(
                test_name="",
                passed=False,
                turns_taken=turn + 1,
                tool_calls=tool_calls_made,
                error_message=f"No tool call found in turn {turn + 1}",
                transcript=history
            )
        
        if len(tool_calls) > 1:
            return TestResult(
                test_name="",
                passed=False,
                turns_taken=turn + 1,
                tool_calls=tool_calls_made,
                error_message=f"Multiple tool calls found in turn {turn + 1} (expected 1, got {len(tool_calls)})",
                transcript=history
            )
        
        tool_call = tool_calls[0]
        tool_calls_made.append(tool_call.tool_name)
        
        # Execute tool
        result = simulate_tool_execution(tool_call)
        
        # Record history
        history.append({
            "turn": turn + 1,
            "response": response_text,
            "tool_call": tool_call.tool_name,
            "tool_args": tool_call.arguments,
            "result": result
        })
        
        # Check if finished
        if tool_call.tool_name == "finish":
            finished = True
            break
    
    # Validate result
    if not finished:
        return TestResult(
            test_name="",
            passed=False,
            turns_taken=len(history),
            tool_calls=tool_calls_made,
            error_message=f"Agent did not call 'finish' within {max_turns} turns",
            transcript=history
        )
    
    return TestResult(
        test_name="",
        passed=True,
        turns_taken=len(history),
        tool_calls=tool_calls_made,
        transcript=history
    )


def validate_prompt_template(prompt: str) -> tuple[bool, str]:
    """Validate that the generated prompt has required characteristics."""
    
    issues = []
    
    # Check for tool definitions variable
    if "{$TOOLS}" not in prompt and "{$FUNCTIONS}" not in prompt:
        issues.append("Prompt does not include a variable for tool definitions ({$TOOLS} or {$FUNCTIONS})")
    
    # Check for task variable
    if "{$TASK}" not in prompt:
        issues.append("Prompt does not include a task variable ({$TASK})")
    
    # Check for mentions of tool calling
    tool_keywords = ["function_call", "tool_call", "function", "tool"]
    if not any(keyword in prompt.lower() for keyword in tool_keywords):
        issues.append("Prompt does not mention tool/function calling")
    
    # Check for finish instruction
    if "finish" not in prompt.lower():
        issues.append("Prompt does not mention the 'finish' tool or completion signal")
    
    # Check for one-at-a-time instruction
    one_at_time_keywords = ["one tool", "single tool", "one function", "one at a time"]
    if not any(keyword in prompt.lower() for keyword in one_at_time_keywords):
        issues.append("Prompt does not explicitly state to call one tool at a time")
    
    if issues:
        return False, "; ".join(issues)
    
    return True, "Prompt structure is valid"


def run_test_suite(prompt_template: str, client, model_name: str) -> tuple[List[TestResult], bool]:
    """Run all test cases and return results."""
    
    results = []
    all_passed = True
    
    for test_case in TEST_CASES:
        print(f"\n{'='*80}")
        print(f"Running test: {test_case.name}")
        print(f"Description: {test_case.description}")
        print(f"Task: {test_case.task}")
        print(f"{'='*80}")
        
        result = run_agent_conversation(
            prompt_template=prompt_template,
            task=test_case.task,
            max_turns=test_case.max_turns,
            client=client,
            model_name=model_name
        )
        
        result.test_name = test_case.name
        results.append(result)
        
        if result.passed:
            print(f"✓ PASSED - {result.turns_taken} turns, tools: {' -> '.join(result.tool_calls)}")
        else:
            print(f"✗ FAILED - {result.error_message}")
            all_passed = False
        
        # Show transcript
        if result.transcript:
            print("\nTranscript:")
            for entry in result.transcript:
                print(f"  Turn {entry['turn']}: {entry['tool_call']} -> {entry['result'][:100]}...")
    
    return results, all_passed


def generate_and_test_agent_x(max_attempts: int = 3) -> bool:
    """Generate Agent X prompt and test it, regenerating if needed."""
    
    client, model_name = get_client()
    
    # Task description for Agent X
    task_description = """An autonomous agent named 'Agent X' that can plan and execute tasks using system tools. 

The agent must:
1. Receive a task description and available system tools
2. In each turn, call EXACTLY ONE tool using the format: <function_call>tool_name(arg1="value1", arg2="value2")</function_call>
3. After each turn, receive the tool result in <function_result> tags
4. Continue calling tools sequentially based on previous results
5. When the task is complete, call the 'finish' tool with a summary

The prompt should include explicit examples showing:
- How to analyze the task and plan tool usage
- The exact format for making a single tool call
- How to use previous tool results to decide the next action
- How conversation history is provided and should be used
- When and how to call the 'finish' tool

Format requirement: Tool calls MUST be wrapped in <function_call></function_call> tags and follow the pattern: function_name(arg="value")"""
    
    for attempt in range(1, max_attempts + 1):
        print(f"\n{'#'*80}")
        print(f"# ATTEMPT {attempt}/{max_attempts}: Generating Agent X prompt template")
        print(f"{'#'*80}\n")
        
        # Generate prompt
        try:
            generated = generate_prompt_template(
                task=task_description,
                requested_variables=["TASK", "TOOLS"],
                client=client,
                model_name=model_name
            )
        except Exception as e:
            print(f"✗ Generation failed: {str(e)}")
            continue
        
        prompt = generated.final_prompt_template
        
        print("Generated prompt template:")
        print("-" * 80)
        print(pretty_print(prompt[:1000]))
        print("...")
        print(pretty_print(prompt[-500:]))
        print("-" * 80)
        
        # Validate structure
        is_valid, validation_msg = validate_prompt_template(prompt)
        print(f"\nPrompt validation: {validation_msg}")
        
        if not is_valid:
            print(f"✗ Prompt structure is invalid, regenerating...")
            continue
        
        # Run test suite
        print("\n" + "="*80)
        print("RUNNING TEST SUITE")
        print("="*80)
        
        results, all_passed = run_test_suite(prompt, client, model_name)
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        passed_count = sum(1 for r in results if r.passed)
        print(f"Passed: {passed_count}/{len(results)}")
        
        for result in results:
            status = "✓" if result.passed else "✗"
            print(f"  {status} {result.test_name}: {result.error_message or 'OK'}")
        
        if all_passed:
            print("\n" + "🎉" * 40)
            print("ALL TESTS PASSED!")
            print("🎉" * 40)
            
            # Save the successful prompt
            output_dir = Path(__file__).parent.parent / "generated_prompts"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "agent_x_prompt.txt"
            output_file.write_text(prompt)
            print(f"\nSaved successful prompt to: {output_file}")
            
            # Save test results
            results_file = output_dir / "agent_x_test_results.json"
            results_data = {
                "attempt": attempt,
                "all_passed": all_passed,
                "tests": [
                    {
                        "name": r.test_name,
                        "passed": r.passed,
                        "turns": r.turns_taken,
                        "tool_calls": r.tool_calls,
                        "error": r.error_message
                    }
                    for r in results
                ]
            }
            results_file.write_text(json.dumps(results_data, indent=2))
            print(f"Saved test results to: {results_file}")
            
            return True
        
        else:
            print(f"\n✗ Some tests failed. Regenerating prompt...")
    
    print("\n" + "="*80)
    print(f"FAILED: Could not generate a passing prompt in {max_attempts} attempts")
    print("="*80)
    return False


def main():
    """Main entry point."""
    success = generate_and_test_agent_x(max_attempts=3)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
