from crewai_tools import tool
import requests
import dotenv
import os


dotenv.load_dotenv()
COMPOSIO_API_KEY = os.environ["COMPOSIO_API_KEY"]


@tool("Send Email")
def send_email(connectedAccountId: str, to_email: str, subject: str, body: str, cc: str | None = None, bcc: str | None = None) -> str:
    """
        Send an email via Gmail.

        :param required connectedAccountId: The ID of the connected account.
        :param required to_email: Recipient email address.
        :param required subject: Email subject.
        :param required body: Email body content.
        :param optional cc: CC email addresses (comma-separated).
        :param optional bcc: BCC email addresses (comma-separated).
    """

    print("\n\nSending email\n\n")

    url = "https://backend.composio.dev/api/v1/actions/gmail_send_email/execute"

    input_data = {
        "to_email": to_email,
        "subject": subject,
        "body": body
    }

    if cc is not None:
        input_data["cc"] = cc
    if bcc is not None:
        input_data["bcc"] = bcc

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "gmail",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        return f"✅ Email sent successfully to {to_email}!"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Gmail authentication credentials expired. Please re-authenticate using `!authenticate_gmail` command."
        return "❌ Something went wrong while sending the email."


@tool("Search Emails")
def search_emails(connectedAccountId: str, query: str, max_results: int = 10) -> str:
    """
        Search for emails in Gmail inbox.

        :param required connectedAccountId: The ID of the connected account.
        :param required query: Search query (e.g., "from:someone@example.com", "subject:meeting", "is:unread").
        :param optional max_results: Maximum number of emails to return (default: 10).
    """

    print("\n\nSearching emails\n\n")

    url = "https://backend.composio.dev/api/v1/actions/gmail_search_emails/execute"

    input_data = {
        "query": query,
        "max_results": max_results
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "gmail",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        emails = response_json.get("response", {}).get("messages", [])
        if emails:
            email_list = []
            for email in emails[:max_results]:
                subject = email.get("subject", "No Subject")
                sender = email.get("from", "Unknown")
                snippet = email.get("snippet", "")[:50]
                email_list.append(f"• **From:** {sender}\n  **Subject:** {subject}\n  **Preview:** {snippet}...")
            return "📧 **Search Results:**\n" + "\n\n".join(email_list)
        else:
            return "No emails found matching your search."
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Gmail authentication credentials expired. Please re-authenticate using `!authenticate_gmail` command."
        return "❌ Something went wrong while searching emails."


@tool("Get Unread Email Count")
def get_unread_count(connectedAccountId: str) -> str:
    """
        Get the count of unread emails in Gmail inbox.

        :param required connectedAccountId: The ID of the connected account.
    """

    print("\n\nGetting unread email count\n\n")

    url = "https://backend.composio.dev/api/v1/actions/gmail_get_profile/execute"

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "gmail",
        "input": {}
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        profile = response_json.get("response", {})
        email = profile.get("emailAddress", "your account")
        return f"📬 You have unread emails in {email}. Use search to find specific emails!"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Gmail authentication credentials expired. Please re-authenticate using `!authenticate_gmail` command."
        return "❌ Something went wrong while fetching email information."


@tool("Create Draft Email")
def create_draft(connectedAccountId: str, to_email: str, subject: str, body: str) -> str:
    """
        Create a draft email in Gmail.

        :param required connectedAccountId: The ID of the connected account.
        :param required to_email: Recipient email address.
        :param required subject: Email subject.
        :param required body: Email body content.
    """

    print("\n\nCreating draft email\n\n")

    url = "https://backend.composio.dev/api/v1/actions/gmail_create_draft/execute"

    input_data = {
        "to_email": to_email,
        "subject": subject,
        "body": body
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "gmail",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        return f"📝 Draft email created successfully! You can review and send it from your Gmail."
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Gmail authentication credentials expired. Please re-authenticate using `!authenticate_gmail` command."
        return "❌ Something went wrong while creating the draft."
