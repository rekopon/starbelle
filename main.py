import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

# Load config
with open('config.json') as f:
    config = json.load(f)

GUILD_ID = 1084896922671775844  # Your Discord server (guild) ID

bot = commands.Bot(command_prefix='!', intents=intents)

# Load all cogs asynchronously
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            print(f"Loading: {filename}")
            await bot.load_extension(f'cogs.{filename[:-3]}')

# When the bot is ready
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    await load_extensions()
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))  # Instant slash command sync

# Slash command: /sync
@bot.tree.command(name="sync", description="Manually sync slash commands")
async def sync(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    await interaction.followup.send("✅ Slash commands synced!", ephemeral=True)

# Start the bot
bot.run(os.getenv("TOKEN"))
