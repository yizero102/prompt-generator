# Task: Design a marketing strategy for launching a new product

## Task Description
Design a marketing strategy for launching a new product

## Input Variables
- `{$PRODUCT_DESCRIPTION}`: Detailed description of the product
- `{$TARGET_AUDIENCE}`: Description of the target market/audience
- `{$BUDGET}`: Available marketing budget

## Prompt Template

```
<Inputs>
{$PRODUCT_DESCRIPTION}
{$TARGET_AUDIENCE}
{$BUDGET}
</Inputs>

<Instructions Structure>
1. Present product, audience, and budget constraints
2. Request strategic analysis and planning
3. Require comprehensive strategy with multiple channels
4. Ask for timeline and success metrics
</Instructions Structure>

<Instructions>
You will be designing a comprehensive marketing strategy for launching a new product. Your strategy should be tailored to the specific product, audience, and budget constraints provided.

Here is the product information:
<product>
{$PRODUCT_DESCRIPTION}
</product>

Here is the target audience:
<audience>
{$TARGET_AUDIENCE}
</audience>

Here is the available budget:
<budget>
{$BUDGET}
</budget>

Create a comprehensive marketing strategy that includes:

<strategy_overview>
Provide a high-level summary of your marketing approach and key strategic themes.
</strategy_overview>

<market_positioning>
Explain how the product should be positioned in the market and what key messages should be emphasized.
Include:
- Unique value proposition
- Key differentiators
- Brand positioning
</market_positioning>

<marketing_channels>
For each recommended marketing channel, specify:

<channel name="[channel name]">
<rationale>Why this channel is appropriate for the audience</rationale>
<tactics>Specific tactics to employ</tactics>
<budget_allocation>Suggested budget allocation (amount or percentage)</budget_allocation>
<expected_outcomes>What results to expect</expected_outcomes>
</channel>

Include at least 4-5 channels (e.g., social media, content marketing, paid advertising, PR, email marketing, influencer partnerships, etc.)
</marketing_channels>

<launch_timeline>
Create a phased timeline for the launch:
- Pre-launch phase (activities and timeline)
- Launch phase (activities and timeline)
- Post-launch phase (activities and timeline)
</launch_timeline>

<success_metrics>
Define 5-7 key performance indicators (KPIs) to measure campaign success, including:
- How each will be measured
- Target benchmarks
- Timeline for evaluation
</success_metrics>

<risk_mitigation>
Identify potential risks or challenges and how to address them.
</risk_mitigation>

Ensure your strategy is realistic given the budget constraints and highly targeted to the specific audience described.
</Instructions>
```

## Expected Behavior
The AI should:
1. Create a coherent, comprehensive marketing strategy
2. Tailor recommendations to the specific product and audience
3. Respect budget constraints in allocations
4. Recommend appropriate marketing channels with clear rationale
5. Provide actionable, specific tactics rather than vague suggestions
6. Include realistic timeline and measurable success metrics
7. Consider potential risks and challenges

## Usage Example

**Input:**
```
PRODUCT_DESCRIPTION:
EcoBottle - A smart water bottle that tracks hydration, reminds users to drink water, 
and is made from 100% recycled materials. Connects to smartphone app. Price: $45.

TARGET_AUDIENCE:
Health-conscious millennials and Gen Z (ages 22-35), urban professionals, 
interested in fitness and sustainability.

BUDGET:
$50,000 for 3-month launch campaign
```

**Expected Output:**
A detailed marketing strategy including digital channels (Instagram, TikTok), influencer partnerships with fitness/eco-influencers, content marketing, specific budget breakdowns, launch timeline, and success metrics like app downloads, sales targets, and social media engagement rates.
