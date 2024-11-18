# Telegram Message Forwarder Bot

An intelligent and efficient Telegram bot that monitors specific groups, extracts relevant data such as Solana wallet addresses and specific URLs, and forwards them to designated groups or bots. Built for scalability and extensibility, this project ensures accurate filtering, duplicate prevention, and group-specific configurations.

---

## 📋 Features
- **Advanced Message Filtering:** Identifies Solana wallet addresses and specific URLs (e.g., `pump.fun`, `dexscreener.com`).
- **Targeted Forwarding:** Filters and forwards messages based on group IDs and user IDs.
- **Duplicate Prevention:** Maintains a tracking system to prevent redundant forwarding.
- **Customizable Group Notifiers:** Adds a tailored notifier to forwarded messages for better context.
- **Automated Cleanup:** Periodically clears outdated tracking data for optimal performance.
- **Resilient Architecture:** Handles errors gracefully and ensures smooth operation with continuous monitoring.

---

## 🔧 Prerequisites
1. **Python 3.8 or later** installed. [Download Python](https://www.python.org/downloads/)
2. Install required Python libraries:
   ```bash
   pip install telethon
3. Obtain the following credentials from the [Telegram Developer Portal](https://my.telegram.org/)):
    api_id
    api_hash
   

### 🛠️ Setup Instructions

1. **Clone the Repository**  
   Run the following commands in your terminal:

   ```bash
   git clone https://github.com/kensdv/tg-automation
   cd tg-automation

2. **Create config.json**
Create a `config.json` file in the root directory with the following structure:

```json
{
  "api_id": "<YOUR_API_ID>",
  "api_hash": "<YOUR_API_HASH>",
  "group_notifiers": {
    "<GROUP_ID_1>": "<NOTIFIER_KEY_1>",
    "<GROUP_ID_2>": "<NOTIFIER_KEY_2>"
  },
  "notifier_keys": {
    "<NOTIFIER_KEY_1>": "<CUSTOM_NOTIFIER_TEXT_1>",
    "<NOTIFIER_KEY_2>": "<CUSTOM_NOTIFIER_TEXT_2>"
  },
  "destination_group_id": "<DESTINATION_GROUP_ID>",
  "trading_bot_id": "<TRADING_BOT_ID>",
  "specified_group_id": "<SPECIFIED_GROUP_ID>",
  "specified_user_id": "<SPECIFIED_USER_ID>"
}



After completing the setup, start the bot with:
```
python bot.py


### 🔍 How It Works

#### Message Monitoring:
- The bot listens to messages from the configured groups.
- Filters messages by:
  - Solana wallet address format (32–44 alphanumeric characters).
  - URLs matching `pump.fun` or `dexscreener.com`.

#### Content Filtering:
- Filters out duplicate wallet addresses already forwarded.
- Applies user-specific filtering within a designated group.

#### Message Forwarding:
- Constructs a forwarding message containing:
  - Detected wallet addresses.
  - Matching URLs.
  - A group-specific notifier.
- Forwards the message to:
  - A destination group.
  - A trading bot.

#### Duplicate Prevention:
- Tracks forwarded content using a timestamped dictionary.
- Automatically clears old entries every 24 hours.


## 💡 Example Workflow

1. A monitored group sends a message:

2. The bot detects:
- Solana address: `E7dhJ2NCjf82HqYzLFGfFhYh6zMzT7uL5Dg7ZZpJ`
- URL: `https://pump.fun/token123`

3. The bot constructs a message:

4. The bot forwards the message to:
- A destination group.
- A trading bot.


## 🤝 Contributions
We welcome contributions to enhance the bot's functionality! Here's how you can contribute:

1. **Fork this repository**.
2. **Create a new branch** for your feature or bug fix.
3. **Commit your changes** and submit a pull request.

## 🙌 Acknowledgments
- The [Telethon library](https://github.com/LonamiWebs/Telethon) for its seamless integration with the Telegram API.
- The blockchain and Telegram communities for their support and inspiration.
