# Task: Rate a resume according to a rubric

## Task Description
Rate a resume according to a rubric

## Input Variables
- `{$RESUME}`: The resume text to be evaluated
- `{$RUBRIC}`: The rubric containing evaluation criteria and scoring guidelines

## Prompt Template

```
<Inputs>
{$RESUME}
{$RUBRIC}
</Inputs>

<Instructions Structure>
1. Present the resume and rubric
2. Ask the AI to evaluate each criterion in the rubric
3. Require justification before scores
4. Request structured output with scores
</Instructions Structure>

<Instructions>
You will be evaluating a resume according to a specific rubric. Your goal is to provide a fair, detailed assessment based on the criteria provided.

Here is the resume to evaluate:
<resume>
{$RESUME}
</resume>

Here is the rubric you should use for evaluation:
<rubric>
{$RUBRIC}
</rubric>

Please evaluate the resume carefully against each criterion in the rubric. For each criterion:
1. First, identify relevant information from the resume
2. Then, provide your justification for the score
3. Finally, assign a score according to the rubric guidelines

Use the following format for your evaluation:

For each criterion in the rubric, write:

<criterion name="[criterion name]">
<evidence>
Quote or describe relevant parts of the resume that relate to this criterion.
</evidence>
<justification>
Explain how the evidence supports your scoring decision. Be specific about strengths and weaknesses.
</justification>
<score>[numerical score according to rubric]</score>
</criterion>

After evaluating all criteria, provide:

<overall_score>
[sum or average of scores as specified by rubric]
</overall_score>

<summary>
Provide a brief overall assessment of the resume, highlighting key strengths and areas for improvement.
</summary>
</Instructions>
```

## Expected Behavior
The AI should:
1. Carefully read and understand both the resume and rubric
2. Evaluate each criterion systematically
3. Provide evidence from the resume for each evaluation
4. Give justification BEFORE assigning scores
5. Calculate overall score correctly
6. Provide constructive feedback

## Usage Example

**Input:**
```
RESUME:
John Doe
Software Engineer
5 years of experience in Python and JavaScript
Led team of 3 developers on e-commerce project
Bachelor's in Computer Science

RUBRIC:
- Experience (0-5 points): Years of relevant experience
- Education (0-3 points): Relevant degree
- Leadership (0-2 points): Evidence of leadership
- Technical Skills (0-5 points): Breadth and depth of technical skills
Total possible: 15 points
```

**Expected Output:**
Structured evaluation with evidence, justification, and scores for each criterion, plus overall score and summary.
