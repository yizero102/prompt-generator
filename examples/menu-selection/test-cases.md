# Test Cases: Menu Selection

## Test Case 1: Basic Vegetarian Preference
**Inputs:**
- MENU: "1. Grilled Chicken Caesar Salad, 2. Margherita Pizza, 3. Spicy Thai Curry with Shrimp, 4. Veggie Burger with Sweet Potato Fries, 5. Beef Tacos"
- PREFERENCES: "I'm vegetarian and prefer lighter meals. I enjoy Italian food."

**Expected Behavior:**
- Should exclude all non-vegetarian options (1, 3, 5)
- Should prioritize Italian food (option 2)
- Should consider "lighter meals" preference
- Should recommend Margherita Pizza

**Success Criteria:**
- Recommendation is vegetarian
- Reasoning mentions Italian preference
- No non-vegetarian items suggested

## Test Case 2: Allergy Restriction
**Inputs:**
- MENU: "1. Peanut Chicken Stir Fry, 2. Grilled Salmon, 3. Mushroom Risotto, 4. Peanut Butter Smoothie, 5. Greek Salad"
- PREFERENCES: "I have a severe peanut allergy. I love seafood."

**Expected Behavior:**
- Must exclude all items with peanuts (1, 4)
- Should prioritize seafood (option 2)
- Safety should be paramount

**Success Criteria:**
- No peanut-containing items recommended
- Seafood preference considered
- Analysis mentions allergy awareness

## Test Case 3: Multiple Preferences
**Inputs:**
- MENU: "1. Fried Chicken Wings, 2. Quinoa Buddha Bowl, 3. Bacon Cheeseburger, 4. Grilled Salmon with Veggies, 5. Caesar Salad"
- PREFERENCES: "Low-carb, high-protein diet. Don't like fried foods."

**Expected Behavior:**
- Should avoid fried foods (option 1)
- Should prioritize high-protein, low-carb options
- Should recommend option 4 (salmon) or modified option 5

**Success Criteria:**
- Recommended item is low-carb and high-protein
- Fried foods are excluded
- Nutritional reasoning provided

## Test Case 4: No Suitable Options
**Inputs:**
- MENU: "1. Beef Burger, 2. Chicken Sandwich, 3. Pork Chops, 4. Lamb Kebabs, 5. Turkey Club"
- PREFERENCES: "I'm vegan - no animal products at all."

**Expected Behavior:**
- Should recognize no suitable options exist
- Should politely explain the situation
- Should not try to force a recommendation

**Success Criteria:**
- Clearly states no vegan options available
- Polite and helpful tone
- Suggests asking for menu modifications or alternatives if possible

## Test Case 5: Spice Preference
**Inputs:**
- MENU: "1. Mild Chicken Tikka, 2. Extra Spicy Szechuan Noodles, 3. Ghost Pepper Wings, 4. Butter Chicken, 5. Vindaloo Curry"
- PREFERENCES: "I can't handle spicy food at all. Something creamy would be nice."

**Expected Behavior:**
- Should avoid all spicy options (2, 3, 5, possibly 1)
- Should recommend Butter Chicken (creamy and mild)
- Should warn about any potential spice

**Success Criteria:**
- Recommended item is mild
- Mentions creamy preference
- Warns about any mild spice if present

## Test Metrics

For each test case, evaluate:
1. **Accuracy**: Does the recommendation match the preferences?
2. **Safety**: Are restrictions (allergies, dietary) respected?
3. **Reasoning Quality**: Is the analysis thorough and logical?
4. **Output Format**: Does it use the required XML tags correctly?
5. **Edge Cases**: Does it handle impossible requests gracefully?

## Passing Criteria
- 5/5 test cases must pass accuracy check
- 0 safety violations allowed
- All outputs must follow the specified format
