#!/usr/bin/env python3
"""
Demo script showing the prompt generator structure without requiring API calls.
This creates mock examples to demonstrate the output format.
"""
import json
from pathlib import Path


def create_mock_examples():
    """Create mock examples to show the expected output structure."""
    
    examples_dir = Path('examples')
    examples_dir.mkdir(exist_ok=True)
    
    mock_examples = [
        {
            'name': 'customer_complaint_email',
            'task': 'Draft an email responding to a customer complaint',
            'variables': ['$CUSTOMER_COMPLAINT', '$COMPANY_NAME'],
            'prompt_template': '''You will be drafting a professional email response to a customer complaint. Your goal is to acknowledge the issue, express empathy, and provide a clear path to resolution.

Here is the customer complaint:
<complaint>
{$CUSTOMER_COMPLAINT}
</complaint>

You are responding on behalf of:
<company>
{$COMPANY_NAME}
</company>

Please draft an email response that:
- Acknowledges the customer's frustration
- Apologizes for the inconvenience
- Provides a clear explanation or solution
- Offers specific next steps
- Maintains a professional and empathetic tone

Write your email response inside <email> tags.'''
        },
        {
            'name': 'menu_item_chooser',
            'task': 'Choose an item from a menu for me given user preferences',
            'variables': ['$MENU', '$PREFERENCES'],
            'prompt_template': '''You will be helping a user choose the best item from a menu based on their preferences.

Here is the menu:
<menu>
{$MENU}
</menu>

Here are the user's preferences:
<preferences>
{$PREFERENCES}
</preferences>

Please analyze the menu items against the user's preferences and recommend the best option. In your response:
1. Consider all stated preferences (dietary restrictions, taste preferences, budget, etc.)
2. Explain why your recommendation matches their preferences
3. If applicable, suggest a second choice as an alternative

Provide your recommendation inside <recommendation> tags.'''
        }
    ]
    
    for example in mock_examples:
        output_file = examples_dir / f"{example['name']}.json"
        with open(output_file, 'w') as f:
            json.dump(example, f, indent=2)
        print(f"✓ Created mock example: {output_file}")
    
    return mock_examples


def create_mock_test_results():
    """Create mock test results."""
    
    test_results_dir = Path('test_results')
    test_results_dir.mkdir(exist_ok=True)
    
    mock_test = {
        'prompt_data': {
            'name': 'customer_complaint_email',
            'task': 'Draft an email responding to a customer complaint',
            'variables': ['$CUSTOMER_COMPLAINT', '$COMPANY_NAME']
        },
        'test_values': {
            '$CUSTOMER_COMPLAINT': 'My order #12345 arrived damaged and customer service is not responding.',
            '$COMPANY_NAME': 'Acme Corp'
        },
        'response': '''<email>
Subject: Re: Your Order #12345 - Our Sincere Apologies

Dear Valued Customer,

Thank you for reaching out to us regarding order #12345. I sincerely apologize that your item arrived damaged and that you experienced difficulty reaching our customer service team. This is not the level of service we strive to provide, and I understand your frustration.

I want to make this right for you immediately. Here's what I can do:

1. I will arrange for a replacement item to be shipped to you today via express delivery at no additional cost
2. We will email you a prepaid return label for the damaged item
3. I'm also applying a 20% discount to your next purchase as an apology for this inconvenience

You should receive your replacement within 2-3 business days. I will personally monitor this order to ensure everything goes smoothly.

If you have any questions or concerns, please don't hesitate to reach out to me directly at this email address.

Again, I apologize for this experience and appreciate your patience.

Best regards,
Customer Success Team
Acme Corp
</email>'''
    }
    
    output_file = test_results_dir / 'customer_complaint_email_test.json'
    with open(output_file, 'w') as f:
        json.dump(mock_test, f, indent=2)
    
    print(f"✓ Created mock test result: {output_file}")


def main():
    print("="*80)
    print("DEMO: Prompt Generator Output Structure")
    print("="*80)
    print()
    print("This demo creates mock examples to show the expected output format")
    print("without requiring an API key.")
    print()
    
    print("Creating mock prompt templates...")
    examples = create_mock_examples()
    
    print("\nCreating mock test results...")
    create_mock_test_results()
    
    print("\n" + "="*80)
    print("Example Output Structure:")
    print("="*80)
    print("\nPrompt Template Format:")
    print("-"*80)
    print(json.dumps(examples[0], indent=2))
    print("-"*80)
    
    print("\n" + "="*80)
    print("Demo Complete!")
    print("="*80)
    print("\nGenerated files:")
    print("  - examples/customer_complaint_email.json")
    print("  - examples/menu_item_chooser.json")
    print("  - test_results/customer_complaint_email_test.json")
    print("\nTo use the real prompt generator:")
    print("  1. Set ANTHROPIC_API_KEY environment variable")
    print("  2. Run: ./generate_quickstart_examples.py")
    print("  3. Run: ./generate_test_cases.py")
    print("  4. Run: ./complex_task_verification.py")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
