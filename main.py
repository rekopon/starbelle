import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

# Load config
with open('config.json') as f:
    config = json.load(f)

GUILD_ID = 806263779238477824  # 👈 Replace this with your server's ID

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    await load_extensions()
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))  # 👈 Fast sync for your server

# Manual sync command
@bot.tree.command(name="sync", description="Manually sync slash commands")
async def sync(interaction: discord.Interaction):
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    await interaction.response.send_message("✅ Slash commands synced (guild only).", ephemeral=True)

bot.run(os.getenv("TOKEN"))


