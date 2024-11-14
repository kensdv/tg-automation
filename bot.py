import json
import logging
import re
import time
import asyncio
from telethon import TelegramClient, events

# Load config from the file
with open('config.json') as config_file:
    config = json.load(config_file)

# Set up logging
logging.basicConfig(level=logging.WARNING)

# Your Telegram API credentials
api_id = config['api_id']
api_hash = config['api_hash']

# Group configurations from config
group_notifiers = config['group_notifiers']
notifier_keys = config['notifier_keys']
destination_group_id = config['destination_group_id']
trading_bot_id = config['trading_bot_id']
specified_group_id = config['specified_group_id']  # ID of the group needing specific user check
specified_user_id = config['specified_user_id']  # User ID to filter in specified group only

# Solana address pattern and complete link capture for pump.fun and dexscreener.com
solana_address_pattern = r'\b[a-zA-Z0-9]{32,44}\b'
keyword_patterns = [
    r'https://pump\.fun[^\s]*',       # Captures the complete URL starting with pump.fun
    r'https://dexscreener\.com[^\s]*'  # Captures the complete URL starting with dexscreener.com
]
session_file = 'session_name'

# Create a new Telethon client instance using the session file
client = TelegramClient(session_file, api_id, api_hash)

# Set to track forwarded CAs to prevent duplicates
forwarded_cas = {}

# Resolve the destination group entity
async def get_destination_entity():
    try:
        return await client.get_entity(destination_group_id)
    except Exception as e:
        print(f"Error resolving destination entity: {e}")
        return None

# Resolve the trading bot entity
async def get_trading_bot_entity():
    try:
        return await client.get_entity(trading_bot_id)
    except Exception as e:
        print(f"Error resolving trading bot entity: {e}")
        return None

TIME_THRESHOLD = 86400  # 24 hours in seconds

# Function to periodically clear old entries from forwarded_cas
async def clean_forwarded_cas():
    while True:
        try:
            current_time = time.time()
            to_remove = [address for address, timestamp in forwarded_cas.items() 
                         if current_time - timestamp > TIME_THRESHOLD]

            for address in to_remove:
                del forwarded_cas[address]

            logging.info(f"Cleaned {len(to_remove)} old addresses from forwarded_cas.")
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

        # Run this check every 24hr
        await asyncio.sleep(86400)

        
# Event handler for new messages in all groups
@client.on(events.NewMessage(chats=[int(chat_id) for chat_id in group_notifiers.keys()]))
async def forward_message(event):
    try:
        message_text = event.message.message or ''
        group_id = str(event.chat_id)
        sender_id = event.sender_id

        # Check if the message is from the specified group with user filter
        if group_id == specified_group_id and sender_id != specified_user_id:
            return  # Skip messages not from the specified user in this group

        # Print incoming messages for debugging
        print(f"Incoming message from Group {group_id}, Sender {sender_id}: {message_text}")

        # Find all potential Solana contract addresses
        addresses = re.findall(solana_address_pattern, message_text)

        # Filter out addresses already forwarded
        current_time = time.time()
        new_addresses = [address for address in addresses if address not in forwarded_cas]
        if not new_addresses:
            print("No new Solana address or keywords found.")
            return

        # Track forwarded addresses with the current timestamp
        for address in new_addresses:
            forwarded_cas[address] = current_time

        # Search for full URLs matching keywords
        found_keywords = []
        for pattern in keyword_patterns:
            matches = re.findall(pattern, message_text)
            if matches:
                found_keywords.extend(matches)

        if new_addresses or found_keywords:
            # Get the notifier key for the group ID
            notifier_key = group_notifiers.get(group_id, '1')
            notifier = notifier_keys.get(notifier_key, 'Risky Gamble 🟪')

            # Prepare the forwarding message
            forward_message = f"{notifier}\n\n"
            if new_addresses:
                forward_message += f" {', '.join(new_addresses)}\n\n"
            if found_keywords:
                forward_message += f"{', '.join(found_keywords)}\n\n"
            forward_message += " "

            # Send message to destination group
            destination_entity = await get_destination_entity()
            if destination_entity:
                await client.send_message(destination_entity, forward_message)
                print(f"Forwarded message with CA: {new_addresses}, Keywords: {found_keywords} to destination group.")
            
            # Send message to trading bot
            trading_bot_entity = await get_trading_bot_entity()
            if trading_bot_entity:
                await client.send_message(trading_bot_entity, forward_message)
                print(f"Forwarded message with CA: {new_addresses}, Keywords: {found_keywords} to trading bot.")
    
    except Exception as e:
        print(f"Error: {e}")

# Keep the script alive
async def keep_alive():
    while True:
        await asyncio.sleep(60)

# Main function to start the client
async def main():
    await client.start()
    print("User client is running, listening for messages...")

    try:
        await asyncio.gather(keep_alive(), clean_forwarded_cas())
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        await client.disconnect()

# Start the client
with client:
    client.loop.run_until_complete(main())
