# Prompt Template: Rate a Resume According to a Rubric

## Task
Rate a resume according to a rubric

## Inputs
- `{$RESUME}` - The resume text to be evaluated
- `{$RUBRIC}` - The evaluation rubric with criteria and scoring guidelines

## Instructions

```
You will be evaluating a resume based on a provided rubric. Your goal is to provide a fair, objective assessment of the resume's quality.

Here is the resume to evaluate:
<resume>
{$RESUME}
</resume>

Here is the rubric to use for evaluation:
<rubric>
{$RUBRIC}
</rubric>

Please evaluate the resume carefully against each criterion in the rubric. 

In <evaluation> tags, work through each rubric criterion:
1. State the criterion
2. Identify relevant evidence from the resume
3. Explain how well the resume meets this criterion
4. Assign a score based on the rubric guidelines

After evaluating all criteria, provide your final assessment in <summary> tags:
- Overall score (sum or average as specified by rubric)
- Key strengths identified
- Key areas for improvement
- Brief overall assessment

Be objective and base your evaluation only on what is present in the resume. If the rubric specifies score ranges, stay within those ranges. Quote specific parts of the resume when supporting your evaluation.
```

## Example Usage

**Input:**
- RESUME: "John Doe\nSoftware Engineer\n\nExperience:\n- Senior Developer at TechCorp (2020-2023): Led team of 5 engineers, increased system performance by 40%\n- Developer at StartupXYZ (2018-2020): Built RESTful APIs, worked with React\n\nEducation:\nBS Computer Science, State University, 2018\n\nSkills: Python, JavaScript, React, AWS"
- RUBRIC: "Rate on 1-5 scale:\n1. Relevant Experience (1-5 points)\n2. Technical Skills (1-5 points)\n3. Leadership/Impact (1-5 points)\n4. Education (1-5 points)\nTotal: /20 points"

**Expected Output:**
```
<evaluation>
Criterion 1: Relevant Experience (1-5 points)
Evidence: Candidate has 5 years of software engineering experience, including roles at both established companies and startups. Experience includes "Senior Developer at TechCorp (2020-2023)" and "Developer at StartupXYZ (2018-2020)."
Assessment: Strong relevant experience with clear progression from Developer to Senior Developer. Good variety of experience.
Score: 5/5

Criterion 2: Technical Skills (1-5 points)
Evidence: Lists "Python, JavaScript, React, AWS" and mentions building "RESTful APIs" in experience section.
Assessment: Solid technical skill set relevant to modern software development. Skills align with experience described. However, the skills list is somewhat brief.
Score: 4/5

Criterion 3: Leadership/Impact (1-5 points)
Evidence: "Led team of 5 engineers, increased system performance by 40%"
Assessment: Clear evidence of leadership and quantifiable impact. Shows ability to lead and deliver measurable results.
Score: 5/5

Criterion 4: Education (1-5 points)
Evidence: "BS Computer Science, State University, 2018"
Assessment: Relevant bachelor's degree in computer science from an accredited university.
Score: 4/5
</evaluation>

<summary>
Overall Score: 18/20 (90%)

Key Strengths:
- Strong relevant experience with clear career progression
- Demonstrated leadership and measurable impact
- Appropriate educational background
- Technical skills align with experience

Areas for Improvement:
- Could expand technical skills section with more specific technologies or certifications
- Could include more quantifiable achievements in earlier role

Overall Assessment: This is a strong resume that demonstrates solid experience, leadership capability, and technical competence. The candidate shows clear career growth and provides concrete evidence of impact.
</summary>
```
