from discord.ext import commands


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self):
        pass

    @commands.command()
    async def nuke(self, ctx):
        await ctx.channel.purge(limit=500)


def setup(bot):
    bot.add_cog(Administration(bot))
