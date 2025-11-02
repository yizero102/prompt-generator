# Getting Started with Prompt Generator

This guide will walk you through creating your first prompt template and testing it.

## Prerequisites

- Python 3.6 or higher
- An AI assistant (Claude, GPT-4, or similar) to generate prompts

## Quick Start (5 minutes)

### Step 1: Choose Your Approach

You have three options:

**Option A: Use an Existing Example** (Fastest)
```bash
# Browse the examples
ls examples/

# View an example
cat examples/menu-selection/prompt-template.md
```

**Option B: Automated Generation** (Easiest for new prompts)
```bash
# Interactive guided mode
python scripts/run_all.py
```

**Option C: Manual Generation** (Most control)
```bash
# Generate metaprompt
python scripts/generate_prompt.py "Your task description"
```

## Detailed Walkthrough

### Creating Your First Prompt Template

Let's create a prompt for "Summarize a research paper for a general audience."

#### Step 1: Generate the Metaprompt

```bash
python scripts/generate_prompt.py "Summarize a research paper for a general audience" "PAPER,AUDIENCE"
```

This outputs a long metaprompt. Copy it.

#### Step 2: Get AI to Generate Your Prompt

1. Go to Claude.ai, ChatGPT, or your preferred AI
2. Paste the entire metaprompt
3. Wait for the AI to respond

The AI will provide:
- `<Inputs>` section listing variables
- `<Instructions Structure>` with planning
- `<Instructions>` with your complete prompt template

#### Step 3: Save Your Prompt Template

Copy the `<Instructions>` section and save it:

```bash
mkdir -p examples/research-summary
```

Create `examples/research-summary/prompt-template.md`:

```markdown
# Prompt Template: Research Paper Summary

## Task
Summarize a research paper for a general audience

## Inputs
- `{$PAPER}` - The research paper text
- `{$AUDIENCE}` - Description of target audience

## Instructions
[Paste the <Instructions> from AI here]

## Example Usage
[Add an example showing how to use the prompt]
```

### Creating Test Cases

#### Step 1: Generate Test Framework

```bash
python scripts/generate_tests.py "Research Summary" "PAPER,AUDIENCE"
```

This provides guidance and a template.

#### Step 2: Create Specific Test Cases

Create `examples/research-summary/test-cases.md`:

```markdown
# Test Cases: Research Summary

## Test Case 1: Medical Research for General Public
**Inputs:**
- PAPER: "[Sample medical research abstract]"
- AUDIENCE: "General public with no medical background"

**Expected Behavior:**
- Should avoid medical jargon
- Should explain complex terms
- Should highlight practical implications

**Success Criteria:**
- No unexplained technical terms
- Clear structure (problem, method, results, implications)
- Accessible to stated audience

[Add 4-6 more test cases...]
```

#### Step 3: Run Your Tests

For each test case:

1. Take the test inputs
2. Replace variables in your prompt template:
   ```
   Replace {$PAPER} with test PAPER value
   Replace {$AUDIENCE} with test AUDIENCE value
   ```
3. Send complete prompt to AI
4. Check if output meets success criteria
5. Document results

### Example: Full Process

Let's do a complete example for "Rate customer service interactions."

#### 1. Generate Prompt

```bash
python scripts/generate_prompt.py "Rate customer service interactions on professionalism and helpfulness" "INTERACTION,CRITERIA"
```

**Output:** Metaprompt ready for AI ✓

#### 2. Send to AI

Copy metaprompt → Paste in Claude → Get response

**AI Response:**
```
<Inputs>
{$INTERACTION}
{$CRITERIA}
</Inputs>

<Instructions Structure>
[Planning...]
</Instructions Structure>

<Instructions>
You will rate customer service interactions...
[Full prompt template]
</Instructions>
```

#### 3. Save Prompt

Create `examples/service-rating/prompt-template.md` with the instructions.

#### 4. Generate Test Framework

```bash
python scripts/generate_tests.py "Service Rating" "INTERACTION,CRITERIA"
```

#### 5. Create Tests

Create `examples/service-rating/test-cases.md`:

