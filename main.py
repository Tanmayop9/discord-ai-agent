import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from tinydb import TinyDB, Query
import requests 
import json
from utils.manage_events import manage_events
from utils.manage_multi_service import manage_multi_service


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
INTEGRATION_ID = os.getenv("INTEGRATION_ID")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")


# Create a database to store user data

if not os.path.exists('./db'):
    os.makedirs('./db')

if not os.path.exists('./db/temp_user.json'):
    with open('./db/temp_user.json', 'w') as f:
        f.close()

if not os.path.exists('./db/user.json'):
    with open('./db/user.json', 'w') as f:
        f.close()


temp_user_db = TinyDB('./db/temp_user.json') # Temporary database to store user data for the current session
user_db = TinyDB('./db/user.json')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    # keeps track of how many guilds / servers the bot is associated with.
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@bot.event
async def on_message(message):
    # if message.content.lower() == "hello":
        # await message.channel.send("hey bro, what's up?")
    await bot.process_commands(message) # Ensures that other commands are processed


@bot.command(name='create_account')
async def _create_account(ctx):
    """
        Create an account and save `user_id` and `connected_account_id` in the database.
    """

    url = "https://backend.composio.dev/api/v1/connectedAccounts"
    user_id = ctx.author.id

    # Check if the user already has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        payload = {"integrationId": INTEGRATION_ID}
        headers = {
            "X-API-Key": COMPOSIO_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = json.loads(response.text)

        temp_user_db.insert({"user_id": user_id, "connected_account_id": response_data["connectedAccountId"]})

        await ctx.send(f"Click [here]({response_data['redirectUrl']}) to connect your account.\nOnce you have connected your account, you can use `!calendar` to manage events.")

    else:
        await ctx.send("You already have an account.")


@bot.command(name='authenticate')
async def _authenticate(ctx):
    """
        Create an new account again (because authentication credentials might be expired) and save `user_id` and `connected_account_id` in the database.
    """

    url = "https://backend.composio.dev/api/v1/connectedAccounts"
    user_id = ctx.author.id

    # Check if the user already has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if is_account:
        payload = {"integrationId": INTEGRATION_ID}
        headers = {
            "X-API-Key": COMPOSIO_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = json.loads(response.text)

        user_db.update({"connected_account_id": response_data["connectedAccountId"]}, Account.user_id == user_id)

        await ctx.send(f"Click [here]({response_data['redirectUrl']}) to connect your account.\nOnce you have connected your account, you can use `!calendar` to manage events.")

    else:
        await ctx.send("You don't have an account yet. Please create one using `!create_account`.")


@bot.command(name='calendar')
async def _calendar(ctx, *, message: str):
    """
        Manage events on Google Calendar. 
    """

    user_id = ctx.author.id

    # Check if the user has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        is_temp_account = temp_user_db.search(Account.user_id == user_id)

        if not is_temp_account:
            await ctx.send("You don't have an account yet. Please create one using `!create_account`.")
            return

        else:
            # Move the temporary account to the main database
            user_db.insert(is_temp_account[0])
            temp_user_db.remove(Account.user_id == user_id)

    await ctx.send("Processing your request...")

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_events(connected_account_id, message)
    await ctx.send(response)


@bot.command(name='upcoming')
async def _upcoming(ctx, count: int = 10):
    """
        List upcoming events from Google Calendar.
    """

    user_id = ctx.author.id

    # Check if the user has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        await ctx.send("You don't have an account yet. Please create one using `!create_account`.")
        return

    await ctx.send("Fetching your upcoming events...")

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_events(connected_account_id, f"List my next {count} upcoming events")
    await ctx.send(response)


@bot.command(name='help')
async def _help(ctx):
    """
        Display help information about available commands.
    """
    
    help_text = """
📚 **Discord AI Agent - Multi-Service Assistant**

**Account Management:**
• `!create_account` - Create a new account and connect to services
• `!authenticate` - Re-authenticate your account if credentials expire

**📅 Calendar Management:**
• `!calendar <message>` - Natural language calendar management
  Examples:
  - "Create a meeting tomorrow at 2pm for 1 hour"
  - "Find all my events this week"
  - "Delete the meeting called 'Team Sync'"
  - "Add john@example.com to my project meeting"

• `!upcoming [count]` - List your upcoming events (default: 10)

**📧 Gmail Commands:**
• `!gmail <message>` - Manage your Gmail
  Examples:
  - "Send an email to john@example.com with subject 'Meeting' and body 'Let's meet tomorrow'"
  - "Search for emails from sarah@example.com"
  - "Create a draft email to team@example.com about the project update"
  - "Check my unread emails"

**🐙 GitHub Commands:**
• `!github <message>` - Manage GitHub
  Examples:
  - "Create an issue in owner/repo with title 'Bug fix needed'"
  - "List open issues in facebook/react"
  - "Search for python machine learning repositories"
  - "Star the repository tensorflow/tensorflow"
  - "Create a pull request in owner/repo from feature-branch to main"

**💬 Slack Commands:**
• `!slack <message>` - Manage Slack
  Examples:
  - "Send message 'Hello team!' to #general"
  - "List all channels"
  - "Create a channel called project-alpha"
  - "Set my status to 'In a meeting' with emoji :calendar:"
  - "Send direct message to @john saying 'Great work!'"

**🤖 AI Multi-Service:**
• `!ai <message>` - Use AI agent with access to ALL services
  The AI will automatically determine which service(s) to use!
  Examples:
  - "Send an email about tomorrow's meeting and add it to my calendar"
  - "Create a GitHub issue and notify the team on Slack"
  - "Check my calendar and send a summary to my email"

**What you can do:**
✅ Manage Google Calendar events
✅ Send and search Gmail messages
✅ Create GitHub issues and PRs
✅ Send Slack messages and manage channels
✅ Use natural language for all commands
✅ Combine multiple services with AI agent

**Tips:**
💡 Be specific with dates, times, and email addresses
💡 Include repository names for GitHub commands (owner/repo)
💡 Use channel names (#general) for Slack
💡 The bot understands natural language - just chat normally!

Need help? Just ask the bot in natural language! 🤖
"""
    
    await ctx.send(help_text)


@bot.command(name='gmail')
async def _gmail(ctx, *, message: str):
    """
        Manage Gmail - send emails, search inbox, create drafts.
    """

    user_id = ctx.author.id

    # Check if the user has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        await ctx.send("You don't have an account yet. Please create one using `!create_account` and authenticate with Gmail.")
        return

    await ctx.send("Processing your Gmail request...")

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="gmail")
    await ctx.send(response)


@bot.command(name='github')
async def _github(ctx, *, message: str):
    """
        Manage GitHub - create issues, search repos, create PRs.
    """

    user_id = ctx.author.id

    # Check if the user has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        await ctx.send("You don't have an account yet. Please create one using `!create_account` and authenticate with GitHub.")
        return

    await ctx.send("Processing your GitHub request...")

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="github")
    await ctx.send(response)


@bot.command(name='slack')
async def _slack(ctx, *, message: str):
    """
        Manage Slack - send messages, create channels, set status.
    """

    user_id = ctx.author.id

    # Check if the user has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        await ctx.send("You don't have an account yet. Please create one using `!create_account` and authenticate with Slack.")
        return

    await ctx.send("Processing your Slack request...")

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="slack")
    await ctx.send(response)


@bot.command(name='ai')
async def _ai(ctx, *, message: str):
    """
        Use the AI agent with access to all services (Calendar, Gmail, GitHub, Slack).
    """

    user_id = ctx.author.id

    # Check if the user has an account
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)

    if not is_account:
        await ctx.send("You don't have an account yet. Please create one using `!create_account`.")
        return

    await ctx.send("Processing your request with AI agent...")

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="all")
    await ctx.send(response)


bot.run(DISCORD_BOT_TOKEN)
