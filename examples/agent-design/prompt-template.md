# Prompt Template: Design an Agent for Planning and Executing Tasks

## Task
Design an agent that can plan and execute tasks, and design the system tools it will use for planning and user communication, with the distinction that the tools for execution are to be provided by the user

## Inputs
- `{$AGENT_PURPOSE}` - The overall purpose and domain of the agent
- `{$TASK_TYPES}` - Types of tasks the agent should be able to handle
- `{$USER_PROVIDED_TOOLS}` - Description of execution tools the user will provide (optional)

## Instructions

```
You will design an AI agent system that can plan and execute tasks autonomously. Your design should include the agent's core capabilities, the planning/communication tools you'll design, and how it will work with user-provided execution tools.

Here is the agent's purpose:
<purpose>
{$AGENT_PURPOSE}
</purpose>

Types of tasks it should handle:
<task_types>
{$TASK_TYPES}
</task_types>

User-provided execution tools (if specified):
<user_tools>
{$USER_PROVIDED_TOOLS}
</user_tools>

Design a complete agent architecture that can intelligently plan and execute tasks.

Structure your design as follows:

In <agent_overview> tags, provide:
- Agent's core purpose and capabilities
- Key design principles
- Overall architecture approach

In <planning_system> tags, design:
- How the agent breaks down tasks into steps
- Decision-making framework
- Error handling and replanning approach
- Success criteria evaluation

In <system_tools> tags, design the planning and communication tools the agent will use:
- Tool for task decomposition and planning
- Tool for tracking task state and progress
- Tool for communicating with user (status updates, clarifying questions, results)
- Tool for reflection/learning from execution
- For each tool, specify:
  - Tool name and purpose
  - Input parameters
  - Output format
  - When/how the agent should use it

In <execution_framework> tags, explain:
- How agent will work with user-provided execution tools
- How it determines which tool to use for each step
- How it handles tool failures or unexpected results
- How it validates outputs from execution tools

In <agent_prompt> tags, write the actual system prompt that will govern the agent's behavior:
- Instructions for how to approach tasks
- How to use the planning/communication tools
- How to use execution tools
- Decision-making guidelines
- Error handling procedures
- Communication standards

In <example_execution> tags, provide a detailed walkthrough of how the agent would handle a sample task from start to finish, showing:
- Initial task breakdown
- Tool calls made
- Decision points
- User communication
- Error handling if applicable
- Task completion

Your design should enable the agent to work autonomously while remaining transparent and communicative with users.
```

## Example Usage

**Input:**
- AGENT_PURPOSE: "Personal productivity assistant that helps users manage and complete their daily tasks and projects"
- TASK_TYPES: "Schedule meetings, send emails, research information, create documents, set reminders, track progress on projects"
- USER_PROVIDED_TOOLS: "send_email(to, subject, body), create_calendar_event(title, date, time, duration), web_search(query), create_document(title, content), set_reminder(time, message)"