```markdown
## Test Case 1: Excellent Service
**Inputs:**
- INTERACTION: "Agent greeted warmly, resolved issue in 5 minutes, followed up..."
- CRITERIA: "Professionalism (1-5), Helpfulness (1-5), Speed (1-5)"

**Expected Behavior:**
- Should give high scores
- Should cite specific evidence
- Should follow scoring format

**Success Criteria:**
- All three categories scored
- Evidence quoted from interaction
- Scores justified
```

#### 6. Test It

Replace variables in prompt:
```
Your prompt template
+ Test Case 1 inputs
= Complete prompt for AI
```

Send to AI, verify output matches criteria.

#### 7. Iterate

If tests fail:
- Add more specific instructions
- Provide examples in prompt
- Clarify output format
- Re-test

## Using the Interactive Tool

For the easiest experience:

```bash
python scripts/run_all.py
```

Follow the prompts:

```
Enter your task description:
> Summarize a research paper for a general audience

Enter a short name for this task:
> research-summary

Enter input variables (comma-separated):
> PAPER,AUDIENCE

[Tool generates metaprompt]

ACTION REQUIRED:
1. Copy the metaprompt output above
2. Send it to an AI assistant
3. Save the <Instructions> section
4. Save it as: examples/research-summary/prompt-template.md

Press Enter when you've saved the prompt template...

[Tool generates test framework]

ACTION REQUIRED:
1. Review the test framework
2. Create specific test cases
3. Save them as: examples/research-summary/test-cases.md

Press Enter when you've saved the test cases...

[Summary and next steps]
```

## Tips for Success

### Writing Good Task Descriptions

✅ **Good:**
- "Rate resumes according to a rubric"
- "Explain complex scientific concepts in simple terms"
- "Draft professional email responses to customer complaints"

❌ **Too Vague:**
- "Help with hiring"
- "Make things simple"
- "Write emails"

### Choosing Variables

Think about what information the AI needs:

- **Menu Selection Task**
  - Variables: `MENU`, `PREFERENCES`
  - Not needed: Time of day, location (unless relevant)

- **Resume Rating Task**
  - Variables: `RESUME`, `RUBRIC`
  - Optional: `JOB_DESCRIPTION`, `EXPERIENCE_LEVEL`

### Creating Good Tests

Each test should:
1. **Be Specific**: Exact input values, not descriptions
2. **Be Realistic**: Use real-world examples
3. **Have Clear Criteria**: Measurable success conditions
4. **Cover Different Scenarios**: Happy path, edge cases, errors

### When to Iterate

Improve your prompt if:
- Tests fail consistently
- Output format is inconsistent
- AI misunderstands instructions
- Edge cases aren't handled
- Results vary too much

Don't iterate if:
- Only one test fails (might be the test)
- Results are good but not perfect
- Changes are stylistic only

## Common Issues

### Issue: AI generates wrong variable names

**Solution:** Specify variables explicitly:
```bash
python scripts/generate_prompt.py "Your task" "EXACT,VARIABLE,NAMES"
```

### Issue: Prompt too long

**Solution:**
- Simplify the task
- Break into multiple prompts
- Remove optional variables

### Issue: Tests keep failing

**Solution:**
1. Check if success criteria are realistic
2. Add examples to prompt template
3. Make instructions more specific
4. Clarify output format

### Issue: Inconsistent results

**Solution:**
- Add more structure (XML tags, sections)
- Specify exact output format
- Provide examples of correct output
- Add "think step-by-step" instruction

## Next Steps

1. **Create Your First Prompt**: Follow the walkthrough above
2. **Study Examples**: Look at `examples/` for patterns
3. **Test Thoroughly**: Create comprehensive test cases
4. **Share Your Work**: Add good prompts to the examples directory
5. **Iterate**: Refine based on real-world usage

## Getting Help

- Check `README.md` for full documentation
- Review `PROJECT_STRUCTURE.md` for organization details
- Study examples in `examples/` directory
- Look at existing test cases for testing patterns

## Resources

- **Main Documentation**: [README.md](README.md)
- **Project Structure**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Examples Directory**: [examples/](examples/)
- **Scripts**: [scripts/](scripts/)

---

Ready to create your first prompt? Run:

```bash
python scripts/run_all.py
```
