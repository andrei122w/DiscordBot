import discord
from discord.ext import commands
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Botul s-a conectat la Discord ca utilizatorul {bot.user}.")
    
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    token = os.getenv("TOKEN")
    if not token:
        raise RuntimeError("TOKEN is missing. Set it in your .env file or environment.")

    async with bot:
        await load_extensions()
        await bot.start(token)

asyncio.run(main())
