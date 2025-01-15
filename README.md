
# Fortnite iMessage Bot with Discord Control

This project integrates a Fortnite bot that tracks player statuses with an iMessage group chat and a Discord bot for managing the bot settings.

---

## Features

- Tracks Fortnite friends' online/offline status.
- Sends real-time updates to an iMessage group chat.
- Discord bot for managing settings and restarting the Fortnite bot.
- Advanced logging for tracking events and user activity.
- Role-based permissions for admin, moderator, and user roles.

---

## Prerequisites

1. **Python 3.9+** installed on your system.
2. **Fortnite API Credentials**:
   - Epic Games email and password.
   - Ensure the account has 2FA enabled.
3. **iMessage Bridge**:
   - An API server that allows iMessage integration (e.g., a Bubble-based server).
4. **Discord Bot**:
   - Create a bot and retrieve the token from the [Discord Developer Portal](https://discord.com/developers/applications).

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fortnite-imessage-bot.git
cd fortnite-imessage-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure the Environment Variables
Create a `.env` file in the root directory with the following content:
```plaintext
DISCORD_TOKEN=your_discord_bot_token
EPIC_EMAIL=your_epic_games_email@example.com
EPIC_PASSWORD=your_epic_games_password
IMESSAGE_API_URL=http://your_imessage_api_url
GROUP_ID=your_imessage_group_id
ADMIN_ROLE=Admin
MODERATOR_ROLE=Moderator
```

### 4. Run the Bots
#### Fortnite Bot:
```bash
python fortnite_bot.py
```

#### Discord Bot:
```bash
python discord_bot.py
```

---

## Discord Bot Commands

| Command        | Role       | Description                                       |
|----------------|------------|---------------------------------------------------|
| `!set`         | Admin      | Update a setting in the `.env` file.              |
| `!view`        | Admin/Mod  | View current settings.                            |
| `!restart`     | Admin/Mod  | Restart the Fortnite bot.                         |
| `!logs`        | Admin      | View the last 20 log entries.                     |

---

## Logging

The bot logs all significant events to files located in the `logs/` directory:
- `fortnite_bot.log` for Fortnite bot activity.
- `bot.log` for Discord bot activity.

---

## File Structure

```
fortnite-imessage-bot/
│
├── .env               # Environment variables
├── .gitignore         # Git ignore file
├── discord_bot.py     # Discord bot for settings management
├── fortnite_bot.py    # Fortnite bot for tracking player statuses
├── requirements.txt   # Python dependencies
├── logs/              # Log files directory
└── README.md          # Project documentation
```

---

## Example Usage

### Fortnite Notifications in iMessage
- **"King has come online."**
- **"GOAT has gone offline."**

### Discord Bot
- **Admin:** `!set EPIC_EMAIL new_email@example.com`
- **Moderator:** `!restart`
- **View Settings:** `!view`
- **Access Logs:** `!logs`

---

## Contributing

Feel free to fork this repository, submit pull requests, or report issues.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### How to Use:
1. Copy this content into a file named `README.md`.
2. Commit it to your GitHub repository.
3. The file is now ready for display on your GitHub project page.
