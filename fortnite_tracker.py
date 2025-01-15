import os
import logging
import asyncio
from dotenv import load_dotenv
from fortnite_api import FortniteAPI
import discord
from discord.ext import tasks

# Load environment variables
load_dotenv()

# Environment Variables
FORTNITE_BOT_TOKEN = os.getenv("FORTNITE_BOT_TOKEN")
NOTIFICATION_CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID"))
EPIC_EMAIL = os.getenv("EPIC_EMAIL")
EPIC_PASSWORD = os.getenv("EPIC_PASSWORD")

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename="logs/fortnite_tracker.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Discord client setup
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

# Fortnite API setup
fortnite_api = FortniteAPI(email=EPIC_EMAIL, password=EPIC_PASSWORD)

# State tracking for online players
online_players = set()

@discord_client.event
async def on_ready():
    logging.info(f"Fortnite Tracker Bot logged in as {discord_client.user}")
    print(f"Fortnite Tracker Bot logged in as {discord_client.user}")
    check_fortnite_status.start()

# Periodically check Fortnite friends' statuses
@tasks.loop(seconds=60)  # Check every 60 seconds
async def check_fortnite_status():
    global online_players

    try:
        friends = fortnite_api.get_friends()
        new_online_players = {friend["displayName"] for friend in friends if friend["isOnline"]}
        newly_offline_players = online_players - new_online_players
        newly_online_players = new_online_players - online_players

        # Update the state
        online_players = new_online_players

        # Get the Discord channel
        channel = discord_client.get_channel(NOTIFICATION_CHANNEL_ID)

        # Notify about status changes
        for player in newly_online_players:
            await channel.send(f"**{player}** has come online!")
            logging.info(f"Notification: {player} came online.")

        for player in newly_offline_players:
            await channel.send(f"**{player}** has gone offline!")
            logging.info(f"Notification: {player} went offline.")

    except Exception as e:
        logging.error(f"Error checking Fortnite status: {e}")

discord_client.run(FORTNITE_BOT_TOKEN)
