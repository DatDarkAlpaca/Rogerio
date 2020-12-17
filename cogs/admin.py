from discord.ext import commands
from discord.utils import get
from discord import Member


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self):
        pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, user: Member, before, after):
        role = get(user.guild.roles, name="Call")
        
        if before.channel is None and after.channel is not None:
            await user.add_roles(role)
        elif before.channel and not after.channel:
            await user.remove_roles(role)

    @commands.command()
    async def nuke(self, ctx):
        await ctx.channel.purge(limit=500)


def setup(bot):
    bot.add_cog(Administration(bot))
