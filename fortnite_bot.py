import os
import time
import logging
import fortnitepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment Variables
EPIC_EMAIL = os.getenv("EPIC_EMAIL")
EPIC_PASSWORD = os.getenv("EPIC_PASSWORD")
IMESSAGE_API_URL = os.getenv("IMESSAGE_API_URL")
GROUP_ID = os.getenv("GROUP_ID")
LOG_FILE = "logs/fortnite_bot.log"

# Set up logging
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

# Fortnite API setup
client = fortnitepy.Client(
    email=EPIC_EMAIL,
    password=EPIC_PASSWORD
)

# Send message to iMessage group
def send_imessage(text):
    try:
        import requests
        response = requests.post(
            f"{IMESSAGE_API_URL}/send",
            json={"group_id": GROUP_ID, "message": text}
        )
        if response.status_code == 200:
            logging.info(f"iMessage sent: {text}")
        else:
            logging.error(f"Failed to send iMessage: {response.text}")
    except Exception as e:
        logging.error(f"Exception while sending iMessage: {e}")

# Retrieve the online friends
async def get_online_players():
    """Fetches the list of online friends using Fortnite API."""
    try:
        await client.start()
        online_players = [
            friend.display_name
            for friend in client.friends
            if friend.is_online()
        ]
        await client.close()
        return online_players
    except Exception as e:
        logging.error(f"Error fetching online players: {e}")
        await client.close()
        return []

# Main loop
def main():
    previous_players = set()

    logging.info("Fortnite bot started.")
    print("Fortnite bot is running...")

    while True:
        try:
            # Fortnite API logic
            import asyncio
            current_players = set(asyncio.run(get_online_players()))

            joined = current_players - previous_players
            left = previous_players - current_players

            for player in joined:
                message = f"{player} has come online."
                send_imessage(message)
                logging.info(message)

            for player in left:
                message = f"{player} has gone offline."
                send_imessage(message)
                logging.info(message)

            previous_players = current_players
            time.sleep(60)  # Poll every 60 seconds
        except KeyboardInterrupt:
            logging.info("Fortnite bot stopped.")
            print("Fortnite bot stopped.")
            break
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
