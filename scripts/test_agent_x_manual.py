#!/usr/bin/env python3
"""
Test the manually crafted Agent X prompt with real LLM calls.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import get_client


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
        task="Search for information about Python programming and provide key insights",
        expected_tool_sequence=["search_web", "finish"],
        max_turns=6,
        description="Search task requiring web search"
    ),
    TestCase(
        name="file_operations",
        task="Read the file 'data.txt' and write a summary to 'summary.txt'",
        expected_tool_sequence=["read_file", "write_file", "finish"],
        max_turns=8,
        description="File operations requiring read and write"
    ),
]


def extract_tool_calls(response: str) -> List[ToolCall]:
    """Extract tool calls from agent response."""
    tool_calls = []
    
    # Pattern: <function_call>function_name(arg1="value1", arg2="value2")</function_call>
    pattern = r'<function_call>\s*(\w+)\s*\(([^)]*)\)\s*</function_call>'
    matches = re.findall(pattern, response, re.DOTALL)
    
    for tool_name, args_str in matches:
        # Parse arguments
        arguments = {}
        if args_str.strip():
            # Parse key="value" patterns
            arg_pattern = r'(\w+)\s*=\s*["\']([^"\']*)["\']'
            arg_matches = re.findall(arg_pattern, args_str)
            for key, value in arg_matches:
                arguments[key] = value
        
        tool_calls.append(ToolCall(
            tool_name=tool_name,
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
            # Safe evaluation using only basic math
            import ast
            import operator
            
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.USub: operator.neg,
            }
            
            def eval_expr(node):
                if isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.BinOp):
                    return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
                elif isinstance(node, ast.UnaryOp):
                    return ops[type(node.op)](eval_expr(node.operand))
                else:
                    raise ValueError(f"Unsupported operation: {type(node)}")
            
            result = eval_expr(ast.parse(expression, mode='eval').body)
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
    
    elif tool_name == "search_web":
        query = args.get("query", "")
        return f"Search results for '{query}': Python is a high-level, interpreted programming language known for its simplicity and readability. Key features include: dynamic typing, automatic memory management, extensive standard library, support for multiple programming paradigms (object-oriented, functional, procedural), and a large ecosystem of third-party packages."
    
    elif tool_name == "read_file":
        filepath = args.get("filepath", "")
        return f"Contents of {filepath}: Sample data with numbers: 10, 20, 30, 40, 50. The data shows a consistent pattern with values increasing by 10 each time. Total sum is 150. Average value is 30."
    
    elif tool_name == "write_file":
        filepath = args.get("filepath", "")
        content = args.get("content", "")
        return f"Successfully wrote {len(content)} characters to {filepath}"
    
    elif tool_name == "finish":
        summary = args.get("summary", "")
        return f"Task completed. Summary: {summary}"
    
    else:
        return f"Error: Unknown tool '{tool_name}'"


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
    filled_prompt = filled_prompt.replace("{$HISTORY}", "")  # No history for first turn
    
    for turn in range(max_turns):
        # Build history context for subsequent turns
        if history:
            history_str = "\n\n<conversation_history>\n"
            for i, h in enumerate(history):
                history_str += f"Turn {i+1}:\n"
                history_str += f"Tool called: {h['tool_call']}\n"
                history_str += f"Arguments: {h['tool_args']}\n"
                history_str += f"<function_result>{h['result']}</function_result>\n\n"
            history_str += "</conversation_history>"
            
            current_prompt = filled_prompt.replace("{$HISTORY}", history_str)
        else:
            current_prompt = filled_prompt
        
        # Call the LLM
        try:
            print(f"\nCalling LLM for turn {turn + 1}...")
            print(f"Prompt length: {len(current_prompt)} chars")
            
            message = client.messages.create(
                model=model_name,
                max_tokens=2048,
                temperature=0,
                messages=[{"role": "user", "content": current_prompt}]
            )
            
            print(f"Response received. Content blocks: {len(message.content)}")
            for i, block in enumerate(message.content):
                block_type = getattr(block, 'type', 'unknown')
                print(f"  Block {i}: type={block_type}, has_text={hasattr(block, 'text')}, has_thinking={hasattr(block, 'thinking')}")
                if block_type == "tool_use":
                    print(f"    Tool use block found! name={getattr(block, 'name', 'N/A')}, input={getattr(block, 'input', 'N/A')}")
            
            # Extract response - try text blocks first, then thinking blocks
            text_blocks = [
                block.text for block in message.content
                if getattr(block, "type", None) == "text" and getattr(block, "text", None)
            ]
            
            thinking_blocks = [
                block.thinking for block in message.content
                if getattr(block, "type", None) == "thinking" and getattr(block, "thinking", None)
            ]
            
            # Check for tool_use blocks (native Anthropic format)
            tool_use_blocks = [
                block for block in message.content
                if getattr(block, "type", None) == "tool_use"
            ]
            
            # If there are tool_use blocks, convert them to function_call format
            if tool_use_blocks:
                for tool_block in tool_use_blocks:
                    tool_name = getattr(tool_block, "name", "")
                    tool_input = getattr(tool_block, "input", {})
                    # Convert to function call format
                    args_str = ", ".join(f'{k}="{v}"' for k, v in tool_input.items())
                    func_call = f"<function_call>{tool_name}({args_str})</function_call>"
                    text_blocks.append(func_call)
            
            # Use text blocks if available, otherwise use thinking blocks
            if text_blocks:
                response_text = "\n\n".join(text_blocks)
            elif thinking_blocks:
                response_text = "\n\n".join(thinking_blocks)
            else:
                response_text = ""
            
            print(f"Extracted response text length: {len(response_text)} chars (from {'text' if text_blocks else 'thinking' if thinking_blocks else 'none'})")
            
        except Exception as e:
            return TestResult(
                test_name="",
                passed=False,
                turns_taken=turn + 1,
                tool_calls=tool_calls_made,
                error_message=f"LLM call failed: {str(e)}",
                transcript=history
            )
        
        print(f"\nTurn {turn + 1} response (first 400 chars):")
        print("-" * 60)
        print(response_text[:400])
        if len(response_text) > 400:
            print("...")
        print("-" * 60)
        
        # Extract tool calls
        tool_calls = extract_tool_calls(response_text)
        
        # Validate: should call exactly ONE tool per turn
        if len(tool_calls) == 0:
            return TestResult(
                test_name="",
                passed=False,
                turns_taken=turn + 1,
                tool_calls=tool_calls_made,
                error_message=f"No tool call found in turn {turn + 1}. Response: {response_text[:200]}",
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
        print(f"Tool called: {tool_call.tool_name} with args: {tool_call.arguments}")
        
        # Execute tool
        result = simulate_tool_execution(tool_call)
        print(f"Tool result: {result[:100]}...")
        
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


def run_test_suite(prompt_template: str, client, model_name: str) -> tuple[List[TestResult], bool]:
    """Run all test cases and return results."""
    
    results = []
    all_passed = True
    
    for test_case in TEST_CASES:
        print(f"\n{'='*80}")
        print(f"Test: {test_case.name}")
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
            print(f"\n✓ PASSED - {result.turns_taken} turns, tools: {' -> '.join(result.tool_calls)}")
        else:
            print(f"\n✗ FAILED - {result.error_message}")
            all_passed = False
    
    return results, all_passed


def main():
    """Main entry point."""
    
    client, model_name = get_client()
    
    # Load the manual prompt
    prompt_file = Path(__file__).parent.parent / "generated_prompts" / "agent_x_prompt_manual.txt"
    if not prompt_file.exists():
        print(f"Error: Prompt file not found: {prompt_file}")
        sys.exit(1)
    
    prompt_template = prompt_file.read_text()
    
    print("="*80)
    print("TESTING AGENT X PROMPT WITH REAL LLM")
    print("="*80)
    print(f"Using model: {model_name}")
    print(f"Prompt file: {prompt_file}")
    print("="*80)
    
    # Run test suite
    results, all_passed = run_test_suite(prompt_template, client, model_name)
    
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
        
        # Save test results
        output_dir = Path(__file__).parent.parent / "generated_prompts"
        results_file = output_dir / "agent_x_test_results.json"
        results_data = {
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
        print(f"\nSaved test results to: {results_file}")
        
        sys.exit(0)
    else:
        print("\n" + "="*80)
        print("SOME TESTS FAILED")
        print("="*80)
        sys.exit(1)


if __name__ == "__main__":
    main()
