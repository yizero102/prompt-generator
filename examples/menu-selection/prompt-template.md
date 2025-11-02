# Prompt Template: Choose a Menu Item Based on User Preferences

## Task
Choose an item from a menu for me given user preferences

## Inputs
- `{$MENU}` - The menu with available items
- `{$PREFERENCES}` - User's dietary preferences, restrictions, and taste preferences

## Instructions

```
You will help a user choose the best item from a menu based on their preferences. 

Here is the menu:
<menu>
{$MENU}
</menu>

Here are the user's preferences:
<preferences>
{$PREFERENCES}
</preferences>

Please analyze the menu items and the user's preferences carefully. Consider:
- Dietary restrictions (allergies, vegetarian, vegan, etc.)
- Taste preferences (spicy, sweet, savory, etc.)
- Nutritional preferences (low-carb, high-protein, etc.)
- Any other stated preferences

First, in <analysis> tags, think through which menu items match the user's preferences and which don't. Consider why each item might be a good or poor fit.

Then, provide your recommendation in <recommendation> tags. Include:
- The name of the recommended menu item
- A brief explanation of why this item best matches the user's preferences
- If there are multiple good options, you may suggest a few alternatives

If no menu items are suitable given the user's restrictions, politely explain this in your recommendation.
```

## Example Usage

**Input:**
- MENU: "1. Grilled Chicken Caesar Salad, 2. Margherita Pizza, 3. Spicy Thai Curry with Shrimp, 4. Veggie Burger with Sweet Potato Fries, 5. Beef Tacos"
- PREFERENCES: "I'm vegetarian and prefer lighter meals. I enjoy Italian food."

**Expected Output:**
```
<analysis>
Looking at the menu options:
1. Grilled Chicken Caesar Salad - Contains chicken, not vegetarian
2. Margherita Pizza - Vegetarian, Italian cuisine, could work
3. Spicy Thai Curry with Shrimp - Contains shrimp, not vegetarian
4. Veggie Burger with Sweet Potato Fries - Vegetarian, but may be heavy
5. Beef Tacos - Contains beef, not vegetarian

The user needs vegetarian options and prefers lighter meals with Italian food preference. Options 2 and 4 are vegetarian. The Margherita Pizza fits both the vegetarian requirement and Italian preference.
</analysis>

<recommendation>
I recommend the Margherita Pizza (option 2). This is a vegetarian option that aligns perfectly with your preference for Italian food. It's also relatively lighter than the Veggie Burger with fries, making it a good choice for someone who prefers lighter meals.
</recommendation>
```