**Expected Output:**
```
<agent_overview>
Core Purpose: A personal productivity assistant that autonomously plans and executes daily tasks and project work on behalf of the user. The agent can handle complex, multi-step tasks like "prepare for tomorrow's meeting" or "organize the team offsite" by breaking them into manageable steps and executing them using available tools.

Key Design Principles:
1. Transparency: Always communicate what it's doing and why
2. User confirmation for important actions: Seek approval before sending emails or scheduling meetings
3. Adaptability: Replan when things don't go as expected
4. Proactivity: Anticipate needs and suggest next steps
5. Learn from context: Use conversation history and user preferences

Architecture Approach: The agent operates in a plan-execute-reflect cycle. It analyzes the user's request, creates a detailed plan, executes steps using tools, monitors progress, and adapts as needed. Planning and communication tools are built into the system, while execution tools are provided by the user.
</agent_overview>

<planning_system>
Task Decomposition Process:
1. Analyze user request to understand goal and constraints
2. Identify required information and tools needed
3. Break into sequential or parallel subtasks
4. Identify dependencies between subtasks
5. Estimate complexity and potential failure points
6. Create ordered execution plan

Decision-Making Framework:
- Evaluate multiple approaches to a task
- Consider efficiency vs. thoroughness tradeoffs
- Prioritize user preferences and past feedback
- Assess risk of actions (sending email to wrong person = high risk)
- Determine when to ask user vs. proceed autonomously

Error Handling & Replanning:
- If tool fails: try alternative approach or ask user for guidance
- If output unexpected: analyze cause and adjust plan
- If information missing: use web_search or ask user
- If goal unreachable: explain constraints and suggest alternatives
- Always maintain task state to avoid repeating successful steps

Success Criteria:
- All subtasks completed successfully
- User goal achieved (verify through reflection)
- No user complaints or corrections
- Task completed within reasonable time/effort
</planning_system>

<system_tools>
Tool 1: create_task_plan
Purpose: Break down user request into detailed, executable plan
Inputs:
  - user_request (string): The task requested by user
  - context (object): Relevant context (calendar, previous conversations, preferences)
Outputs:
  - plan_id (string): Unique identifier for this plan
  - steps (array): List of steps, each with:
    - step_id
    - description
    - required_tool
    - dependencies (which steps must complete first)
    - risk_level (low/medium/high)
    - requires_user_approval (boolean)
When to use: At the start of any new task request, before execution begins

Tool 2: update_task_state
Purpose: Track progress and current state of task execution
Inputs:
  - plan_id (string): Which plan is being executed
  - step_id (string): Which step just completed/failed
  - status (string): "completed", "failed", "in_progress", "blocked"
  - result (object): Output from the step execution
  - notes (string): Any observations or issues
Outputs:
  - overall_progress (string): Percentage complete
  - next_steps (array): What should happen next
  - blockers (array): Any issues preventing progress
When to use: After each step execution, whether successful or not

Tool 3: communicate_with_user
Purpose: Send updates, ask questions, or report results to user
Inputs:
  - message_type (string): "status_update", "question", "approval_request", "completion_report", "error_notification"
  - content (string): The message to the user
  - requires_response (boolean): Whether agent should wait for user input
  - context (object): Relevant information to display (plan progress, error details, etc.)
Outputs:
  - user_response (string): User's reply if requires_response=true
  - timestamp (string): When communication occurred
When to use: 
  - Before high-risk actions (approval_request)
  - After every 3-4 steps or significant milestone (status_update)
  - When blocked or uncertain (question)
  - When task completes (completion_report)
  - When errors occur (error_notification)

Tool 4: reflect_and_learn
Purpose: Analyze task execution to improve future performance
Inputs:
  - plan_id (string): The completed plan
  - user_feedback (string): Any feedback user provided
  - actual_steps (array): What actually happened vs. what was planned
Outputs:
  - insights (array): Lessons learned
  - preference_updates (object): User preferences to remember
  - improvement_suggestions (array): How to handle similar tasks better
When to use: After task completion, especially if there were deviations from plan or user corrections
</system_tools>

<execution_framework>
Working with User-Provided Tools:
The agent has access to execution tools (send_email, create_calendar_event, web_search, create_document, set_reminder) that are provided by the user's environment. The agent doesn't implement these tools but must use them correctly.

Tool Selection Process:
1. For each step in the plan, identify which execution tool(s) are needed
2. Verify tool is available in user-provided tools
3. Prepare correct parameters based on task context
4. Execute tool call
5. Validate output matches expectations

Handling Tool Failures:
- Tool returns error: Log error, inform user via communicate_with_user, attempt alternative approach
- Tool succeeds but output unexpected: Analyze discrepancy, update plan if needed
- Tool not available: Inform user what tool is needed and why, ask for alternative approach
- Tool partially succeeds: Determine if acceptable or if retry/correction needed

Output Validation:
- After sending email: Confirm it was sent, no errors in recipient/content
- After scheduling: Verify event created at correct time, attendees notified
- After web search: Check if results are relevant to query
- After document creation: Confirm document accessible and content correct
- After reminder: Confirm reminder is set for correct time

The agent should treat execution tools as black boxes - it knows what they do but not how they work internally. It focuses on choosing the right tool, providing correct parameters, and handling results appropriately.
</execution_framework>

<agent_prompt>
You are a personal productivity assistant that helps users manage and complete their daily tasks and projects. You can handle complex requests by breaking them into steps and executing them autonomously using available tools.

**Your Capabilities:**
- Plan multi-step tasks by breaking them down into manageable subtasks
- Execute tasks using tools provided by the user's environment
- Track progress and adapt when things don't go as planned
- Communicate clearly about what you're doing and why
- Learn from user feedback to improve over time

**Tools You Use:**

System Tools (for planning and communication):
- create_task_plan: Break down tasks into executable plans
- update_task_state: Track progress and maintain task state
- communicate_with_user: Send updates, ask questions, request approvals
- reflect_and_learn: Improve from completed tasks

Execution Tools (provided by user environment):
- send_email(to, subject, body): Send emails
- create_calendar_event(title, date, time, duration): Schedule events
- web_search(query): Search the web for information
- create_document(title, content): Create text documents
- set_reminder(time, message): Set time-based reminders

**How to Handle Tasks:**

1. **Understand the Request**
   - Analyze what the user wants to accomplish
   - Identify the end goal and any constraints
   - Note any missing information you'll need

2. **Create a Plan**
   - Use create_task_plan to break the request into steps
   - Identify which execution tools each step requires
   - Mark high-risk steps that need user approval
   - Consider dependencies between steps

3. **Communicate Before Starting**
   - Use communicate_with_user to share your plan
   - For high-risk actions (sending important emails, scheduling with others), request explicit approval
   - Clarify any ambiguities before proceeding

4. **Execute Step by Step**
   - Work through plan in order, respecting dependencies
   - Use appropriate execution tools for each step
   - After each step, use update_task_state to track progress
   - Validate that each step achieved intended outcome

5. **Handle Issues Gracefully**
   - If a tool fails, try an alternative approach or ask user for guidance
   - If results are unexpected, replan rather than forge ahead
   - If missing information, use web_search or ask user
   - Always update task state when issues occur

6. **Communicate Throughout**
   - Send status updates after significant progress
   - Notify user of any problems immediately
   - Don't execute high-risk actions without approval
   - Be transparent about what you're doing

7. **Complete and Reflect**
   - When all steps are done, verify the goal is achieved
   - Use communicate_with_user to report completion and results
   - Use reflect_and_learn to improve from this experience
   - Ask for feedback if the outcome might not be exactly what user wanted

**Guidelines:**
- Always prioritize user intent over literal instruction
- Be proactive but not presumptuous
- Seek approval for anything that could have significant consequences
- If uncertain, ask rather than guess
- Learn from corrections and adjust behavior
- Maintain context from previous interactions

**Communication Style:**
- Be clear and concise
- Explain your reasoning for important decisions
- Use structured formats for complex updates
- Be respectful of user's time
- Show progress, don't just work silently

Now, when a user gives you a task, follow this process to plan and execute it successfully.
</agent_prompt>

<example_execution>
User Request: "Prepare me for tomorrow's 2pm client meeting with Acme Corp"

Step 1: Planning
Agent uses create_task_plan:
```
Plan ID: plan_001
Steps:
1. [search_info] Search for information about Acme Corp (low risk, no approval needed)
2. [search_history] Search for previous communications with Acme Corp (low risk, no approval needed)
3. [create_brief] Create briefing document with company info and history (low risk, no approval needed)
4. [calendar_check] Verify meeting is on calendar (low risk, no approval needed)
5. [send_doc] Send briefing document to user (medium risk, requires approval)
Dependencies: Steps 1,2 must complete before 3; Step 4 independent; Step 5 requires 3
```

Step 2: Communicate Plan
Agent uses communicate_with_user:
```
Message Type: approval_request
Content: "I'll help you prepare for tomorrow's Acme Corp meeting. Here's my plan:
1. Research Acme Corp's recent news and information
2. Find our previous emails/communications with them
3. Create a briefing document summarizing key points
4. Verify the meeting is confirmed on your calendar
5. Send you the briefing document

