# Test Cases: Resume Rating

## Test Case 1: Strong Resume with Clear Metrics
**Inputs:**
- RESUME: "Sarah Johnson\nProduct Manager\n\nExperience:\n- Senior PM at BigTech (2020-2023): Launched 3 products, $10M revenue, 95% customer satisfaction\n- PM at MidSize (2018-2020): Managed roadmap for 50K users\n\nEducation: MBA Harvard 2018, BS Engineering MIT 2016\n\nSkills: Agile, SQL, Tableau, Market Research"
- RUBRIC: "Rate 1-5 scale:\n1. Experience Relevance (1-5)\n2. Impact/Metrics (1-5)\n3. Education (1-5)\n4. Skills (1-5)\nTotal: /20"

**Expected Behavior:**
- Should recognize strong quantifiable metrics
- Should note prestigious education
- Should give high scores (18-20 range)

**Success Criteria:**
- Impact/Metrics score is 5/5
- Education score is 4-5/5
- Total score is 17+
- Mentions specific metrics in evaluation

## Test Case 2: Entry-Level Resume
**Inputs:**
- RESUME: "Alex Kim\nRecent Graduate\n\nEducation: BS Biology, Local College, 2023, GPA 3.4\n\nInternship: Lab Assistant at Research Center (Summer 2022): Assisted with experiments\n\nSkills: Microsoft Office, Basic Python"
- RUBRIC: "Entry-level rubric, 1-5 scale:\n1. Education (1-5)\n2. Relevant Experience (1-5)\n3. Skills (1-5)\n4. Potential (1-5)\nTotal: /20"

**Expected Behavior:**
- Should evaluate appropriately for entry-level
- Should not penalize for limited experience
- Should focus on potential and foundational skills
- Score should be moderate (10-14 range)

**Success Criteria:**
- Education score is reasonable (3-4)
- Evaluation acknowledges entry-level context
- Doesn't unfairly compare to senior candidates
- Mentions potential or growth areas

## Test Case 3: Resume with Gaps and Issues
**Inputs:**
- RESUME: "Name: Chris\nJob wanted: Management\n\nWorked at some places 2015-2022\nGood at computers and talking to people"
- RUBRIC: "Rate 1-5:\n1. Professional Presentation (1-5)\n2. Clear Experience (1-5)\n3. Specific Skills (1-5)\n4. Completeness (1-5)\nTotal: /20"

**Expected Behavior:**
- Should identify lack of detail
- Should note formatting issues
- Should give low scores (5-10 range)
- Should be constructive in feedback

**Success Criteria:**
- Low scores reflect quality issues
- Specific problems identified (vague dates, missing details)
- Feedback is constructive, not harsh
- Points out what's missing

## Test Case 4: Overqualified Resume
**Inputs:**
- RESUME: "Dr. Patricia Brown, PhD\n25 years experience as CTO\nPhD Computer Science Stanford, MS MIT, BS CalTech\n50+ publications, 10 patents\nExperience: CTO at Fortune 500 (15 years), VP Eng (10 years)"
- RUBRIC: "Junior Developer Position - Rate 1-5:\n1. Appropriate Experience Level (1-5)\n2. Technical Skills (1-5)\n3. Team Fit (1-5)\n4. Growth Potential (1-5)\nTotal: /20"

**Expected Behavior:**
- Should recognize overqualification
- Should note potential fit issues for junior role
- Should be objective about mismatch
- Score may be mixed (high skills, low fit)

**Success Criteria:**
- Acknowledges overqualification
- Notes potential concerns (retention, team dynamics)
- Still objective about candidate's qualifications
- Addresses role-candidate mismatch

## Test Case 5: Rubric with Weighted Criteria
**Inputs:**
- RESUME: "Maria Garcia\nData Scientist\n\nExperience: 3 years at AnalyticsCo\nEducation: MS Statistics\nSkills: Python, R, SQL, TensorFlow\nProjects: Built ML model with 95% accuracy"
- RUBRIC: "Weighted scoring:\n1. Technical Skills (×3): Rate 1-5, multiply by 3\n2. Experience (×2): Rate 1-5, multiply by 2\n3. Education (×1): Rate 1-5, multiply by 1\nTotal: /30 points"

**Expected Behavior:**
- Should correctly apply weighted scoring
- Should multiply each score by weight
- Should sum to correct total
- Should explain weighting in summary

**Success Criteria:**
- Math is correct (proper multiplication and addition)
- Each criterion shows base score and weighted score
- Final total uses weighted scores
- Evaluation mentions weighting system

## Test Metrics

For each test case, evaluate:
1. **Scoring Accuracy**: Are scores justified by evidence?
2. **Rubric Adherence**: Does it follow the rubric exactly?
3. **Evidence-Based**: Does it quote/reference resume content?
4. **Output Format**: Proper use of evaluation and summary tags?
5. **Mathematical Accuracy**: Correct score calculations?
6. **Objectivity**: Fair and unbiased assessment?

## Passing Criteria
- All test cases must have correct mathematical scoring
- Evidence must be cited from resume for each criterion
- Output format must be consistent across all tests
- No subjective bias in scoring
- Constructive feedback in all cases
