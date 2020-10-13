from discord.ext import commands


class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Minecraft "Tellraw" with a custom name:
    @commands.command()
    async def say_as(self, ctx, name: str, *args):
        msg = ' '.join(args)
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'tellraw @a ["<{}> {}"]'.format(name, msg))

    # Minecraft "Say":
    @commands.command()
    async def say(self, ctx, *args):
        msg = ' '.join(args)
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'say {}"]'.format(msg))

    # Minecraft "List":
    @commands.command()
    async def list(self, ctx):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'list')

    # Minecraft "Reload" server:
    @commands.command()
    async def reload(self, ctx):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'reload')

    # Minecraft "Teleport":
    @commands.command()
    async def tp(self, ctx, arg0: str, arg1: str):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'tp {} {}'.format(arg0, arg1))

    # Minecraft "Give":
    @commands.command()
    async def give(self, ctx, name: str, item: str, amount: str):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'give {} {} {}'.format(name, item, amount))

    # Internal Data Getter [WIP]:
    @commands.command()
    async def _get(self, ctx, target: str, *args):
        arg = ' '.join(args)
        arg = arg.lower()

        if arg == 'position':
            await self.get_player_position(ctx, target)

    # Minecraft "Summon" at position:
    @commands.command()
    async def summon(self, ctx, entity: str, x: str, y: str, z: str, nbt: str):
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {} {}'.format(entity, x, y, z, nbt))

    # Minecraft "Summon" at target's position [WIP]:
    @commands.command()
    async def summon(self, ctx, entity: str, to_player: str):
        (x, y, z) = self.get_player_position(ctx, to_player)
        await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {}'.format(entity, x, y, z))

    # Minecraft "Summon" at position 'amount' times:
    @commands.command()
    async def summon_for(self, ctx, entity: str, x: str, y: str, z: str, nbt: str, amount: int):
        for ent in range(amount):
            await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {} {}'.format(entity, x, y, z, nbt))

    # Minecraft "Summon" at player's position 'amount' times [WIP]:
    @commands.command()
    async def summon_for(self, ctx, entity: str, to_player: str, amount: int):
        (x, y, z) = self.get_player_position(ctx, to_player)
        for ent in range(amount):
            await self.bot.get_cog('MinecraftAdmin').execute(ctx, 'summon {} {} {} {}'.format(entity, x, y, z))

    # -=-=-= :  Custom Execute Helpers :  =-=-=-=- #

    # Retrieves the player's position using its internal data:
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
