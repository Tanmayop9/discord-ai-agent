import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from tinydb import TinyDB, Query
import requests 
import json
from utils.manage_events import manage_events


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
📚 **Discord AI Calendar Agent - Commands**

**Account Management:**
• `!create_account` - Create a new account and connect to Google Calendar
• `!authenticate` - Re-authenticate your account if credentials expire

**Calendar Management:**
• `!calendar <message>` - Natural language calendar management
  Examples:
  - "Create a meeting tomorrow at 2pm for 1 hour"
  - "Find all my events this week"
  - "Delete the meeting called 'Team Sync'"
  - "Add john@example.com to my project meeting"
  - "Update my dentist appointment to next Monday at 3pm"

• `!upcoming [count]` - List your upcoming events (default: 10)
  Example: `!upcoming 5` - Show next 5 events

**What you can do with natural language:**
✅ Create events with meeting rooms, attendees, and descriptions
✅ Find and search events
✅ Update event details (time, title, description)
✅ Delete events
✅ Add or remove attendees
✅ Get detailed event information
✅ List your calendars
✅ Quick add events from simple text

**Tips:**
💡 Be specific with dates and times
💡 Include email addresses when adding attendees
💡 You can ask to create Google Meet rooms
💡 The bot understands natural language - just chat normally!

Need help? Just ask the bot in natural language! 🤖
"""
    
    await ctx.send(help_text)


bot.run(DISCORD_BOT_TOKEN)
