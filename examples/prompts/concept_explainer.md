# Task: Explain a complex scientific concept in simple terms

## Task Description
Explain a complex scientific concept in simple terms

## Input Variables
- `{$CONCEPT}`: The complex scientific concept to be explained

## Prompt Template

```
<Inputs>
{$CONCEPT}
</Inputs>

<Instructions Structure>
1. Present the concept to explain
2. Specify the target audience (general public)
3. Request use of analogies and simple language
4. Ask for structured explanation with examples
</Instructions Structure>

<Instructions>
You will be explaining a complex scientific concept in a way that is accessible to someone without a scientific background. Your goal is to make the concept understandable while remaining accurate.

Here is the concept you need to explain:
<concept>
{$CONCEPT}
</concept>

When creating your explanation, follow these guidelines:
- Use simple, everyday language and avoid jargon. If you must use technical terms, define them clearly.
- Use analogies and metaphors that relate to common experiences
- Break down the concept into smaller, digestible parts
- Use concrete examples where possible
- Build from simple ideas to more complex ones

Structure your explanation as follows:

<simple_explanation>
Start with a one-sentence, plain-language summary of what the concept is.
</simple_explanation>

<detailed_explanation>
Provide a more detailed explanation, broken into logical sections. For each section:
1. Introduce the sub-concept
2. Use an analogy or metaphor if helpful
3. Provide a concrete example
4. Connect it to everyday experience where possible
</detailed_explanation>

<key_takeaways>
List 3-5 key points that capture the essence of the concept in simple terms.
</key_takeaways>

<common_misconceptions>
Address any common misunderstandings about this concept, if applicable.
</common_misconceptions>

Remember: Your audience is curious but may not have any background in science. Clarity and accessibility are more important than comprehensive technical detail.
</Instructions>
```

## Expected Behavior
The AI should:
1. Avoid technical jargon or explain it when necessary
2. Use relatable analogies and metaphors
3. Provide concrete examples
4. Structure the explanation logically
5. Make the concept accessible without oversimplifying to the point of inaccuracy
6. Address common misconceptions

## Usage Example

**Input:**
```
CONCEPT: Quantum entanglement
```

**Expected Output:**
A clear, accessible explanation that might use analogies like "magic coins" or "connected twins" to illustrate how entangled particles behave, structured with simple summary, detailed breakdown, key takeaways, and common misconceptions.
