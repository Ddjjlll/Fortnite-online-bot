# Fortnite iMessage Bot with Discord Controller

This project integrates a Fortnite iMessage bot with a Discord bot for managing settings.

## Features
- Tracks Fortnite players online/offline.
- Sends updates to an iMessage group chat.
- Allows dynamic settings management through Discord commands.
- Supports advanced logging and role-based permissions.

## Setup

### Prerequisites
1. Python 3.9+ installed on your system.
2. A Discord bot token. [How to create one?](https://discordpy.readthedocs.io/en/stable/discord.html)
3. Fortnite account credentials.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/fortnite-imessage-bot.git
   cd fortnite-imessage-bot
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the .env file with your configuration:

Add your Discord token.
Add Fortnite account and iMessage API details.
Run the bots:

Fortnite Bot:
bash
Copy code
python fortnite_bot.py
Discord Bot:
bash
Copy code
python discord_bot.py
Commands
Discord Bot Commands
Command	Role	Description
!set	Admin	Update a setting in the .env file.
!view	Admin/Mod	View current settings.
!restart	Admin/Mod	Restart the Fortnite bot.
!logs	Admin	View the last 20 log entries.
