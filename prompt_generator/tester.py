import json
from typing import List, Dict, Optional


class PromptTester:
    def __init__(self):
        self.test_results = []
    
    def create_test_case(self, task: str, prompt_template: str, variables: Dict[str, str], 
                        expected_behavior: str, validation_criteria: List[str]) -> Dict:
        return {
            "task": task,
            "prompt_template": prompt_template,
            "test_inputs": variables,
            "expected_behavior": expected_behavior,
            "validation_criteria": validation_criteria,
            "status": "pending"
        }
    
    def validate_output(self, output: str, validation_criteria: List[str]) -> Dict[str, any]:
        results = {
            "passed": [],
            "failed": [],
            "overall_passed": True
        }
        
        for criterion in validation_criteria:
            if self._check_criterion(output, criterion):
                results["passed"].append(criterion)
            else:
                results["failed"].append(criterion)
                results["overall_passed"] = False
        
        return results
    
    def _check_criterion(self, output: str, criterion: str) -> bool:
        criterion_lower = criterion.lower()
        output_lower = output.lower()
        
        if "contains" in criterion_lower:
            parts = criterion.split("'")
            if len(parts) >= 2:
                search_term = parts[1]
                return search_term.lower() in output_lower
        
        if "format" in criterion_lower and "xml" in criterion_lower:
            return "<" in output and ">" in output
        
        if "length" in criterion_lower:
            if "minimum" in criterion_lower or "at least" in criterion_lower:
                try:
                    words = output.split()
                    return len(words) >= 50
                except:
                    return False
        
        return True
    
    def run_test(self, test_case: Dict, llm_output: Optional[str] = None) -> Dict:
        if llm_output is None:
            llm_output = self._simulate_llm_response(test_case)
        
        validation_result = self.validate_output(llm_output, test_case["validation_criteria"])
        
        test_case["llm_output"] = llm_output
        test_case["validation_result"] = validation_result
        test_case["status"] = "passed" if validation_result["overall_passed"] else "failed"
        
        self.test_results.append(test_case)
        
        return test_case
    
    def _simulate_llm_response(self, test_case: Dict) -> str:
        return f"Simulated LLM response for task: {test_case['task']}"
    
    def save_test_results(self, output_path: str):
        with open(output_path, 'w') as f:
            json.dump(self.test_results, f, indent=2)
    
    def load_test_results(self, input_path: str) -> List[Dict]:
        with open(input_path, 'r') as f:
            self.test_results = json.load(f)
        return self.test_results
    
    def generate_test_report(self) -> str:
        if not self.test_results:
            return "No test results available."
        
        total = len(self.test_results)
        passed = sum(1 for t in self.test_results if t["status"] == "passed")
        failed = total - passed
        
        report = f"""
Test Report
===========
Total Tests: {total}
Passed: {passed}
Failed: {failed}
Success Rate: {(passed/total)*100:.1f}%

Detailed Results:
"""
        
        for i, test in enumerate(self.test_results, 1):
            report += f"\n{i}. Task: {test['task']}\n"
            report += f"   Status: {test['status']}\n"
            if test.get('validation_result'):
                report += f"   Passed Criteria: {len(test['validation_result']['passed'])}\n"
                report += f"   Failed Criteria: {len(test['validation_result']['failed'])}\n"
        
        return report
