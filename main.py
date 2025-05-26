import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

# Load config
with open('config.json') as f:
    config = json.load(f)

GUILD_ID = 1084896922671775844  # Your server ID

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            print(f"Loading: {filename}")
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} ({bot.user.id})')
    await load_extensions()
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔁 Synced {len(synced)} command(s) to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

@bot.tree.command(name="sync", description="Manually sync slash commands")
async def manual_sync(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        await interaction.followup.send(f"✅ Synced {len(synced)} command(s) to this server.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Failed to sync: {e}", ephemeral=True)
        print(f"❌ Sync command failed: {e}")

bot.run(os.getenv("TOKEN"))
