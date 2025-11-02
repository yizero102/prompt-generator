import os
import json
from typing import List, Dict, Optional


class PromptGenerator:
    def __init__(self, metaprompt: str):
        self.metaprompt = metaprompt
    
    def generate_prompt(self, task: str, variables: Optional[List[str]] = None) -> Dict[str, any]:
        prompt = self.metaprompt.replace("{{TASK}}", task)
        
        result = {
            "task": task,
            "variables": variables if variables else [],
            "metaprompt_query": prompt,
            "instructions": None
        }
        
        return result
    
    def save_prompt(self, prompt_data: Dict[str, any], output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(prompt_data, f, indent=2)
    
    def load_prompt(self, input_path: str) -> Dict[str, any]:
        with open(input_path, 'r') as f:
            return json.load(f)
    
    def format_for_llm(self, task: str, variables: Optional[List[str]] = None) -> str:
        return self.metaprompt.replace("{{TASK}}", task)


def generate_prompt_template(task: str, variables: Optional[List[str]] = None, metaprompt: str = None) -> str:
    from .config import METAPROMPT
    
    if metaprompt is None:
        metaprompt = METAPROMPT
    
    generator = PromptGenerator(metaprompt)
    return generator.format_for_llm(task, variables)
