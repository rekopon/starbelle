import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

# Load config
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='!', intents=intents)

# Load all cogs in /cogs
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            print(f"🔄 Loading: {filename}")
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} ({bot.user.id})')
    await load_extensions()

    try:
        synced = await bot.tree.sync()  # Only sync ONCE globally
        print(f"✅ Synced {len(synced)} global command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

bot.run(os.getenv("TOKEN"))
