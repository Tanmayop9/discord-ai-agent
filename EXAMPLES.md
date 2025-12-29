# Usage Examples

This document provides practical examples of how to use the Discord AI Agent with various services.

## 🆕 Modern Interactive Features

### Interactive Dashboard
The new interactive dashboard provides quick access to all services with buttons:
```
!dashboard
```
This opens a menu with buttons for:
- 📅 Calendar - Quick calendar actions
- 📧 Gmail - Check email status
- 🐙 GitHub - View GitHub info
- 💬 Slack - Slack quick actions
- 🤖 AI Assistant - AI help

### Calendar Menu
Open an interactive menu for calendar operations:
```
!calendar_menu
```
Features:
- **📅 Upcoming Events** - View your next events instantly
- **📆 Today's Events** - See today's schedule
- **➕ Create Event** - Fill out a form to create events easily

### Service Selection Menu
Choose your service with a dropdown:
```
!service_menu
```
Select from Calendar, Gmail, GitHub, Slack, or AI services.

### Interactive Help
Get contextual help with category selection:
```
!help
```
Then select a category from the dropdown to get specific help.

## 📅 Google Calendar Examples

### Creating Events
```
!calendar Create a team standup meeting tomorrow at 10am for 30 minutes
!calendar Schedule a dentist appointment on Friday at 2pm
!calendar Create a project review meeting next Monday at 3pm with alice@example.com and bob@example.com
!calendar Schedule a team sync tomorrow at 11am with Google Meet link
```

### Finding Events
```
!calendar Find all my events this week
!calendar Show me events with "meeting" in the title
!calendar What events do I have today?
!upcoming 5
```

### Updating Events
```
!calendar Update my dentist appointment to next Friday at 3pm
!calendar Change the project meeting title to "Q4 Project Review"
!calendar Add sarah@example.com to the team standup meeting
```

### Deleting Events
```
!calendar Delete the meeting called "Old Project Sync"
!calendar Remove the dentist appointment
```

### Getting Details
```
!calendar Get details about the project review meeting
!calendar Show me all my calendars
```

## 📧 Gmail Examples

### Sending Emails
```
!gmail Send an email to john@example.com with subject "Project Update" and message "The project is on track for completion next week."
!gmail Email sarah@example.com about tomorrow's meeting
!gmail Send a thank you email to team@example.com
```

### Searching Emails
```
!gmail Search for emails from boss@example.com
!gmail Find emails with subject containing "invoice"
!gmail Search for unread emails from last week
!gmail Show me emails about the project
```

### Creating Drafts
```
!gmail Create a draft email to client@example.com about the project proposal
!gmail Draft an email to team@example.com with subject "Weekly Update"
```

### Checking Inbox
```
!gmail Check my unread emails
!gmail Get my email status
```

## 🐙 GitHub Examples

### Creating Issues
```
!github Create an issue in facebook/react titled "Bug in useState hook"
!github Create a bug report in microsoft/vscode about syntax highlighting
!github Open an issue in owner/repo with title "Feature request: dark mode" and description "We need a dark mode option"
```

### Listing Issues
```
!github List open issues in tensorflow/tensorflow
!github Show me all issues in nodejs/node
!github Get closed issues in vuejs/vue
```

### Searching Repositories
```
!github Search for machine learning repositories
!github Find Python web framework repositories
!github Search for repositories with topic "react"
```

### Creating Pull Requests
```
!github Create a pull request in owner/repo from feature-branch to main with title "Add new feature"
!github Open a PR in myorg/myrepo merging dev into production
```

### Starring Repositories
```
!github Star the repository pytorch/pytorch
!github Star facebook/react
```

## 💬 Slack Examples

### Sending Messages
```
!slack Send "Good morning team!" to #general
!slack Post "Deployment completed successfully ✅" in #dev-ops
!slack Message #engineering saying "Code review needed for PR #123"
```

### Managing Channels
```
!slack List all channels
!slack Create a channel called project-phoenix
!slack Create a private channel named confidential-planning
```

### Setting Status
```
!slack Set my status to "In a meeting" with calendar emoji
!slack Update status to "Working from home 🏠"
!slack Set status "On vacation" with palm tree emoji
```

### Direct Messages
```
!slack Send a direct message to @john saying "Great work on the presentation!"
!slack DM @sarah about the upcoming deadline
```

## 🤖 Multi-Service AI Agent Examples

The `!ai` command can work across multiple services automatically:

### Combined Operations
```
!ai Schedule a project kickoff meeting for next Monday at 2pm and send an email to team@example.com notifying them
!ai Create a GitHub issue in owner/repo about the bug and notify #dev-team on Slack
!ai Check my calendar for tomorrow and send me an email summary
!ai Find all meetings this week with "standup" in the title and send the list to #general on Slack
```

### Smart Automation
```
!ai I need to organize a team event next Friday - create a calendar event, draft an invitation email, and post about it on Slack #general
!ai Create a weekly status report: check my completed GitHub issues and send an email to manager@example.com
!ai Schedule a code review meeting tomorrow and create a GitHub issue as a reminder
```

## 💡 Tips for Best Results

1. **Be Specific**: Include dates, times, and email addresses explicitly
   - Good: "Create a meeting tomorrow at 2pm with john@example.com"
   - Bad: "Schedule something soon"

2. **Use Full Repository Names**: For GitHub, always use `owner/repo` format
   - Good: "List issues in facebook/react"
   - Bad: "List issues in react"

3. **Channel Names**: For Slack, use `#channel-name` format
   - Good: "Send message to #general"
   - Bad: "Send message to general"

4. **Natural Language**: The AI understands context, so feel free to be conversational
   - "Can you schedule a meeting with Bob for next Tuesday?"
   - "I need to email Sarah about the project update"
   - "Create an issue in our repo about that bug we discussed"

5. **Multi-Service**: Use `!ai` when your task involves multiple services
   - Better: `!ai Create a meeting and notify the team on Slack`
   - Instead of: Two separate commands

## 🔧 Troubleshooting

### Authentication Errors
If you see authentication errors, re-authenticate:
```
!authenticate
```

### Service Not Working
Make sure you've connected the service when creating your account:
1. Run `!create_account`
2. Follow the Composio link to connect all services you need
3. Try your command again

### Need Help?
Use the help command to see all available features:
```
!help
```
