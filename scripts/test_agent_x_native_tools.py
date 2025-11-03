#!/usr/bin/env python3
"""
Test Agent X using native Anthropic tool calling format.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.append(str(Path(__file__).resolve().parents[1]))

from prompt_generator import get_client


# Define tools in Anthropic's native format
TOOLS = [
    {
        "name": "calculate",
        "description": "Perform mathematical calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "search_web",
        "description": "Search the web for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_file",
        "description": "Read contents of a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["filepath", "content"]
        }
    },
    {
        "name": "finish",
        "description": "Signal that the task is complete and terminate",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Summary of what was accomplished"
                }
            },
            "required": ["summary"]
        }
    }
]


@dataclass
class TestCase:
    """Test case for Agent X."""
    name: str
    task: str
    expected_tools: List[str]
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
        expected_tools=["calculate", "finish"],
        max_turns=5,
        description="Simple task requiring one calculation"
    ),
    TestCase(
        name="multi_step_calculation",
        task="Calculate the average of 10, 20, 30, and 40. You must do this in TWO separate calculations: First calculate the sum (10+20+30+40), then in a second calculation divide that sum by 4.",
        expected_tools=["calculate", "calculate", "finish"],
        max_turns=8,
        description="Multi-step calculation requiring separate tool calls"
    ),
    TestCase(
        name="search_and_summarize",
        task="Search for information about Python programming",
        expected_tools=["search_web", "finish"],
        max_turns=6,
        description="Search task"
    ),
    TestCase(
        name="file_operations",
        task="Read the file 'data.txt' and write a summary to 'summary.txt'",
        expected_tools=["read_file", "write_file", "finish"],
        max_turns=8,
        description="File operations"
    ),
]


def simulate_tool_execution(tool_name: str, tool_input: Dict[str, Any]) -> str:
    """Simulate tool execution and return mock results."""
    
    if tool_name == "calculate":
        expression = tool_input.get("expression", "")
        try:
            # Safe evaluation
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
                    raise ValueError(f"Unsupported operation")
            
            result = eval_expr(ast.parse(expression, mode='eval').body)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
    
    elif tool_name == "search_web":
        query = tool_input.get("query", "")
        return "Python is a high-level, interpreted programming language. Key features: readability, extensive libraries, dynamic typing, large community."
    
    elif tool_name == "read_file":
        filepath = tool_input.get("filepath", "")
        return f"Contents of {filepath}: Sample data - numbers 10, 20, 30, 40, 50. Pattern: increasing by 10. Sum: 150, Average: 30."
    
    elif tool_name == "write_file":
        filepath = tool_input.get("filepath", "")
        content = tool_input.get("content", "")
        return f"Successfully wrote {len(content)} characters to {filepath}"
    
    elif tool_name == "finish":
        summary = tool_input.get("summary", "")
        return f"Task completed: {summary}"
    
    return "Tool executed"


def run_agent_conversation(
    task: str,
    max_turns: int,
    client,
    model_name: str
) -> TestResult:
    """Run a multi-turn conversation with the agent using native tool calling."""
    
    system_prompt = """You are Agent X, an AI assistant that completes tasks using available tools.

CRITICAL RULES:
1. You MUST call EXACTLY ONE tool per turn - never respond with just text
2. Use previous tool results to inform your next action  
3. After completing the task, you MUST call the 'finish' tool with a summary
4. NEVER provide final answers as text - ALWAYS call 'finish' to complete

