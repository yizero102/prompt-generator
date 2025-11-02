# Task: Draft an email responding to a customer complaint

## Task Description
Draft an email responding to a customer complaint

## Input Variables
- `{$CUSTOMER_COMPLAINT}`: The customer's complaint text
- `{$COMPANY_NAME}`: The name of the company

## Prompt Template

```
<Inputs>
{$CUSTOMER_COMPLAINT}
{$COMPANY_NAME}
</Inputs>

<Instructions Structure>
1. Present the customer complaint and company context
2. Ask the AI to analyze the complaint
3. Request a professionally-worded, empathetic response
4. Specify tone and structure requirements
</Instructions Structure>

<Instructions>
You will be drafting a professional email response to a customer complaint. Your goal is to address the customer's concerns with empathy, professionalism, and a solution-oriented approach.

Here is the customer's complaint:
<complaint>
{$CUSTOMER_COMPLAINT}
</complaint>

You are responding on behalf of:
<company>
{$COMPANY_NAME}
</company>

Before drafting your response, analyze the complaint in a scratchpad:

<scratchpad>
1. Identify the main issues or concerns raised
2. Note the customer's emotional state/tone
3. Determine what resolution or response would be appropriate
4. Consider what the customer needs to hear
</scratchpad>

Now, draft your email response following these guidelines:
- Begin with an empathetic acknowledgment of their concerns
- Apologize sincerely if appropriate (without admitting legal liability unnecessarily)
- Address each specific concern they raised
- Offer a concrete solution or next steps
- Maintain a professional, courteous tone throughout
- End with reassurance and an invitation to follow up if needed

Format your response as a complete email with:

<email>
<subject_line>
[Write an appropriate subject line]
</subject_line>

<body>
[Write the complete email body here]
</body>
</email>

Remember: The goal is to turn this negative experience into an opportunity to demonstrate excellent customer service and potentially retain the customer's business.
</Instructions>
```

## Expected Behavior
The AI should:
1. Demonstrate empathy and understanding
2. Address all specific concerns mentioned in the complaint
3. Maintain professional tone throughout
4. Offer concrete solutions or next steps
5. Use appropriate email structure and formatting
6. Balance accountability with professionalism

## Usage Example

**Input:**
```
CUSTOMER_COMPLAINT:
I ordered a laptop from your website 3 weeks ago and it still hasn't arrived. 
The tracking number doesn't work and no one responds to my emails. 
This is completely unacceptable! I need this for work.

COMPANY_NAME: TechGear Electronics
```

**Expected Output:**
A professional, empathetic email that acknowledges the frustration, apologizes for the delay and communication issues, offers to investigate the shipping status, provides a specific timeline for resolution, and possibly offers compensation.
