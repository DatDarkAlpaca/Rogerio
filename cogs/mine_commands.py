from discord.ext import commands


class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Say as 'name' Command:
    @commands.command()
    async def say_as(self, ctx, name: str, *args):
        msg = ' '.join(args)
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'tellraw @a ["<{}> {}"]'.format(name, msg))

    # Say as 'name' Command:
    @commands.command()
    async def say(self, ctx, *args):
        msg = ' '.join(args)
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'say {}"]'.format(msg))

    # List Players Command:
    @commands.command()
    async def list(self, ctx):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'list')

    # List Players Command:
    @commands.command()
    async def reload(self, ctx):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'reload')

    # Teleport Player Command:
    @commands.command()
    async def tp(self, ctx, arg0: str, arg1: str):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'tp {} {}'.format(arg0, arg1))

    # Give Command:
    @commands.command()
    async def give(self, ctx, name: str, item: str, amount: str):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'give {} {} {}'.format(name, item, amount))

    # Get Position Command:
    @commands.command()
    async def _get(self, ctx, target: str, *args):
        arg = ' '.join(args)
        arg = arg.lower()

        if arg == 'position':
            await self.get_player_position(ctx, target)

    # [Overloaded] Summon Command (Position):
    @commands.command()
    async def summon(self, ctx, entity: str, x: str, y: str, z: str, nbt: str):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {} {}'.format(entity, x, y, z, nbt))

    # [Overloaded] Summon Command (Player Position):
    @commands.command()
    async def summon(self, ctx, entity: str, to_player: str):
        (x, y, z) = self.get_player_position(ctx, to_player)
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {}'.format(entity, x, y, z))

    # [Overloaded] Summon Amount Command (Position):
    @commands.command()
    async def summon_for(self, ctx, entity: str, x: str, y: str, z: str, nbt: str, amount: int):
        for ent in range(amount):
            await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {} {}'.format(entity, x, y, z, nbt))

    # [Overloaded] Summon Amount Command (Player):
    @commands.command()
    async def summon_for(self, ctx, entity: str, to_player: str, amount: int):
        (x, y, z) = self.get_player_position(ctx, to_player)
        for ent in range(amount):
            await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {}'.format(entity, x, y, z))

    # -=-=-= :  Custom Execute Helpers :  =-=-=-=- #

    # Retrieves the position of the player using data tags:
    async def get_player_position(self, ctx, target: str):
        # Executes the data command:
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'data get entity {} Pos'.format(target))

        # Attempts to retrieve the data:
        pos = []
        if 'entity data:' in self.bot.get_cog('MinecraftAdmin').reply:
            replied = self.bot.get_cog('MinecraftAdmin').reply.split('data:', 1)[-1]
            pos.extend([replied.split(',').replace('[', '')])
        else:
            await ctx.send('I\'m sorry, Mr. {}, but I couldn\'t find the coordinates of {} :('
                           .format(ctx.message.author.mention, target))
        return pos


def setup(bot):
    bot.add_cog(MinecraftCommands(bot))
