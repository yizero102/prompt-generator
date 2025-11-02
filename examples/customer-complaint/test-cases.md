# Test Cases: Customer Complaint Email Response

## Test Case 1: Delayed Shipment with Time Sensitivity
**Inputs:**
- COMPLAINT: "Order #12345 hasn't arrived in 2 weeks. Needed it for event this weekend. Want refund."
- COMPANY_NAME: "StyleHub"
- COMPANY_POLICIES: "Can refund or replace, standard shipping 7-10 days"

**Expected Behavior:**
- Should acknowledge time sensitivity
- Should offer immediate refund as requested
- Should apologize sincerely
- Should offer additional gesture (discount/future benefit)

**Success Criteria:**
- Email shows empathy for missed event
- Offers refund clearly
- Apologizes without making excuses
- Includes proactive solution for future
- Professional but warm tone

## Test Case 2: Product Quality Issue
**Inputs:**
- COMPLAINT: "The laptop I bought from you last month is already broken! The screen flickers constantly and now it won't turn on at all. I paid $1,200 for this! I need a working computer for work. This is ridiculous."
- COMPANY_NAME: "TechDirect"
- COMPANY_POLICIES: "30-day return policy, 1-year warranty, can replace defective items"

**Expected Behavior:**
- Should acknowledge severity (work necessity)
- Should apologize for defective product
- Should explain warranty coverage
- Should offer fast replacement or repair
- Should be empathetic about work impact

**Success Criteria:**
- Acknowledges work urgency
- Explains warranty process clearly
- Offers expedited solution
- Doesn't blame customer
- Restores confidence in product quality

## Test Case 3: Mild Disappointment (Not Angry)
**Inputs:**
- COMPLAINT: "Hi, I received my order but the color is not quite what I expected from the website photos. It's more beige than cream. Not sure if I should return it or keep it. A bit disappointed."
- COMPANY_NAME: "HomeDecor Plus"
- COMPANY_POLICIES: "Free returns within 30 days, can exchange for different color"

**Expected Behavior:**
- Should match customer's mild tone (not over-apologize)
- Should acknowledge color representation challenges
- Should make return/exchange easy
- Should be helpful and friendly

**Success Criteria:**
- Tone matches customer's (not overly formal)
- Offers easy return/exchange process
- Doesn't over-apologize for minor issue
- Helpful and solution-oriented
- Makes customer feel heard

## Test Case 4: Rude/Hostile Customer
**Inputs:**
- COMPLAINT: "Your company is absolutely terrible! I've been on hold for 45 minutes and no one answers! Your customer service is the WORST I've ever experienced. I'm never shopping here again and I'll tell everyone I know how awful you are!!!"
- COMPANY_NAME: "ServiceCo"
- COMPANY_POLICIES: "Committed to <5 minute wait times, can escalate to supervisor"

**Expected Behavior:**
- Should remain professional despite hostility
- Should acknowledge the wait time issue
- Should apologize for poor experience
- Should offer immediate help
- Should not be defensive

**Success Criteria:**
- Remains calm and professional
- Doesn't mirror hostile tone
- Sincere apology for wait time
- Offers immediate assistance
- Attempts to restore relationship
- No defensive language

## Test Case 5: Billing Error
**Inputs:**
- COMPLAINT: "I was charged twice for my order #98765! My bank statement shows two charges of $89.99 from your store on the same day. I only ordered once. I need this fixed immediately."
- COMPANY_NAME: "ShopSmart"
- COMPANY_POLICIES: "Can reverse charges within 24 hours, pending charges may appear temporarily"

**Expected Behavior:**
- Should take billing seriously (financial impact)
- Should investigate immediately
- Should explain what likely happened
- Should provide clear timeline for resolution
- Should provide proof/confirmation

**Success Criteria:**
- Takes financial concern seriously
- Explains investigation process
- Provides clear timeline
- Offers immediate action
- May explain pending vs. posted charges
- Confirms resolution method

## Test Case 6: Service Experience Complaint
**Inputs:**
- COMPLAINT: "I visited your store location on Main Street yesterday and the staff was incredibly rude. A sales associate rolled her eyes at my questions and another one ignored me completely. I've been a loyal customer for 5 years and I'm shocked by this treatment."
- COMPANY_NAME: "RetailPro"
- COMPANY_POLICIES: "Customer-first culture, can escalate to store manager and regional manager"

**Expected Behavior:**
- Should take staff behavior seriously
- Should apologize profusely
- Should acknowledge long-term loyalty
- Should explain how complaint will be addressed
- Should offer to make it right

**Success Criteria:**
- Strong apology for staff behavior
- Acknowledges loyalty and values customer
- Explains concrete action (manager review)
- Offers gesture for poor experience
- Reassures about company values
- Personal follow-up offered

## Test Metrics

For each test case, evaluate:
1. **Empathy**: Does response show genuine understanding?
2. **Solution Quality**: Is solution appropriate and clear?
3. **Tone**: Professional, warm, appropriate to situation?
4. **Completeness**: All concerns addressed?
5. **Format**: Proper email structure (subject, greeting, body, closing)?
6. **De-escalation**: Does it calm rather than inflame?

## Passing Criteria
- All 6 test cases must show appropriate empathy
- Solutions must be clear and actionable in all cases
- No defensive or dismissive language allowed
- Professional format in all responses
- Tone must match situation (not generic)
- Must attempt to restore customer relationship
