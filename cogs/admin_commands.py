import discord
from discord.ext import commands
from discord import app_commands
from database.db import Database

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()

    @app_commands.command(name="addachievement", description="Add a new achievement")
    async def add_achievement(
        self,
        interaction: discord.Interaction,
        name: str,
        description: str,
        type: str,
        role_id: int,
        threshold: int = None,
        channel_id: int = None
    ):
        self.db.add_achievement(name, description, type, role_id, threshold, channel_id)
        await interaction.response.send_message(f"✅ Achievement '{name}' added.")

    @app_commands.command(name="approve", description="Approve a manual achievement")
    async def approve_manual(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        achievement_name: str
    ):
        self.db.grant_manual_achievement(user.id, achievement_name)
        await interaction.response.send_message(f"✅ {user.display_name} granted achievement '{achievement_name}'.")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))

