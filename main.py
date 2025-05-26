import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()

# Load config from file
with open('config.json') as f:
    config = json.load(f)

bot = commands.Bot(command_prefix='!', intents=intents)

# Load all cogs from ./cogs/
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            print(f"Loading: {filename}")
            await bot.load_extension(f'cogs.{filename[:-3]}')

# When bot is ready
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} ({bot.user.id})')
    await load_extensions()
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} global command(s)")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

# Manual slash command to sync again
@bot.tree.command(name="sync", description="Manually sync slash commands")
async def manual_sync(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        synced = await bot.tree.sync()
        await interaction.followup.send(f"✅ Synced {len(synced)} global command(s).", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Sync failed: {e}", ephemeral=True)
        print(f"❌ Sync command failed: {e}")

# Start the bot using your token
bot.run(os.getenv("TOKEN"))
