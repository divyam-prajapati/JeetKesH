import discord
from discord import Embed, Colour, ButtonStyle, ActionRow, Button
import yaml
from discord.ext import commands
from datetime import datetime
import aiohttp

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

async def create_jeet_card(details: str) -> Embed:
    data = {}
    
    detail = details.split('|')
    data['source']=detail[0]
    data['ca']=detail[1]
    data['calls']=detail[2]

    async with aiohttp.ClientSession() as session:
        dex_url = f"https://api.dexscreener.com/latest/dex/tokens/{data['ca']}"
        async with session.get(dex_url) as resp:
            dex_data = await resp.json()
            data['mc'] = dex_data['pairs'][0]['fdv'] if dex_data['pairs'] else 'N/A'
            data['vol24'] = dex_data['pairs'][0]['volume']['h24'] if dex_data['pairs'] else 'N/A'
            data['vol1'] = dex_data['pairs'][0]['volume']['h1'] if dex_data['pairs'] else 'N/A'
            data['chain'] = dex_data['pairs'][0]['chainId']
            data['img'] = dex_data['pairs'][0]['info']['header']
            data['name'] = dex_data['pairs'][0]['baseToken']['name']
            data['token'] = dex_data['pairs'][0]['baseToken']['symbol']



    body = f"""
💹 MC:`{data['mc']}`
📈 VOL:`{data['vol24']}` 
📉 1H:`{data['vol1']}`
☎️ CALLS:`{data['calls']}`
🤙 BY:`{data['source']}`
📋 CA:`{data['ca']}`

<a:fire:1380742987843239946> **New Jeet Signal!** <a:letsgo:1380746421929771128>

💡 **Tips :**
- Ape now, regret later 😉
- **ALL CA HERE ARE SUBJECTED TO GO TO 0**
- TAKE __**PROFITS AT 2X**__ MFERR
"""

    embed = discord.Embed(
      title=f"{data['token']}",
      url=f"https://dexscreener.com/{data['chain']}/{data['ca']}",
      description=body,
      colour=Colour.gold(),
      timestamp=datetime.now()
    )
    embed.set_author(
        name=f"{data['name']}",
    )
    embed.set_image(url=f"{data['img']}")
    embed.add_field(name="📑",value=f"> ```{data['ca']}```")
    embed.set_footer(
        text="DYOR !! PIKA.. PIKA...",
        icon_url="https://cdn3.emoji.gg/emojis/58668-pixelpikachu.gif"
    )

    return embed

async def start_discord_sender(queue):
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Discord bot logged in as {bot.user}")
        test_channel = bot.get_channel(config["discord"]["test_channel"])
        
        while True:
            dets = await queue.get() 
            message = await create_jeet_card(dets)
            try:
                test_message = await test_channel.send(embed=message)
                await test_message.add_reaction('<a:watch:1380744932750528613>')
                print(f"✅ Forwarded to Discord")
            except Exception as e:
                print(f"❌ Discord send failed: {e}")

    await bot.start(config["discord"]["bot_token"])