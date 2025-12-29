import os
import dotenv
from datetime import datetime
from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

# Calendar tools
from tools import (
    create_event,
    find_events,
    update_event,
    delete_event,
    get_event_id_by_title,
    quick_add_event,
    remove_attendee_event,
    list_upcoming_events,
    add_attendee_to_event,
    get_event_details,
    list_calendars,
)

# Gmail tools
from gmail_tools import (
    send_email,
    search_emails,
    get_unread_count,
    create_draft,
)

# GitHub tools
from github_tools import (
    create_github_issue,
    list_github_issues,
    search_github_repos,
    create_pull_request,
    star_repository,
)

# Slack tools
from slack_tools import (
    send_slack_message,
    list_slack_channels,
    create_slack_channel,
    set_slack_status,
    send_slack_dm,
)


# Load the environment variables
dotenv.load_dotenv()
google_api_key = os.environ["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1, google_api_key=google_api_key)

date = datetime.today().strftime("%Y-%m-%d")
timezone = datetime.now().astimezone().tzinfo


def manage_multi_service(connectedAccountId: str, prompt: str, service: str = "calendar") -> str:
    """
        Run the crew to manage multiple services (calendar, gmail, github, slack).
        :param required connectedAccountId: The ID of the connected account of the user.
        :param required prompt: The prompt for the crew to follow.
        :param optional service: The service to use - "calendar", "gmail", "github", "slack", or "all" (default: "calendar").
    """

    # Select tools based on service
    if service == "calendar":
        tools = [get_event_id_by_title, create_event, find_events, update_event, delete_event, 
                 quick_add_event, remove_attendee_event, list_upcoming_events, add_attendee_to_event, 
                 get_event_details, list_calendars]
        role = "Google Calendar Agent"
        goal = "You take action on Google Calendar using Google Calendar APIs"
        backstory = """You are an AI agent responsible for taking actions on Google Calendar on users' behalf.
        You need to take action on Calendar using Google Calendar APIs. Use correct tools to run APIs from the given tool-set."""
    
    elif service == "gmail":
        tools = [send_email, search_emails, get_unread_count, create_draft]
        role = "Gmail Agent"
        goal = "You manage Gmail operations like sending emails, searching inbox, and creating drafts"
        backstory = """You are an AI agent responsible for managing Gmail operations on users' behalf.
        You can send emails, search the inbox, check unread messages, and create drafts."""
    
    elif service == "github":
        tools = [create_github_issue, list_github_issues, search_github_repos, 
                 create_pull_request, star_repository]
        role = "GitHub Agent"
        goal = "You manage GitHub operations like creating issues, pull requests, and searching repositories"
        backstory = """You are an AI agent responsible for managing GitHub operations on users' behalf.
        You can create issues, list issues, search repositories, create pull requests, and star repositories."""
    
    elif service == "slack":
        tools = [send_slack_message, list_slack_channels, create_slack_channel, 
                 set_slack_status, send_slack_dm]
        role = "Slack Agent"
        goal = "You manage Slack operations like sending messages, creating channels, and managing status"
        backstory = """You are an AI agent responsible for managing Slack operations on users' behalf.
        You can send messages to channels, create channels, set status, and send direct messages."""
    
    elif service == "all":
        tools = [
            # Calendar
            get_event_id_by_title, create_event, find_events, update_event, delete_event, 
            quick_add_event, remove_attendee_event, list_upcoming_events, add_attendee_to_event, 
            get_event_details, list_calendars,
            # Gmail
            send_email, search_emails, get_unread_count, create_draft,
            # GitHub
            create_github_issue, list_github_issues, search_github_repos, 
            create_pull_request, star_repository,
            # Slack
            send_slack_message, list_slack_channels, create_slack_channel, 
            set_slack_status, send_slack_dm,
        ]
        role = "Multi-Service AI Agent"
        goal = "You manage multiple services including Google Calendar, Gmail, GitHub, and Slack"
        backstory = """You are an AI agent responsible for managing multiple services on users' behalf.
        You can handle Google Calendar events, Gmail emails, GitHub issues and repositories, and Slack messages.
        Choose the appropriate service and tools based on the user's request."""
    
    else:
        # Invalid service name
        return f"Invalid service '{service}'. Please use 'calendar', 'gmail', 'github', 'slack', or 'all'."

    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        verbose=True,
        tools=tools,
        llm=llm,
    )

    # Build task description based on service
    if service == "calendar":
        task_desc = f"""Manage events in Google Calendar based on: \n {prompt} \n 
        Schedule it for given date. Today's date is {date} and make the timezone be {timezone}.
        The connected account ID (connectedAccountId) is {connectedAccountId}."""
        expected = "Successfully completed the calendar task. Give a human-like response with emojis if necessary."
    else:
        task_desc = f"""Handle the following request for {service}: \n {prompt} \n 
        Today's date is {date} and timezone is {timezone}.
        The connected account ID (connectedAccountId) is {connectedAccountId}.
        For GitHub tasks, make sure to extract repository owner and name from the request.
        For Slack tasks, identify the channel or user correctly.
        For Gmail tasks, ensure email addresses are properly formatted."""
        expected = f"Successfully completed the {service} task. Give a human-like response with emojis if necessary."

    task = Task(
        description=task_desc,
        agent=agent,
        expected_output=expected,
    )

    response = task.execute()
    if response:
        return response
    else:
        return "Something went wrong. Please try again."
