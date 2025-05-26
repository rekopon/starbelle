import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

# Load config
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='!', intents=intents)

# Load all cogs/extensions asynchronously
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Bot ready event
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    await bot.tree.sync()  # Global sync (may take time)
    await load_extensions()

# Slash command to manually sync commands
@bot.tree.command(name="sync", description="Manually sync slash commands")
async def sync(interaction: discord.Interaction):
    await bot.tree.sync()
    await interaction.response.send_message("✅ Slash commands synced!", ephemeral=True)

bot.run(os.getenv("TOKEN"))

