# Prompt Template Examples Index

This directory contains fully-developed prompt templates with comprehensive test suites. Each example demonstrates best practices for prompt engineering and testing.

## Available Examples

### 1. Menu Selection
**Path:** [menu-selection/](menu-selection/)  
**Task:** Choose an item from a menu based on user preferences  
**Variables:** `MENU`, `PREFERENCES`  
**Use Cases:**
- Restaurant ordering systems
- Product recommendation engines
- Dietary restriction handling
- Personalized suggestions

**Key Features:**
- Handles dietary restrictions (allergies, vegetarian, vegan)
- Considers taste and nutritional preferences
- Gracefully handles no suitable options
- Provides reasoning for recommendations

**Test Coverage:** 5 test cases covering basic preferences, allergies, multiple requirements, impossible requests, and spice tolerance.

---

### 2. Resume Rating
**Path:** [resume-rating/](resume-rating/)  
**Task:** Rate a resume according to a rubric  
**Variables:** `RESUME`, `RUBRIC`  
**Use Cases:**
- HR screening processes
- Candidate evaluation
- Resume review services
- Hiring pipeline automation

**Key Features:**
- Evidence-based scoring (quotes from resume)
- Flexible rubric support (weighted, scored, categorical)
- Objective assessment methodology
- Constructive feedback generation

**Test Coverage:** 5 test cases including strong resumes, entry-level candidates, problematic resumes, overqualified candidates, and weighted scoring.

---

### 3. Explain Complex Concepts
**Path:** [explain-concept/](explain-concept/)  
**Task:** Explain a complex scientific concept in simple terms  
**Variables:** `CONCEPT`, `AUDIENCE`  
**Use Cases:**
- Educational content creation
- Science communication
- Documentation simplification
- Training material development

**Key Features:**
- Audience-appropriate language
- Effective use of analogies
- Addresses common misconceptions
- Explains practical relevance

**Test Coverage:** 6 test cases across physics, biology, chemistry, medicine, computer science, and mathematics for different audience levels.

---

### 4. Customer Complaint Response
**Path:** [customer-complaint/](customer-complaint/)  
**Task:** Draft an email responding to a customer complaint  
**Variables:** `COMPLAINT`, `COMPANY_NAME`, `COMPANY_POLICIES`  
**Use Cases:**
- Customer service automation
- Email response templates
- Complaint management systems
- Customer satisfaction recovery

**Key Features:**
- Empathetic tone matching complaint severity
- Solution-oriented responses
- Professional de-escalation
- Policy-compliant resolutions

**Test Coverage:** 6 test cases covering delayed shipments, product defects, mild disappointment, hostile customers, billing errors, and service complaints.

---

### 5. Marketing Strategy
**Path:** [marketing-strategy/](marketing-strategy/)  
**Task:** Design a marketing strategy for launching a new product  
**Variables:** `PRODUCT_DESCRIPTION`, `TARGET_MARKET`, `BUDGET`, `TIMELINE`  
**Use Cases:**
- Product launch planning
- Marketing campaign design
- Go-to-market strategy
- Marketing budget allocation

**Key Features:**
- Comprehensive multi-channel strategies
- Budget allocation guidance
- Timeline/phasing recommendations
- Measurable KPIs and success metrics

**Test Coverage:** 6 test cases including consumer products, B2B SaaS, local businesses, luxury products, unspecified budgets, and repositioning scenarios.

---

### 6. Agent Design
**Path:** [agent-design/](agent-design/)  
**Task:** Design an AI agent for planning and executing tasks  
**Variables:** `AGENT_PURPOSE`, `TASK_TYPES`, `USER_PROVIDED_TOOLS`  
**Use Cases:**
- AI agent architecture
- Task automation systems
- Workflow orchestration
- Autonomous assistants

**Key Features:**
- Complete agent architecture design
- Planning and execution framework
- Tool integration patterns
- Communication protocols

**Test Coverage:** 8 test cases covering sequential tasks, information gathering, missing information, error handling, high-risk actions, complex multi-step tasks, parallel execution, and tool-agnostic designs.

