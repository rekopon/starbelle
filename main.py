import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('__'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv("TOKEN"))
