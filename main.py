import discord
from discord.ext import commands
from discord.ui import Button, Select, View, Modal, TextInput
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


# ===== Interactive UI Components =====

class ServiceSelectView(View):
    """Select menu for choosing a service to use"""
    def __init__(self, user_id):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.value = None
        
        # Add service select menu
        select = Select(
            placeholder="Choose a service...",
            options=[
                discord.SelectOption(label="📅 Google Calendar", value="calendar", description="Manage your calendar events", emoji="📅"),
                discord.SelectOption(label="📧 Gmail", value="gmail", description="Send and manage emails", emoji="📧"),
                discord.SelectOption(label="🐙 GitHub", value="github", description="Manage repositories and issues", emoji="🐙"),
                discord.SelectOption(label="💬 Slack", value="slack", description="Send messages and manage channels", emoji="💬"),
                discord.SelectOption(label="🤖 AI Multi-Service", value="ai", description="Use AI across all services", emoji="🤖"),
            ]
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu is not for you!", ephemeral=True)
            return
        
        self.value = interaction.data['values'][0]
        await interaction.response.send_message(f"Selected: {self.value}. Now use the corresponding command with your message!", ephemeral=True)
        self.stop()


class CalendarActionView(View):
    """Quick action buttons for calendar operations"""
    def __init__(self, user_id, connected_account_id):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.connected_account_id = connected_account_id
    
    @discord.ui.button(label="📅 Upcoming Events", style=discord.ButtonStyle.primary, emoji="📅")
    async def upcoming_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your menu!", ephemeral=True)
            return
        
        await interaction.response.defer()
        response = manage_events(self.connected_account_id, "List my next 10 upcoming events")
        
        embed = discord.Embed(
            title="📅 Your Upcoming Events",
            description=response,
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed)
    
    @discord.ui.button(label="📆 Today's Events", style=discord.ButtonStyle.secondary, emoji="📆")
    async def today_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your menu!", ephemeral=True)
            return
        
        await interaction.response.defer()
        response = manage_events(self.connected_account_id, "Show me all events today")
        
        embed = discord.Embed(
            title="📆 Today's Events",
            description=response,
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)
    
    @discord.ui.button(label="➕ Create Event", style=discord.ButtonStyle.success, emoji="➕")
    async def create_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your menu!", ephemeral=True)
            return
        
        modal = CreateEventModal(self.connected_account_id)
        await interaction.response.send_modal(modal)


class CreateEventModal(Modal, title="Create Calendar Event"):
    """Modal for creating calendar events"""
    event_title = TextInput(
        label="Event Title",
        placeholder="e.g., Team Meeting",
        required=True,
        max_length=100
    )
    
    event_time = TextInput(
        label="When?",
        placeholder="e.g., tomorrow at 2pm, next Monday at 10am",
        required=True,
        max_length=100
    )
    
    duration = TextInput(
        label="Duration (optional)",
        placeholder="e.g., 1 hour, 30 minutes",
        required=False,
        max_length=50
    )
    
    attendees = TextInput(
        label="Attendees (optional)",
        placeholder="e.g., john@example.com, jane@example.com",
        required=False,
        style=discord.TextStyle.paragraph,
        max_length=200
    )
    
    def __init__(self, connected_account_id):
        super().__init__()
        self.connected_account_id = connected_account_id
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        prompt = f"Create an event titled '{self.event_title.value}' {self.event_time.value}"
        if self.duration.value:
            prompt += f" for {self.duration.value}"
        if self.attendees.value:
            prompt += f" with attendees {self.attendees.value}"
        
        response = manage_events(self.connected_account_id, prompt)
        
        embed = discord.Embed(
            title="✅ Event Creation",
            description=response,
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)


class QuickActionsView(View):
    """Main dashboard with quick action buttons"""
    def __init__(self, user_id, connected_account_id):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.connected_account_id = connected_account_id
    
    @discord.ui.button(label="📅 Calendar", style=discord.ButtonStyle.primary, emoji="📅", row=0)
    async def calendar_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your dashboard!", ephemeral=True)
            return
        
        view = CalendarActionView(self.user_id, self.connected_account_id)
        embed = discord.Embed(
            title="📅 Calendar Quick Actions",
            description="Choose a quick action for your calendar:",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="📧 Gmail", style=discord.ButtonStyle.primary, emoji="📧", row=0)
    async def gmail_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your dashboard!", ephemeral=True)
            return
        
        await interaction.response.defer()
        response = manage_multi_service(self.connected_account_id, "Check my unread emails count", service="gmail")
        
        embed = discord.Embed(
            title="📧 Gmail Status",
            description=response,
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🐙 GitHub", style=discord.ButtonStyle.primary, emoji="🐙", row=0)
    async def github_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your dashboard!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🐙 GitHub Actions",
            description="Use `!github <message>` to:\n• Create issues\n• List issues\n• Search repositories\n• Create pull requests\n• Star repositories",
            color=discord.Color.dark_gray()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="💬 Slack", style=discord.ButtonStyle.primary, emoji="💬", row=0)
    async def slack_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your dashboard!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="💬 Slack Actions",
            description="Use `!slack <message>` to:\n• Send messages to channels\n• Create channels\n• List channels\n• Set status\n• Send direct messages",
            color=discord.Color.purple()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🤖 AI Assistant", style=discord.ButtonStyle.success, emoji="🤖", row=1)
    async def ai_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your dashboard!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🤖 AI Multi-Service Assistant",
            description="Use `!ai <message>` to work across multiple services!\n\nThe AI will automatically determine which services to use based on your request.\n\nExamples:\n• 'Schedule a meeting and notify team on Slack'\n• 'Create GitHub issue and send email'\n• 'Check calendar and send summary via email'",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class HelpView(View):
    """Interactive help menu with category selection"""
    def __init__(self):
        super().__init__(timeout=180)
        
        select = Select(
            placeholder="Choose a category for help...",
            options=[
                discord.SelectOption(label="Getting Started", value="getting_started", description="Setup and authentication", emoji="🚀"),
                discord.SelectOption(label="Calendar Commands", value="calendar", description="Google Calendar help", emoji="📅"),
                discord.SelectOption(label="Gmail Commands", value="gmail", description="Gmail help", emoji="📧"),
                discord.SelectOption(label="GitHub Commands", value="github", description="GitHub help", emoji="🐙"),
                discord.SelectOption(label="Slack Commands", value="slack", description="Slack help", emoji="💬"),
                discord.SelectOption(label="AI Assistant", value="ai", description="Multi-service AI help", emoji="🤖"),
            ]
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        category = interaction.data['values'][0]
        
        if category == "getting_started":
            embed = discord.Embed(
                title="🚀 Getting Started",
                description=(
                    "**Setup Commands:**\n"
                    "• `!create_account` - Create a new account and connect to services\n"
                    "• `!authenticate` - Re-authenticate if credentials expire\n"
                    "• `!dashboard` - Open your interactive dashboard\n\n"
                    "**First Steps:**\n"
                    "1. Run `!create_account` and follow the link\n"
                    "2. Connect the services you want to use\n"
                    "3. Start using commands or the dashboard!"
                ),
                color=discord.Color.green()
            )
        elif category == "calendar":
            embed = discord.Embed(
                title="📅 Calendar Commands",
                description=(
                    "**Commands:**\n"
                    "• `!calendar <message>` - Natural language calendar management\n"
                    "• `!upcoming [count]` - List upcoming events\n"
                    "• `!calendar_menu` - Interactive calendar menu\n\n"
                    "**Examples:**\n"
                    "• Create a meeting tomorrow at 2pm\n"
                    "• Find all events this week\n"
                    "• Delete the meeting called 'Team Sync'"
                ),
                color=discord.Color.blue()
            )
        elif category == "gmail":
            embed = discord.Embed(
                title="📧 Gmail Commands",
                description=(
                    "**Command:**\n"
                    "• `!gmail <message>` - Manage your Gmail\n\n"
                    "**Examples:**\n"
                    "• Send an email to john@example.com with subject 'Meeting'\n"
                    "• Search for emails from sarah@example.com\n"
                    "• Create a draft email\n"
                    "• Check my unread emails"
                ),
                color=discord.Color.red()
            )
        elif category == "github":
            embed = discord.Embed(
                title="🐙 GitHub Commands",
                description=(
                    "**Command:**\n"
                    "• `!github <message>` - Manage GitHub\n\n"
                    "**Examples:**\n"
                    "• Create an issue in owner/repo with title 'Bug fix'\n"
                    "• List open issues in facebook/react\n"
                    "• Search for machine learning repositories\n"
                    "• Create a pull request in owner/repo"
                ),
                color=discord.Color.dark_gray()
            )
        elif category == "slack":
            embed = discord.Embed(
                title="💬 Slack Commands",
                description=(
                    "**Command:**\n"
                    "• `!slack <message>` - Manage Slack\n\n"
                    "**Examples:**\n"
                    "• Send 'Hello team!' to #general\n"
                    "• List all channels\n"
                    "• Create a channel called project-alpha\n"
                    "• Set my status to 'In a meeting'"
                ),
                color=discord.Color.purple()
            )
        elif category == "ai":
            embed = discord.Embed(
                title="🤖 AI Multi-Service Assistant",
                description=(
                    "**Command:**\n"
                    "• `!ai <message>` - AI with access to ALL services\n\n"
                    "**Examples:**\n"
                    "• Schedule a meeting and notify team on Slack\n"
                    "• Create GitHub issue and send email about it\n"
                    "• Check calendar and send summary via email\n"
                    "• Find events this week and post to Slack"
                ),
                color=discord.Color.gold()
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ConfirmView(View):
    """Confirmation dialog for destructive actions"""
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.value = None
        self.user_id = user_id
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success, emoji="✅")
    async def confirm(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your confirmation!", ephemeral=True)
            return
        self.value = True
        await interaction.response.send_message("Confirmed!", ephemeral=True)
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger, emoji="❌")
    async def cancel(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This is not your confirmation!", ephemeral=True)
            return
        self.value = False
        await interaction.response.send_message("Cancelled!", ephemeral=True)
        self.stop()


# ===== Bot Events =====

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

        embed = discord.Embed(
            title="🎉 Account Creation",
            description=(
                "Welcome! Let's get you set up.\n\n"
                "**Step 1:** Click the button below to connect your accounts\n"
                "**Step 2:** Authorize the services you want to use\n"
                "**Step 3:** Return here and start using the bot!\n\n"
                "After setup, use `!dashboard` for quick access to all features."
            ),
            color=discord.Color.green()
        )
        
        view = View()
        connect_button = Button(
            label="Connect Services",
            style=discord.ButtonStyle.link,
            url=response_data['redirectUrl'],
            emoji="🔗"
        )
        view.add_item(connect_button)
        
        await ctx.send(embed=embed, view=view)

    else:
        embed = discord.Embed(
            title="ℹ️ Account Status",
            description="You already have an account! Use `!dashboard` to access all features.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


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

        embed = discord.Embed(
            title="🔄 Re-authentication",
            description=(
                "Let's reconnect your services.\n\n"
                "Click the button below to re-authenticate:"
            ),
            color=discord.Color.orange()
        )
        
        view = View()
        connect_button = Button(
            label="Reconnect Services",
            style=discord.ButtonStyle.link,
            url=response_data['redirectUrl'],
            emoji="🔗"
        )
        view.add_item(connect_button)
        
        await ctx.send(embed=embed, view=view)

    else:
        embed = discord.Embed(
            title="❌ No Account Found",
            description="You don't have an account yet. Please create one using `!create_account`.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


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
            embed = discord.Embed(
                title="❌ No Account",
                description="You don't have an account yet. Please create one using `!create_account`.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        else:
            # Move the temporary account to the main database
            user_db.insert(is_temp_account[0])
            temp_user_db.remove(Account.user_id == user_id)

    processing_embed = discord.Embed(
        title="⏳ Processing...",
        description="Processing your calendar request...",
        color=discord.Color.orange()
    )
    status_msg = await ctx.send(embed=processing_embed)

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_events(connected_account_id, message)
    
    result_embed = discord.Embed(
        title="📅 Calendar Result",
        description=response,
        color=discord.Color.green()
    )
    await status_msg.edit(embed=result_embed)


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
        embed = discord.Embed(
            title="❌ No Account",
            description="You don't have an account yet. Please create one using `!create_account`.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    processing_embed = discord.Embed(
        title="⏳ Fetching Events...",
        description=f"Fetching your next {count} upcoming events...",
        color=discord.Color.orange()
    )
    status_msg = await ctx.send(embed=processing_embed)

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_events(connected_account_id, f"List my next {count} upcoming events")
    
    result_embed = discord.Embed(
        title=f"📅 Your Next {count} Events",
        description=response,
        color=discord.Color.blue()
    )
    await status_msg.edit(embed=result_embed)


@bot.command(name='help')
async def _help(ctx):
    """
        Display interactive help information about available commands.
    """
    
    embed = discord.Embed(
        title="📚 Discord AI Agent - Help",
        description=(
            "Welcome to your multi-service AI assistant! 🤖\n\n"
            "**🆕 Modern Features:**\n"
            "• `!dashboard` - Interactive dashboard with quick actions\n"
            "• `!calendar_menu` - Interactive calendar operations\n"
            "• `!service_menu` - Choose service with dropdown\n\n"
            "**Account Management:**\n"
            "• `!create_account` - Create and connect services\n"
            "• `!authenticate` - Re-authenticate services\n\n"
            "**Services:**\n"
            "📅 `!calendar <msg>` - Calendar management\n"
            "📧 `!gmail <msg>` - Email management\n"
            "🐙 `!github <msg>` - GitHub operations\n"
            "💬 `!slack <msg>` - Slack messaging\n"
            "🤖 `!ai <msg>` - AI multi-service\n\n"
            "**Select a category below for detailed help:**"
        ),
        color=discord.Color.blue()
    )
    
    view = HelpView()
    await ctx.send(embed=embed, view=view)


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
        embed = discord.Embed(
            title="❌ No Account",
            description="You don't have an account yet. Please create one using `!create_account` and authenticate with Gmail.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    processing_embed = discord.Embed(
        title="⏳ Processing Gmail Request...",
        description="Processing your Gmail request...",
        color=discord.Color.orange()
    )
    status_msg = await ctx.send(embed=processing_embed)

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="gmail")
    
    result_embed = discord.Embed(
        title="📧 Gmail Result",
        description=response,
        color=discord.Color.red()
    )
    await status_msg.edit(embed=result_embed)


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
        embed = discord.Embed(
            title="❌ No Account",
            description="You don't have an account yet. Please create one using `!create_account` and authenticate with GitHub.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    processing_embed = discord.Embed(
        title="⏳ Processing GitHub Request...",
        description="Processing your GitHub request...",
        color=discord.Color.orange()
    )
    status_msg = await ctx.send(embed=processing_embed)

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="github")
    
    result_embed = discord.Embed(
        title="🐙 GitHub Result",
        description=response,
        color=discord.Color.dark_gray()
    )
    await status_msg.edit(embed=result_embed)


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
        embed = discord.Embed(
            title="❌ No Account",
            description="You don't have an account yet. Please create one using `!create_account` and authenticate with Slack.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    processing_embed = discord.Embed(
        title="⏳ Processing Slack Request...",
        description="Processing your Slack request...",
        color=discord.Color.orange()
    )
    status_msg = await ctx.send(embed=processing_embed)

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="slack")
    
    result_embed = discord.Embed(
        title="💬 Slack Result",
        description=response,
        color=discord.Color.purple()
    )
    await status_msg.edit(embed=result_embed)


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
        embed = discord.Embed(
            title="❌ No Account",
            description="You don't have an account yet. Please create one using `!create_account`.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    processing_embed = discord.Embed(
        title="⏳ AI Processing...",
        description="Processing your request with AI agent...",
        color=discord.Color.orange()
    )
    status_msg = await ctx.send(embed=processing_embed)

    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]

    response = manage_multi_service(connected_account_id, message, service="all")
    
    result_embed = discord.Embed(
        title="🤖 AI Result",
        description=response,
        color=discord.Color.gold()
    )
    await status_msg.edit(embed=result_embed)


@bot.command(name='dashboard')
async def _dashboard(ctx):
    """
        Open interactive dashboard with quick access to all services.
    """
    
    user_id = ctx.author.id
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)
    
    if not is_account:
        embed = discord.Embed(
            title="❌ No Account",
            description="You need to create an account first!\nUse `!create_account` to get started.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]
    
    embed = discord.Embed(
        title="🎛️ Your Dashboard",
        description=(
            f"Welcome {ctx.author.mention}! 👋\n\n"
            "Use the buttons below for quick access to your services.\n"
            "Each service has its own set of quick actions and features.\n\n"
            "**Available Services:**\n"
            "📅 Calendar • 📧 Gmail • 🐙 GitHub • 💬 Slack • 🤖 AI"
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="Click any button to get started!")
    
    view = QuickActionsView(user_id, connected_account_id)
    await ctx.send(embed=embed, view=view)


@bot.command(name='calendar_menu')
async def _calendar_menu(ctx):
    """
        Open interactive calendar menu with quick actions.
    """
    
    user_id = ctx.author.id
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)
    
    if not is_account:
        embed = discord.Embed(
            title="❌ No Account",
            description="You need to create an account first!\nUse `!create_account` to get started.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    connected_account_id = user_db.search(Account.user_id == user_id)[0]["connected_account_id"]
    
    embed = discord.Embed(
        title="📅 Calendar Quick Actions",
        description=(
            "Choose a quick action or use `!calendar <message>` for natural language commands.\n\n"
            "**Quick Actions:**\n"
            "• View upcoming events\n"
            "• See today's schedule\n"
            "• Create a new event (with form)"
        ),
        color=discord.Color.blue()
    )
    
    view = CalendarActionView(user_id, connected_account_id)
    await ctx.send(embed=embed, view=view)


@bot.command(name='service_menu')
async def _service_menu(ctx):
    """
        Display service selection menu.
    """
    
    user_id = ctx.author.id
    Account = Query()
    is_account = user_db.search(Account.user_id == user_id)
    
    if not is_account:
        embed = discord.Embed(
            title="❌ No Account",
            description="You need to create an account first!\nUse `!create_account` to get started.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="🎯 Service Selection",
        description=(
            "Select a service from the dropdown menu below:\n\n"
            "📅 **Calendar** - Manage events and schedules\n"
            "📧 **Gmail** - Send and manage emails\n"
            "🐙 **GitHub** - Manage repositories and issues\n"
            "💬 **Slack** - Team messaging and channels\n"
            "🤖 **AI** - Multi-service AI assistant"
        ),
        color=discord.Color.purple()
    )
    
    view = ServiceSelectView(user_id)
    await ctx.send(embed=embed, view=view)


bot.run(DISCORD_BOT_TOKEN)