IMPORTANT: Even if you know the answer from a tool result, you must still call the 'finish' tool. Do not end your response with text - always end with a tool call."""
    
    messages = [{"role": "user", "content": task}]
    tool_calls_made = []
    finished = False
    history = []
    
    for turn in range(max_turns):
        print(f"\n--- Turn {turn + 1} ---")
        print(f"Calling LLM... (messages count: {len(messages)})")
        
        try:
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                system=system_prompt,
                tools=TOOLS,
                messages=messages
            )
            
            print(f"Response stop_reason: {response.stop_reason}")
            print(f"Content blocks: {len(response.content)}")
            
            # Extract tool use
            tool_uses = [block for block in response.content if getattr(block, "type", None) == "tool_use"]
            
            if not tool_uses:
                # No tool call found
                text_blocks = [
                    block.text for block in response.content
                    if getattr(block, "type", None) == "text"
                ]
                return TestResult(
                    test_name="",
                    passed=False,
                    turns_taken=turn + 1,
                    tool_calls=tool_calls_made,
                    error_message=f"No tool call in turn {turn + 1}. Text response: {' '.join(text_blocks)[:200]}",
                    transcript=history
                )
            
            if len(tool_uses) > 1:
                return TestResult(
                    test_name="",
                    passed=False,
                    turns_taken=turn + 1,
                    tool_calls=tool_calls_made,
                    error_message=f"Multiple tool calls in turn {turn + 1} (got {len(tool_uses)})",
                    transcript=history
                )
            
            tool_use = tool_uses[0]
            tool_name = tool_use.name
            tool_input = tool_use.input
            tool_id = tool_use.id
            
            print(f"Tool called: {tool_name}")
            print(f"Tool input: {tool_input}")
            
            tool_calls_made.append(tool_name)
            
            # Execute tool
            result = simulate_tool_execution(tool_name, tool_input)
            print(f"Tool result: {result[:100]}")
            
            # Add assistant response to messages
            messages.append({"role": "assistant", "content": response.content})
            
            # Add tool result to messages
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": result
                }]
            })
            
            history.append({
                "turn": turn + 1,
                "tool_name": tool_name,
                "tool_input": tool_input,
                "result": result
            })
            
            # Check if finished
            if tool_name == "finish":
                finished = True
                break
                
        except Exception as e:
            return TestResult(
                test_name="",
                passed=False,
                turns_taken=turn + 1,
                tool_calls=tool_calls_made,
                error_message=f"Error in turn {turn + 1}: {str(e)}",
                transcript=history
            )
    
    if not finished:
        return TestResult(
            test_name="",
            passed=False,
            turns_taken=len(history),
            tool_calls=tool_calls_made,
            error_message=f"Did not call 'finish' within {max_turns} turns",
            transcript=history
        )
    
    return TestResult(
        test_name="",
        passed=True,
        turns_taken=len(history),
        tool_calls=tool_calls_made,
        transcript=history
    )


def run_test_suite(client, model_name: str) -> tuple[List[TestResult], bool]:
    """Run all test cases."""
    
    results = []
    all_passed = True
    
    for test_case in TEST_CASES:
        print(f"\n{'='*80}")
        print(f"Test: {test_case.name}")
        print(f"Task: {test_case.task}")
        print(f"{'='*80}")
        
        result = run_agent_conversation(
            task=test_case.task,
            max_turns=test_case.max_turns,
            client=client,
            model_name=model_name
        )
        
        result.test_name = test_case.name
        results.append(result)
        
        if result.passed:
            print(f"\n✓ PASSED - {result.turns_taken} turns: {' -> '.join(result.tool_calls)}")
        else:
            print(f"\n✗ FAILED - {result.error_message}")
            all_passed = False
    
    return results, all_passed


def main():
    """Main entry point."""
    
    client, model_name = get_client()
    
    print("="*80)
    print("TESTING AGENT X WITH NATIVE TOOL CALLING")
    print("="*80)
    print(f"Model: {model_name}")
    print("="*80)
    
    results, all_passed = run_test_suite(client, model_name)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    passed_count = sum(1 for r in results if r.passed)
    print(f"Passed: {passed_count}/{len(results)}")
    
    for result in results:
        status = "✓" if result.passed else "✗"
        print(f"  {status} {result.test_name}")
        if not result.passed:
            print(f"      Error: {result.error_message}")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        
        # Save results
        output_dir = Path(__file__).parent.parent / "generated_prompts"
        output_dir.mkdir(exist_ok=True)
        results_file = output_dir / "agent_x_native_test_results.json"
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
        print(f"\nResults saved to: {results_file}")
        
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
