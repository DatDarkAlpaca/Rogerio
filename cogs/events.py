from discord.ext.commands import errors
from discord.ext import commands
from datetime import datetime, date
from utils import data


class Events(commands.Cog):
    def __init__(self, bot, debug=False):
        self.config = data.get('config.json')
        self.debug = debug
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        # Logging the error:
        try:
            with open(self.config['error_dir'], mode='a') as f:
                f.write('{} : {} \n'.format(date.today(), err))
        except Exception as e:
            print('[Error]: {}'.format(e))

        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandInvokeError):
            error = data.traceback_maker(err.original)

            if '2000 or fewer' in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send(
                    "You attempted to make the command display more than 2,000 characters...\n"
                    "Both error and command will be ignored."
                )

            await ctx.send(f'There was an error processing the command ;-;\n{error}')

        elif isinstance(err, errors.CheckFailure):
            pass

        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send('You\'ve reached max capacity of command usage at once, please finish the previous one...')

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown... try again in {err.retry_after:.2f} seconds.')

        elif isinstance(err, errors.CommandNotFound):
            pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.message.channel.id not in self.config['valid_channels']:
            return

        if self.debug:
            try:
                print(f'{ctx.guild.name} > {ctx.author} > {ctx.message.clean_content}')
            except AttributeError:
                print(f'Private message > {ctx.author} > {ctx.message.clean_content}')

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.utcnow()
        print('Ready: {} | Servers: {}'.format(self.bot.user, len(self.bot.guilds)))


def setup(bot):
    bot.add_cog(Events(bot))
