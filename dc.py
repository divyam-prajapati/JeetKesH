import discord
from discord import Embed, Colour, ButtonStyle, ActionRow, Button
import yaml
from discord.ext import commands

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

async def create_jeet_card(source: str, token: str, ca: str) -> Embed:
    
    des = """
💡 **Tips :**  
- **Ape now, regret later** 😉 
- **ALL CA HERE ARE SUBJECTED TO GO TO 0**
- TAKE __**PROFITS AT 2X**__ MFER\n\n
"""
    embed = Embed(
        title = "<a:fire:1380742987843239946> **New Jeet Signal!** <a:letsgo:1380746421929771128>",
        description = des,
        color = Colour.gold()
    )
    embed.add_field(name = f"📡 Source : ", value = f'{source}', inline=True)
    embed.add_field(name = f"💰 Token  : ", value = f'{token}', inline=True)
    embed.add_field(name = f"📋 CA :", value=f"\n`{ca}`\n", inline=False)
    
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
        channel = bot.get_channel(config["discord"]["channel_id"])
        test_channel = bot.get_channel(config["discord"]["test_channel"])
        
        while True:
            dets = await queue.get() 
            dets = dets.split('\n')# [Source, Token, CA] 
            message = await create_jeet_card(dets[0],dets[1],dets[2])
            try:
                sent_message = await channel.send(embed=message)
                await sent_message.add_reaction('<a:watch:1380744932750528613>')
                await sent_message.add_reaction('<:UP:1380763722733326458>')
                await sent_message.add_reaction('<:think:1380755163882459168>')
                await sent_message.add_reaction('<a:fire:1380742987843239946>')

                test_message = await test_channel.send(embed=message)
                await test_message.add_reaction('<a:watch:1380744932750528613>')
                await test_message.add_reaction('<:UP:1380763722733326458>')
                await test_message.add_reaction('<:think:1380755163882459168>')
                await test_message.add_reaction('<a:fire:1380742987843239946>')
                print(f"✅ Forwarded to Discord")
            except Exception as e:
                print(f"❌ Discord send failed: {e}")

    await bot.start(config["discord"]["bot_token"])


# embed = discord.Embed(title="$BLURREDCAT",
#                       url="https://dexscreener.com/solana/7nEQWs27SWTrs774uup2cEuo7RiLJ5PV2nCU1u1tpump",
#                       description="🔥 **New Jeet Signal!** 💸\n\n💡 Tips :\n- Ape now, regret later 😉\n- ALL CA HERE ARE SUBJECTED TO GO TO 0\n- TAKE PROFITS AT 2X MFERR",
#                       colour=0x808040,
#                       timestamp=datetime.now())

# embed.set_author(name="KOLscope",
#                  icon_url="https://cdn.worldvectorlogo.com/logos/solana.svg")

# embed.add_field(name="💹MC",
#                 value="3.4M",
#                 inline=True)
# embed.add_field(name="📈Vol",
#                 value="11.4M",
#                 inline=True)
# embed.add_field(name="📋 CA :",
#                 value="> ```egbwzutov9htjiscvuczzkytrkuwobvuoejnhc5bpump```",
#                 inline=False)
# embed.add_field(name="📞 Called at",
#                 value="500k",
#                 inline=True)
# embed.add_field(name="🎙️Callers",
#                 value="7",
#                 inline=True)

# embed.set_image(url="https://s3.tradingview.com/q/qdazKFlf_big.png")

# embed.set_thumbnail(url="https://static2.tgstat.ru/channels/_0/1c/1c1d16c0b508c972066f453fda815cd5.jpg")

# embed.set_footer(text="DYOR !! PIKA.. PIKA...",
#                  icon_url="https://cdn3.emoji.gg/emojis/58668-pixelpikachu.gif")

# await ctx.send(embed=embed)