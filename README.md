# Discord AI Agent

🤖 Meet our powerful AI agent made using [**composio**](https://www.composio.dev/) & [**crew AI**](https://docs.crewai.com/)! 🎉 This bot connects with multiple services including **Google Calendar**, **Gmail**, **GitHub**, and **Slack**, making it a breeze to manage all your productivity tasks right from _discord_. 💬🔗

<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#-demo">Demo</a></li>
    <li><a href="#-features">Features</a></li>
    <li><a href="#-available-commands">Available Commands</a></li>
    <li><a href="#-how-i-used-composio">How I Used Composio?</a></li>
    <li>
      <span>Getting Started</span>
      <ul>
        <li><a href="#-prerequisites">Prerequisites</a></li>
        <li><a href="#-steps-to-run">Steps to Run</a></li>
      </ul>
    </li>
    <li><a href="#%EF%B8%8F-project-structure">Project Structure</a></li>
    <li><a href="#-contributing">Contributing</a></li>
    <li><a href="#-acknowledgments">Acknowledgments<a/></li>
    <li><a href="#-license">License</a></li>
  </ol>
</details>

## 🎥 DEMO
[![demo video](https://img.youtube.com/vi/___DcDDQK-k/0.jpg)](https://www.youtube.com/watch?v=___DcDDQK-k)

## 📙 Features

### 🗓️ Google Calendar
You can manage calendar events just by normal chatting with our bot:

- **Create** events with _meeting rooms, attendees via email, Google Meet integration_ and all the necessary features
- **Find** upcoming events
- **Update** & **Delete** existing events
- **Create Quick** events
- **Add/Remove attendees** from events
- **Get detailed** event information
- **List** all your calendars

### 📧 Gmail
Manage your emails directly from Discord:

- **Send emails** with subject and body
- **Search** your inbox with queries
- **Create drafts** for later sending
- **Check** unread email count

### 🐙 GitHub
Manage your repositories and collaboration:

- **Create issues** in repositories
- **List issues** (open, closed, or all)
- **Search repositories** across GitHub
- **Create pull requests**
- **Star repositories** you like

### 💬 Slack
Stay connected with your team:

- **Send messages** to channels
- **Create channels** (public or private)
- **List** all workspace channels
- **Set your status** with custom emoji
- **Send direct messages** to team members

### 🤖 AI Multi-Service Agent
Use natural language to work across multiple services simultaneously! The AI agent can automatically determine which services to use based on your request.

## 🎮 Available Commands

### Account Management
- `!create_account` - Create a new account and connect to services
- `!authenticate` - Re-authenticate your account if credentials expire
- `!help` - Display detailed help information

### Google Calendar Commands
- `!calendar <message>` - Natural language calendar management
- `!upcoming [count]` - List upcoming events (default: 10)

### Gmail Commands
- `!gmail <message>` - Send emails, search inbox, create drafts

### GitHub Commands
- `!github <message>` - Create issues, search repos, manage PRs

### Slack Commands
- `!slack <message>` - Send messages, create channels, set status

### AI Multi-Service
- `!ai <message>` - Use AI agent with access to ALL services

**Examples:**
```
!calendar Create a team meeting tomorrow at 3pm with john@example.com
!gmail Send an email to sarah@example.com about the project update
!github Create an issue in facebook/react about the bug I found
!slack Send a message to #general saying "Deployment completed!"
!ai Schedule a meeting for next Monday and notify the team on Slack
```

📖 **For more detailed examples, see [EXAMPLES.md](EXAMPLES.md)**

## 🤔 How I used composio?
**Composio** was very _crucial and reliable tool_ for making my project. It helped me to make my agentic tools for the agent **much more faster** and **in an easy way** acting like a **pipeline** between _agent_ and multiple services like _Google Calendar_, _Gmail_, _GitHub_, and _Slack_. It would really took me many more days if done without this 🔥.

## 🫳 Prerequisites
You should have

- Python 3.8 or higher
- GEMINI API KEY
- COMPOSIO API KEY
- Discord Bot Token
- And an [integration id](https://docs.composio.dev/api-reference/integrations/create-a-new-integration) from composio.

## 👣 Steps to Run
**Navigate to the Project Directory:**
Change to the directory where the `setup.sh`, `main.py`, `requirements.txt`, and `README.md` files are located. For example:
```shell
cd path/to/project/directory
```

### 1. Run the Setup File
Make the setup.sh Script Executable (if necessary):
On Linux or macOS, you might need to make the setup.sh script executable:
```shell
chmod +x setup.sh
```
Execute the setup.sh script to set up the environment, install dependencies, login to composio and 
add necessary tools:
```shell
./setup.sh
```
Now, Fill in the `.env` file with your secrets.

### 2. Run the python script
```shell
python3 main.py
```

## 🏛️ Project structure

```bash
├── utils
│   ├── calendar.py
│   ├── manage_events.py
│   └── manage_multi_service.py
├── .env.example
├── .gitignore
├── EXAMPLES.md
├── gmail_tools.py
├── github_tools.py
├── slack_tools.py
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── setup.sh
└── tools.py
```

## 🤗 Contributing
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

## ✍ Acknowledgments
This project couldn't be there if they didn't be there!
- [Composio](https://composio.dev/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [crew AI](https://docs.crewai.com/)
- [Gemini](https://gemini.google.com/app)

Even something was gone wrong while making this project but composio team helped me to over come the issues and I am really thankful to it!

## 🧾 License
This project is licensed under the [MIT License](LICENSE).

