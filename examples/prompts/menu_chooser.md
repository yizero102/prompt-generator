# Task: Choose an item from a menu for me given user preferences

## Task Description
Choose an item from a menu for me given user preferences

## Input Variables
- `{$MENU}`: The menu with available items
- `{$PREFERENCES}`: User's dietary preferences, restrictions, and taste preferences

## Prompt Template

```
<Inputs>
{$MENU}
{$PREFERENCES}
</Inputs>

<Instructions Structure>
1. Present the menu and preferences to the AI
2. Ask it to analyze the menu items against the preferences
3. Use a scratchpad for thinking through options
4. Request a final recommendation with justification
</Instructions Structure>

<Instructions>
I'd like you to help me choose an item from a menu based on my preferences. I will provide you with a menu and my preferences, and I'd like you to recommend the best option for me.

Here is the menu:
<menu>
{$MENU}
</menu>

Here are my preferences:
<preferences>
{$PREFERENCES}
</preferences>

Please analyze the menu items carefully, considering my preferences including any dietary restrictions, taste preferences, and other requirements I've mentioned.

Use the scratchpad below to think through your analysis:

<scratchpad>
- First, identify any dietary restrictions or requirements that eliminate certain options
- Then, consider taste preferences and rank remaining options
- Finally, select the best match
</scratchpad>

After your analysis, provide your recommendation. First explain your reasoning, then give your final recommendation inside <recommendation> tags.
</Instructions>
```

## Expected Behavior
The AI should:
1. Carefully read both the menu and preferences
2. Eliminate items that don't meet dietary restrictions
3. Rank remaining items based on taste preferences
4. Provide clear reasoning before the final recommendation
5. Output the recommendation in the specified XML tags

## Usage Example

**Input:**
```
MENU: 
- Margherita Pizza (vegetarian)
- Pepperoni Pizza
- Caesar Salad (contains anchovies)
- Garden Salad (vegan)
- Pasta Carbonara (contains eggs and bacon)
- Marinara Pasta (vegan)

PREFERENCES:
I'm vegetarian and prefer Italian food. I'm not a fan of very heavy dishes.
```

**Expected Output:**
The AI should recommend either the Margherita Pizza or Marinara Pasta with reasoning about why these options match the preferences.
