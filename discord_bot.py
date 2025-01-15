import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_ROLE = os.getenv("ADMIN_ROLE", "Admin")
MODERATOR_ROLE = os.getenv("MODERATOR_ROLE", "Moderator")
LOG_FILE = "logs/bot.log"

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # Change to INFO, WARNING, or ERROR as needed
)

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Utility function to update the .env file
def update_env(key, value):
    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:
        for line in lines:
            if line.startswith(key):
                file.write(f"{key}={value}\n")
            else:
                file.write(line)

# Permissions check
def has_permission(user_roles, command):
    """Check if a user's roles grant permission for a command."""
    PERMISSIONS = {
        "Admin": ["set", "view", "restart", "logs"],
        "Moderator": ["view", "restart"],
        "User": ["view"]
    }

    for role in user_roles:
        if command in PERMISSIONS.get(role, []):
            return True
    return False

@bot.event
async def on_ready():
    logging.info(f"Discord bot logged in as {bot.user}")
    print(f"Discord bot logged in as {bot.user}")

@bot.command(name="set")
async def set_setting(ctx, key: str, value: str):
    """Command to update a setting in the .env file."""
    user_roles = [role.name for role in ctx.author.roles]
    if not has_permission(user_roles, "set"):
        await ctx.send("You do not have permission to use this command.")
        logging.warning(f"Unauthorized attempt to use 'set' by {ctx.author} ({user_roles})")
        return

    key = key.upper()
    if key in ["EPIC_EMAIL", "EPIC_PASSWORD", "IMESSAGE_API_URL", "GROUP_ID"]:
        update_env(key, value)
        await ctx.send(f"Successfully updated `{key}` to `{value}`!")
        logging.info(f"Updated setting: {key}={value} by {ctx.author} ({user_roles})")
    else:
        await ctx.send("Invalid key. Allowed keys: EPIC_EMAIL, EPIC_PASSWORD, IMESSAGE_API_URL, GROUP_ID.")
        logging.warning(f"Invalid key used in 'set': {key} by {ctx.author} ({user_roles})")

@bot.command(name="view")
async def view_setting(ctx):
    """Command to view all current settings."""
    user_roles = [role.name for role in ctx.author.roles]
    if not has_permission(user_roles, "view"):
        await ctx.send("You do not have permission to use this command.")
        logging.warning(f"Unauthorized attempt to use 'view' by {ctx.author} ({user_roles})")
        return

    with open(".env", "r") as file:
        settings = file.read()
    await ctx.send(f"Current Settings:\n```{settings}```")
    logging.info(f"Settings viewed by {ctx.author} ({user_roles})")

@bot.command(name="restart")
async def restart_bot(ctx):
    """Command to restart the Fortnite bot."""
    user_roles = [role.name for role in ctx.author.roles]
    if not has_permission(user_roles, "restart"):
        await ctx.send("You do not have permission to use this command.")
        logging.warning(f"Unauthorized attempt to use 'restart' by {ctx.author} ({user_roles})")
        return

    os.system("pkill -f fortnite_bot.py && python fortnite_bot.py &")
    await ctx.send("Fortnite bot restarted!")
    logging.info(f"Fortnite bot restarted by {ctx.author} ({user_roles})")

@bot.command(name="logs")
async def view_logs(ctx):
    """Command to view the last 20 lines of the log file."""
    user_roles = [role.name for role in ctx.author.roles]
    if not has_permission(user_roles, "logs"):
        await ctx.send("You do not have permission to use this command.")
        logging.warning(f"Unauthorized attempt to use 'logs' by {ctx.author} ({user_roles})")
        return

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            lines = file.readlines()
            last_lines = lines[-20:]  # Get the last 20 lines
        await ctx.send(f"Last 20 log entries:\n```{''.join(last_lines)}```")
        logging.info(f"Logs viewed by {ctx.author} ({user_roles})")
    else:
        await ctx.send("No logs found.")
        logging.warning(f"Logs requested but no log file found by {ctx.author} ({user_roles})")

bot.run(DISCORD_TOKEN)
