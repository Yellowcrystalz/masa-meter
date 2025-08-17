import discord
from discord import app_commands
from discord.ext import commands


class MasaMeter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Online!")

    @app_commands.command(name="increment", description="Increments the Masa Meter")
    async def increment(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "It works!",
            ephemeral=True
        )

    @app_commands.command(name="history", description="Shows the History")
    async def history(self, interaction: discord.Interaction):
        await interaction.response.send_message("doesn't work yet")


async def setup(bot):
    await bot.add_cog(MasaMeter(bot))
