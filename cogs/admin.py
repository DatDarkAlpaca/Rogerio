from discord.ext import commands


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self):
        pass

    @commands.command()
    async def purge(self, ctx, amount: int):
        if amount > 500:
            amount = 100
        elif amount <= 0:
            return

        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def nuke(self, ctx):
        await ctx.channel.purge(limit=500)


def setup(bot):
    bot.add_cog(Administration(bot))
