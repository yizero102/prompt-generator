# Prompt Template: Explain a Complex Scientific Concept in Simple Terms

## Task
Explain a complex scientific concept in simple terms

## Inputs
- `{$CONCEPT}` - The complex scientific concept to explain
- `{$AUDIENCE}` - The target audience (optional, e.g., "10-year-old", "high school student", "general public")

## Instructions

```
You will explain a complex scientific concept in simple, easy-to-understand terms. Your goal is to make the concept accessible without sacrificing accuracy.

Here is the concept to explain:
<concept>
{$CONCEPT}
</concept>

Target audience:
<audience>
{$AUDIENCE}
</audience>

Please provide a clear, simple explanation that the target audience can understand. Follow these guidelines:
- Avoid jargon and technical terms when possible
- When technical terms are necessary, define them simply
- Use analogies, metaphors, or everyday examples to illustrate the concept
- Break down complex ideas into smaller, digestible parts
- Be accurate - don't oversimplify to the point of being incorrect

Structure your response as follows:

In <simple_explanation> tags, provide your main explanation aimed at the target audience.

In <analogy> tags, provide a helpful real-world analogy or example that makes the concept more relatable.

In <why_it_matters> tags, briefly explain why this concept is important or interesting in everyday life or broader science.

Optionally, in <common_misconceptions> tags, address any common misunderstandings about this concept.

Keep your language friendly and engaging. You're not dumbing down science - you're making it accessible.
```

## Example Usage

**Input:**
- CONCEPT: "Quantum entanglement"
- AUDIENCE: "high school student with basic physics knowledge"

**Expected Output:**
```
<simple_explanation>
Quantum entanglement is a phenomenon where two particles become connected in such a way that the state of one particle instantly affects the state of the other, no matter how far apart they are. 

Imagine you have two special coins. When you flip one coin and it lands on heads, the other coin - even if it's on the other side of the universe - instantly "knows" to land on tails. They're linked together in a mysterious way.

In quantum physics, particles like electrons or photons can become entangled when they interact. Once entangled, measuring a property of one particle (like its spin) immediately determines the corresponding property of the other particle, even if they're separated by huge distances. This happens faster than light could travel between them, which puzzled even Einstein!
</simple_explanation>

<analogy>
Think of entangled particles like a pair of magic dice. You and your friend each take one die and travel to opposite ends of the Earth. When you roll your die and get a 3, your friend's die will always show a 4 (adding up to 7) at the exact same moment, without any signal passing between the dice. The dice aren't communicating - they're just fundamentally connected in a way that determines both their outcomes together.
</analogy>

<why_it_matters>
Quantum entanglement is important because it's one of the key differences between quantum physics and classical physics. It's being used to develop quantum computers, which could solve certain problems much faster than regular computers. It's also crucial for quantum cryptography, which could make completely secure communication possible. Understanding entanglement helps us grasp how the universe works at its most fundamental level.
</why_it_matters>

<common_misconceptions>
A common misconception is that entanglement allows faster-than-light communication. While the correlation between entangled particles is instantaneous, you can't use it to send information faster than light because the measurements appear random until you compare results. Another misconception is that entanglement means particles "communicate" with each other - but they don't send signals; they're simply correlated in a way that doesn't exist in our everyday experience.
</common_misconceptions>
```