---

## Quick Comparison

| Example | Complexity | Variables | Test Cases | Best For |
|---------|-----------|-----------|------------|----------|
| Menu Selection | Low | 2 | 5 | Beginners, recommendation systems |
| Resume Rating | Medium | 2 | 5 | Structured evaluation tasks |
| Explain Concept | Medium | 2 | 6 | Educational, communication |
| Customer Complaint | Medium | 3 | 6 | Customer service, email drafting |
| Marketing Strategy | High | 4 | 6 | Complex planning, strategic work |
| Agent Design | Very High | 3 | 8 | Advanced AI systems, automation |

## How to Use These Examples

### 1. As Templates
Copy and modify for similar tasks:
```bash
cp -r examples/menu-selection examples/my-selection-task
# Edit prompt-template.md and test-cases.md
```

### 2. As Learning Resources
Study to understand:
- How to structure instructions
- How to use XML tags for organization
- How to request specific output formats
- How to handle edge cases

### 3. As Testing References
Learn testing patterns:
- What scenarios to cover
- How to write success criteria
- How to structure test cases
- What metrics to track

### 4. Direct Usage
Some prompts can be used as-is:
```markdown
1. Copy prompt from examples/resume-rating/prompt-template.md
2. Replace {$RESUME} and {$RUBRIC} with your data
3. Send to AI
4. Receive structured evaluation
```

## Example Selection Guide

**Choose Menu Selection if:**
- You need simple decision-making
- You have constraints and preferences
- You want recommendations
- You're learning prompt basics

**Choose Resume Rating if:**
- You need structured evaluation
- You have clear rubrics or criteria
- You want objective assessments
- You need evidence-based outputs

**Choose Explain Concept if:**
- You need content simplification
- You have complex topics to communicate
- You want audience-appropriate explanations
- You need educational content

**Choose Customer Complaint if:**
- You need professional communication
- You want empathetic responses
- You need policy-compliant solutions
- You handle customer issues

**Choose Marketing Strategy if:**
- You need comprehensive planning
- You want multi-channel strategies
- You need budget allocation
- You want measurable outcomes

**Choose Agent Design if:**
- You're building AI systems
- You need task automation
- You want planning + execution
- You need tool integration

## Customization Tips

### Modifying for Your Needs

1. **Adjust Variables**
   - Add context-specific variables
   - Remove optional variables
   - Rename for clarity

2. **Customize Output Format**
   - Change XML tags to match your needs
   - Add or remove sections
   - Adjust structure for integration

3. **Add Domain Knowledge**
   - Include industry-specific terms
   - Add relevant constraints
   - Incorporate company policies

4. **Tune for Your Use Case**
   - Adjust tone (formal, casual, technical)
   - Add specific examples
   - Include edge cases from your domain

### Example Customization

Original (Menu Selection):
```markdown
Variables: MENU, PREFERENCES
```

Customized for Restaurant AI:
```markdown
Variables: MENU, DIETARY_RESTRICTIONS, PREVIOUS_ORDERS, BUDGET, OCCASION
```

## Contributing Your Own Examples

Have a great prompt template? Add it to the collection:

1. Create directory: `examples/your-task-name/`
2. Add `prompt-template.md` following existing format
3. Add `test-cases.md` with 5+ test cases
4. Update this INDEX.md with your example
5. Follow naming and formatting conventions

See [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) for detailed guidelines.

## Additional Resources

- **Main Documentation:** [README.md](../README.md)
- **Getting Started Guide:** [GETTING_STARTED.md](../GETTING_STARTED.md)
- **Project Structure:** [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
- **Metaprompt Template:** [templates/metaprompt.txt](../templates/metaprompt.txt)

## Need Help?

1. Start with the simplest example (Menu Selection)
2. Read the prompt template to understand structure
3. Review test cases to see what good testing looks like
4. Try modifying variables for your use case
5. Create your own tests based on the patterns

---

*All examples include both prompt templates and comprehensive test suites. Each is production-ready and demonstrates best practices in prompt engineering.*
