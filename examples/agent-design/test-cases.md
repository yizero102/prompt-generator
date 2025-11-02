# Test Cases: Agent Design for Planning and Execution

## Test Case 1: Simple Sequential Task
**Inputs:**
- AGENT_PURPOSE: "Personal productivity assistant"
- TASK_TYPES: "Send emails, schedule meetings, set reminders"
- USER_PROVIDED_TOOLS: "send_email(to, subject, body), create_calendar_event(title, date, time), set_reminder(time, message)"

**Test Scenario:** User says "Remind me to call John tomorrow at 10am and send him an email now asking for his availability"

**Expected Behavior:**
- Should create plan with 2 steps: send email, set reminder
- Should execute email first (now), then reminder (for tomorrow)
- Should ask for email content details if needed
- Should confirm both actions completed

**Success Criteria:**
- Agent creates clear task plan
- Identifies correct tools for each step
- Executes in logical order
- Communicates what it's doing
- Handles both immediate and scheduled actions

## Test Case 2: Task Requiring Information Gathering
**Inputs:**
- AGENT_PURPOSE: "Research and document assistant"
- TASK_TYPES: "Research topics, create documents, send emails"
- USER_PROVIDED_TOOLS: "web_search(query), create_document(title, content), send_email(to, subject, body)"

**Test Scenario:** User says "Research quantum computing and create a summary document"

**Expected Behavior:**
- Should use web_search first to gather information
- Should create document with researched information
- Should organize information logically
- Should communicate when research is done and document is created

**Success Criteria:**
- Plans research before document creation
- Shows dependency (research → document)
- Uses web_search appropriately
- Creates document with researched content
- Communicates progress at key milestones

## Test Case 3: Task with Missing Information
**Inputs:**
- AGENT_PURPOSE: "Meeting scheduler"
- TASK_TYPES: "Schedule meetings, send invitations"
- USER_PROVIDED_TOOLS: "create_calendar_event(title, date, time, duration), send_email(to, subject, body)"

**Test Scenario:** User says "Schedule a meeting with the team next week"

**Expected Behavior:**
- Should identify missing information (which day, what time, who is "the team", what duration)
- Should ask user for clarification before proceeding
- Should not make assumptions about critical details
- Once info provided, should schedule meeting and send invitations

**Success Criteria:**
- Identifies all missing required information
- Asks clear questions to user
- Waits for response before proceeding
- Once info received, completes task correctly
- Doesn't hallucinate details

## Test Case 4: Task with Error Handling
**Inputs:**
- AGENT_PURPOSE: "Email and document assistant"
- TASK_TYPES: "Send emails, create documents"
- USER_PROVIDED_TOOLS: "send_email(to, subject, body), create_document(title, content)"

**Test Scenario:** User says "Send the Q4 report to all@company.com"

Agent tries to send email but send_email returns error: "Attachment not supported, email must be text only"

**Expected Behavior:**
- Should handle the error gracefully
- Should try alternative approach (create document with report, send document link)
- Should inform user about the issue and solution
- Should not fail silently or give up

**Success Criteria:**
- Detects tool failure
- Attempts alternative approach
- Communicates issue to user
- Updates task state to reflect error and recovery
- Completes task despite initial failure

## Test Case 5: High-Risk Action Requiring Approval
**Inputs:**
- AGENT_PURPOSE: "Executive assistant"
- TASK_TYPES: "Send emails, schedule meetings, manage communications"
- USER_PROVIDED_TOOLS: "send_email(to, subject, body), create_calendar_event(title, date, time)"

**Test Scenario:** User says "Send an email to the CEO declining the partnership proposal"

**Expected Behavior:**
- Should recognize this as high-risk (important recipient, significant decision)
- Should draft the email but not send without approval
- Should show user the draft and ask for confirmation
- Should only send after user approves

**Success Criteria:**
- Marks action as high-risk in plan
- Seeks user approval before execution
- Shows what will be sent before sending
- Waits for explicit approval
- Clear approval request, not ambiguous

## Test Case 6: Multi-Step Complex Task
**Inputs:**
- AGENT_PURPOSE: "Project management assistant"
- TASK_TYPES: "Research, create documents, send emails, set reminders, schedule meetings"
- USER_PROVIDED_TOOLS: "web_search(query), create_document(title, content), send_email(to, subject, body), set_reminder(time, message), create_calendar_event(title, date, time)"

**Test Scenario:** User says "Plan the Q4 team offsite event"

**Expected Behavior:**
- Should break down into multiple steps:
  - Research venue options
  - Create document with options and agenda
  - Send proposal email to team
  - Set reminder to follow up on responses
  - Schedule calendar event once confirmed
- Should show comprehensive plan before starting
- Should execute steps in logical order
- Should update user on progress

**Success Criteria:**
- Comprehensive task decomposition
- Logical step ordering with dependencies
- Uses multiple different tools appropriately
- Communicates plan upfront
- Sends progress updates
- Tracks state throughout execution
- Completes all sub-tasks

## Test Case 7: Parallel vs Sequential Execution
**Inputs:**
- AGENT_PURPOSE: "Communication assistant"
- TASK_TYPES: "Send emails, set reminders"
- USER_PROVIDED_TOOLS: "send_email(to, subject, body), set_reminder(time, message)"

**Test Scenario:** User says "Send thank you emails to Alice, Bob, and Carol, and remind me to follow up with each of them in one week"

**Expected Behavior:**
- Should identify that emails can be sent in parallel (independent)
- Should send all three emails
- Should set three reminders (one for each person)
- Should execute efficiently

**Success Criteria:**
- Plan shows which steps can be parallel
- Doesn't unnecessarily sequence independent actions
- Sends all three emails
- Sets three distinct reminders
- Completes efficiently

## Test Case 8: Agent Design with No User Tools Specified
**Inputs:**
- AGENT_PURPOSE: "Code review assistant that helps review pull requests"
- TASK_TYPES: "Fetch pull request, analyze code, post comments, approve/request changes"
- USER_PROVIDED_TOOLS: "" (not specified)

**Expected Behavior:**
- Should design agent architecture independent of specific tools
- Should specify what types of execution tools would be needed
- Should describe how agent would work with tools when provided
- Should be flexible about tool implementations

**Success Criteria:**
- Doesn't invent specific tools
- Describes categories of tools needed
- Framework for working with tools is clear
- Design is tool-agnostic where appropriate
- Specifies tool requirements clearly

## Test Metrics

For each test case, evaluate:
1. **Planning Quality**: Does agent break tasks down logically?
2. **Tool Selection**: Does it choose appropriate tools for each step?
3. **Communication**: Does it keep user informed appropriately?
4. **Error Handling**: Does it handle failures gracefully?
5. **Risk Assessment**: Does it identify high-risk actions?
6. **Completeness**: Does design include all necessary components?
7. **User Experience**: Is the interaction smooth and transparent?

## Passing Criteria
- All test cases must show logical task decomposition
- Tool selection must be appropriate in all cases
- Must communicate with user at key decision points
- Error handling must be present and reasonable
- High-risk actions must require approval
- Agent design must be complete (overview, planning, tools, execution, prompt, example)
- Example execution must demonstrate the full agent cycle