I'll need your approval before sending the document. Shall I proceed?"
Requires Response: true
```

User responds: "Yes, go ahead"

Step 3: Execute Research
Agent uses web_search("Acme Corp recent news"):
Result: "Acme Corp recently announced Q3 earnings, new product launch..."

Agent uses update_task_state:
```
Plan ID: plan_001
Step ID: search_info
Status: completed
Result: {summary: "Found recent news about Q3 earnings, new product...", sources: [...]}
Notes: "Good amount of recent information available"
Progress: 20% complete
```

Agent uses web_search("Acme Corp contact history") - assumes this searches user's email/CRM:
Result: "Last contact 3 months ago about pricing proposal..."

Agent uses update_task_state:
```
Plan ID: plan_001
Step ID: search_history
Status: completed
Result: {summary: "Last contact 3 months ago, discussion about pricing", emails: [...]}
Progress: 40% complete
```

Step 4: Create Document
Agent uses create_document:
```
Title: "Acme Corp Meeting Brief - [Tomorrow's Date]"
Content: "
MEETING BRIEF: Acme Corp
Date: [Tomorrow's Date] 2:00 PM

COMPANY OVERVIEW:
- Industry: [from research]
- Recent News: Q3 earnings announced, new product launch
- Key decision makers: [if found]

OUR RELATIONSHIP:
- Last contact: 3 months ago
- Previous discussion: Pricing proposal for [product]
- Status: [if found]

MEETING PREPARATION:
- Review pricing proposal sent 3 months ago
- Prepare to discuss their new product launch
- Questions to ask: [relevant questions based on context]

SUGGESTED AGENDA:
1. Reconnect and catch up
2. Discuss their recent developments
3. Review our proposal status
4. Next steps
"
```

Agent uses update_task_state:
```
Plan ID: plan_001
Step ID: create_brief
Status: completed
Result: {document_id: "doc_123", title: "Acme Corp Meeting Brief"}
Progress: 60% complete
```

Step 5: Check Calendar
Agent uses create_calendar_event - wait, this is for creating events. Need to search instead.

Agent realizes there's no tool to check existing calendar events. Uses communicate_with_user:
```
Message Type: question
Content: "I've created your briefing document. I wanted to verify the meeting is on your calendar, but I don't have a tool to check existing events. Can you confirm the meeting is scheduled for tomorrow at 2pm?"
Requires Response: true
```

User responds: "Yes, it's confirmed"

Agent uses update_task_state:
```
Plan ID: plan_001
Step ID: calendar_check
Status: completed
Result: {confirmed: "user verified"}
Notes: "No tool available to check calendar, user manually confirmed"
Progress: 80% complete
```

Step 6: Send Document (Requires Approval)
Agent uses communicate_with_user:
```
Message Type: approval_request
Content: "I've created your briefing document for tomorrow's Acme Corp meeting. It includes:
- Company overview and recent news
- Summary of our previous interactions (last contact 3 months ago about pricing)
- Suggested talking points and agenda

Would you like me to send you this document, or would you like to review my plan first?"
Requires Response: true
Context: {document_preview: "[First few lines of document]"}
```

User responds: "Send it to me"

Agent uses send_email:
```
to: [user's email address - should be in context]
subject: "Meeting Brief: Acme Corp - Tomorrow 2pm"
body: "Hi,

Here's your briefing document for tomorrow's meeting with Acme Corp at 2pm.

[Content of briefing document]

Good luck with the meeting!

Your AI Assistant"
```

Agent uses update_task_state:
```
Plan ID: plan_001
Step ID: send_doc
Status: completed
Result: {email_sent: true, to: user_email}
Progress: 100% complete
```

Step 7: Complete and Reflect
Agent uses communicate_with_user:
```
Message Type: completion_report
Content: "All done! I've prepared you for tomorrow's Acme Corp meeting:
✓ Researched recent company news and developments
✓ Reviewed our previous communications (3 months ago)
✓ Created briefing document with key points and suggested agenda
✓ Confirmed meeting is on calendar for tomorrow 2pm
✓ Sent briefing document to your email

You're ready for the meeting. Let me know if you need anything else!"
```

Agent uses reflect_and_learn:
```
Plan ID: plan_001
Insights: [
  "User wanted comprehensive prep, not just basic info",
  "No calendar checking tool available - noted for future",
  "Meeting prep tasks valued by user"
]
Preference Updates: {
  "meeting_prep_style": "comprehensive with research"
}
```

Task Complete Successfully.
</example_execution>
```
