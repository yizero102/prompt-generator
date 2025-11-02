# Prompt Template: Draft an Email Responding to a Customer Complaint

## Task
Draft an email responding to a customer complaint

## Inputs
- `{$COMPLAINT}` - The customer's complaint or issue
- `{$COMPANY_NAME}` - The name of the company
- `{$COMPANY_POLICIES}` - Relevant company policies or available solutions (optional)

## Instructions

```
You will draft a professional email response to a customer complaint. Your goal is to address the customer's concerns with empathy, professionalism, and a solution-oriented approach.

Here is the customer's complaint:
<complaint>
{$COMPLAINT}
</complaint>

Company name:
<company>
{$COMPANY_NAME}
</company>

Relevant company policies or available solutions:
<policies>
{$COMPANY_POLICIES}
</policies>

Please draft an email response that follows these guidelines:
- Start with empathy - acknowledge the customer's frustration or inconvenience
- Apologize sincerely without being defensive or making excuses
- Address each specific concern the customer raised
- Provide a clear solution or next steps
- Be professional but warm in tone
- End on a positive note that restores confidence

First, in <analysis> tags, identify:
- The customer's main concerns
- The tone of the complaint (angry, disappointed, frustrated, etc.)
- What resolution would be appropriate
- Any policies or limitations that apply

Then, in <email> tags, write the complete email response. Include:
- An appropriate subject line
- A proper greeting
- The body of the email
- A professional closing with signature line

The email should feel personal and genuinely concerned about the customer's experience, not like a template. Aim for a tone that turns an unhappy customer into a satisfied one.
```

## Example Usage

**Input:**
- COMPLAINT: "I ordered a blue sweater (Order #12345) two weeks ago and it still hasn't arrived! The tracking hasn't updated in 5 days. I needed this for an event this weekend and now it's too late. This is completely unacceptable. I want a refund immediately."
- COMPANY_NAME: "StyleHub"
- COMPANY_POLICIES: "Standard shipping 7-10 days, can offer refund or replacement, can upgrade to express shipping for future orders"

**Expected Output:**
```
<analysis>
Main concerns:
- Order hasn't arrived (2 weeks, tracking stalled)
- Needed item for specific event (time-sensitive)
- Customer is frustrated and angry
- Requesting refund

Tone: Angry and frustrated, feels let down

Appropriate resolution:
- Apologize for shipping delay
- Investigate tracking issue
- Offer immediate refund as requested
- Offer additional gesture (discount on future order)
- Explain what went wrong if known

Applicable policies: Can offer refund, can offer express shipping for future
</analysis>

<email>
Subject: Immediate Action on Your Order #12345 - Our Sincerest Apologies

Dear Valued Customer,

I'm truly sorry for the frustration and disappointment you've experienced with your order. I completely understand how upsetting it is to not receive an item you were counting on, especially for a special event. You have every right to be frustrated, and I want to make this right immediately.

I've looked into your order #12345 for the blue sweater, and I can see that the tracking has indeed been stalled for 5 days. This is not the experience we want any of our customers to have, and I apologize that we let you down when you needed us.

Here's what I'm doing right now to resolve this:

1. I'm processing a full refund to your original payment method immediately. You should see this reflected within 2-3 business days.

2. I'm escalating the tracking issue with our shipping carrier to locate your package. If it does arrive, please feel free to keep it with our compliments for the inconvenience caused.

3. I'd like to offer you a 25% discount code (SORRY25) for your next purchase, along with complimentary express shipping, so you can shop with confidence knowing your next order will arrive on time.

I know this doesn't solve the problem for your event this weekend, and I'm genuinely sorry we couldn't be there for you when you needed us. We're reviewing our shipping processes to prevent situations like this from happening in the future.

If you have any questions or if there's anything else I can do to help, please don't hesitate to reach out to me directly.

Thank you for bringing this to our attention, and again, my sincerest apologies.

Warm regards,

[Name]
Customer Service Manager
StyleHub
[email@stylehub.com]
</email>
```
