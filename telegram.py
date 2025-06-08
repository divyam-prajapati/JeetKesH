from telethon.sync import TelegramClient, events
import re
import time
import yaml
import asyncio
from dataset import ExpiringFIFOSet

async def get_caller_count(client: TelegramClient, contract_address: str) -> int:
    bot_username="@CallAnalyserBot"
    try:
        async with client.conversation(bot_username, timeout=5) as conv:
            await client.send_message(bot_username, contract_address)
            response = await conv.get_response()
            match = re.search(r'❇️\(Total Call\)🚀 \$.+ received calls from (\d+) callers', response.text)
            return int(match.group(1)) if match else 0
    except asyncio.TimeoutError:
        print("Timeout waiting for bot response")
    except Exception as e:
        print(f"Error getting caller count: {e}")
    return 0

async def start_telegram_listener(queue):
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    client = TelegramClient(
        config["telegram"]["session_name"],
        config["telegram"]["api_id"],
        config["telegram"]["api_hash"]
    )
    
    CONTRACT_REGEX = re.compile(r'\b[0-9a-zA-Z]{30,44}\b')
    ca_cache = ExpiringFIFOSet(max_size=100, expiry_seconds=1800)

    @client.on(events.NewMessage(chats=config["telegram"]["bronze_tier_channels"]))
    async def handler(event):
        if not event.message.text:
            return
            
        contracts = CONTRACT_REGEX.findall(event.message.text)
        if contracts:
            contract = contracts[0]
            is_new = await ca_cache.add(contract, {
                'source': event.chat.username,
                'timestamp': time.time()
            })

            if not is_new:
                return
        
            caller_count = await get_caller_count(client,contract)
            clean_msg = (f"{event.chat.username or event.chat.title}|{contract}|{caller_count}")
            # print(clean_msg)
            await queue.put(clean_msg) 

    await client.start()
    print("Telegram listener started...")
    await client.run_until_disconnected()
