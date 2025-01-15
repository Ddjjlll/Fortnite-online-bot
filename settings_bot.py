import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands

# Load environment variables
load_dotenv()

# Environment Variables
SETTINGS_BOT_TOKEN = os.getenv("SETTINGS_BOT_TOKEN")
ADMIN_ROLE = os.getenv("ADMIN_ROLE", "Admin")
LOG_FILE = "logs/settings_bot.log"

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Discord bot setup
intents = discord.Intents.default()
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
def is_admin(ctx):
    return any(role.name == ADMIN_ROLE for role in ctx.author.roles)

@bot.event
async def on_ready():
    logging.info(f"Settings Bot logged in as {bot.user}")
    print(f"Settings Bot logged in as {bot.user}")

@bot.command(name="set")
async def set_setting(ctx, key: str, value: str):
    """Update a setting in the .env file."""
    if not is_admin(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    key = key.upper()
    if key in ["EPIC_EMAIL", "EPIC_PASSWORD", "NOTIFICATION_CHANNEL_ID"]:
        update_env(key, value)
        await ctx.send(f"Updated `{key}` to `{value}`.")
        logging.info(f"Setting updated: {key}={value} by {ctx.author}")
    else:
        await ctx.send("Invalid key. Allowed keys: EPIC_EMAIL, EPIC_PASSWORD, NOTIFICATION_CHANNEL_ID.")

@bot.command(name="view")
async def view_settings(ctx):
    """View current settings."""
    if not is_admin(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    with open(".env", "r") as file:
        settings = file.read()
    await ctx.send(f"Current settings:\n```{settings}```")
    logging.info(f"Settings viewed by {ctx.author}")

bot.run(SETTINGS_BOT_TOKEN)
