from crewai_tools import tool
import requests
import dotenv
import os


dotenv.load_dotenv()
COMPOSIO_API_KEY = os.environ["COMPOSIO_API_KEY"]

# Configuration
MAX_CHANNELS_TO_LIST = 20  # Maximum number of channels to display


@tool("Send Slack Message")
def send_slack_message(connectedAccountId: str, channel: str, text: str) -> str:
    """
        Send a message to a Slack channel.

        :param required connectedAccountId: The ID of the connected account.
        :param required channel: Channel ID or name (e.g., "#general" or "C1234567890").
        :param required text: Message text to send.
    """

    print("\n\nSending Slack message\n\n")

    url = "https://backend.composio.dev/api/v1/actions/slack_send_message/execute"

    input_data = {
        "channel": channel,
        "text": text
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "slack",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        return f"✅ Message sent to {channel} successfully!"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Slack authentication credentials expired. Please re-authenticate using `!authenticate_slack` command."
        return "❌ Something went wrong while sending the Slack message."


@tool("List Slack Channels")
def list_slack_channels(connectedAccountId: str) -> str:
    """
        List all channels in the Slack workspace.

        :param required connectedAccountId: The ID of the connected account.
    """

    print("\n\nListing Slack channels\n\n")

    url = "https://backend.composio.dev/api/v1/actions/slack_list_channels/execute"

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "slack",
        "input": {}
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        channels = response_json.get("response", {}).get("channels", [])
        if channels:
            channel_list = []
            for channel in channels[:MAX_CHANNELS_TO_LIST]:
                name = channel.get("name", "Unknown")
                channel_id = channel.get("id", "")
                is_member = "✓" if channel.get("is_member", False) else " "
                channel_list.append(f"[{is_member}] **#{name}** (`{channel_id}`)")
            total_channels = len(channels)
            result = "💬 **Slack Channels:**\n" + "\n".join(channel_list)
            if total_channels > MAX_CHANNELS_TO_LIST:
                result += f"\n\n(Showing {MAX_CHANNELS_TO_LIST} of {total_channels} channels)"
            return result
        else:
            return "No channels found."
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Slack authentication credentials expired. Please re-authenticate using `!authenticate_slack` command."
        return "❌ Something went wrong while listing channels."


@tool("Create Slack Channel")
def create_slack_channel(connectedAccountId: str, name: str, is_private: bool = False) -> str:
    """
        Create a new channel in Slack workspace.

        :param required connectedAccountId: The ID of the connected account.
        :param required name: Channel name (lowercase, no spaces, hyphens allowed).
        :param optional is_private: Whether the channel should be private (default: False).
    """

    print("\n\nCreating Slack channel\n\n")

    url = "https://backend.composio.dev/api/v1/actions/slack_create_channel/execute"

    input_data = {
        "name": name,
        "is_private": is_private
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "slack",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        channel_data = response_json.get("response", {}).get("channel", {})
        channel_name = channel_data.get("name", name)
        return f"✅ Channel #{channel_name} created successfully!"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Slack authentication credentials expired. Please re-authenticate using `!authenticate_slack` command."
        return "❌ Something went wrong while creating the channel."


@tool("Set Slack Status")
def set_slack_status(connectedAccountId: str, status_text: str, status_emoji: str = ":speech_balloon:") -> str:
    """
        Set your Slack status.

        :param required connectedAccountId: The ID of the connected account.
        :param required status_text: Status text to display.
        :param optional status_emoji: Status emoji (default: ":speech_balloon:").
    """

    print("\n\nSetting Slack status\n\n")

    url = "https://backend.composio.dev/api/v1/actions/slack_set_user_status/execute"

    input_data = {
        "status_text": status_text,
        "status_emoji": status_emoji
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "slack",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        return f"✅ Slack status updated to: {status_emoji} {status_text}"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Slack authentication credentials expired. Please re-authenticate using `!authenticate_slack` command."
        return "❌ Something went wrong while setting Slack status."


@tool("Send Direct Message")
def send_slack_dm(connectedAccountId: str, user: str, text: str) -> str:
    """
        Send a direct message to a Slack user.

        :param required connectedAccountId: The ID of the connected account.
        :param required user: User ID or username.
        :param required text: Message text to send.
    """

    print("\n\nSending Slack DM\n\n")

    url = "https://backend.composio.dev/api/v1/actions/slack_send_direct_message/execute"

    input_data = {
        "user": user,
        "text": text
    }

    payload = {
        "connectedAccountId": connectedAccountId,
        "appName": "slack",
        "input": input_data
    }

    headers = {
        "X-API-Key": COMPOSIO_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()

    if response_json.get("executed"):
        return f"✅ Direct message sent to {user} successfully!"
    else:
        if response_json.get("response", {}).get("error", {}).get("code") == 401:
            return "Your Slack authentication credentials expired. Please re-authenticate using `!authenticate_slack` command."
        return "❌ Something went wrong while sending the direct message."
