from telethon.sync import TelegramClient, events
import re
import yaml
import asyncio

async def start_telegram_listener(queue):
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    client = TelegramClient(
        config["telegram"]["session_name"],
        config["telegram"]["api_id"],
        config["telegram"]["api_hash"]
    )
    
    CONTRACT_REGEX = re.compile(r'\b[0-9a-zA-Z]{30,44}\b')
    COIN_SYMBOL_REGEX = re.compile(r'\$[A-Za-z0-9.]+|\$\$[A-Za-z0-9.]+')

    @client.on(events.NewMessage(chats=config["telegram"]["input_channels"]))
    async def handler(event):
        if not event.message.text:
            return
            
        contracts = CONTRACT_REGEX.findall(event.message.text)
        coin_symbols = COIN_SYMBOL_REGEX.findall(event.message.text)

        if contracts:
            contract = contracts[0] if contracts else 'N/A'
            token = coin_symbols[0] if coin_symbols else 'N/A'
            
            clean_msg = (f"{event.chat.username or event.chat.title}\n{token}\n{contract}")

            await queue.put(clean_msg) 

    await client.start()
    print("Telegram listener started...")
    await client.run_until_disconnected()

# TODO:
# filter repetation
# Other Dets (mc, vol, )
# Called at __
# no. of callers __
# 