from discord.ext import commands
from utils.data import get
from os import listdir


class ExtensionLoader(commands.Cog):
    def __init__(self, bot):
        self.config = get('config.json')
        self.bot = bot

    # Load All Possible Extensions:
    def load_extensions(self):
        print('-= Cogs =-')
        for cog in listdir('cogs'):
            if cog.endswith('.py') and cog not in self.config['ignored_cogs']:
                try:
                    print('🤎 - {} is loaded!'.format(cog[:-3]))
                    self.bot.load_extension(f'cogs.{cog[:-3]}')
                except Exception as e:
                    print('☠ - {} coudn\'t be loaded. {}'.format(cog[:-3], e))

    # Reload extension 'target':
    @commands.command()
    async def reload_extension(self, ctx, target: str):
        self.bot.reload_extension(target)
        await ctx.send('Reloaded extension {}, Mr. {}!'.format(target, ctx.message.author.mention))


def setup(bot):
    bot.add_cog(ExtensionLoader(bot))
