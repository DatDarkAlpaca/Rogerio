from discord.ext import commands
from discord import DMChannel
from utils import data


async def check_permissions(ctx, perms, *, check=all):
    if ctx.author.id in data.get('config.json')['owners'] or ctx.author.id in data.get('config.json')['admins']:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def predicate(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(predicate)


async def check_private(ctx, member):
    try:
        if member == ctx.author:
            return await ctx.send(f'You can\'t {ctx.command.name} yourself')
        if member.id == ctx.bot.user.id:
            return await ctx.send('.......')

        if ctx.author.id in data.get('config.json')['owners']:
            return False

        # Now permission check
        owners = data.get('config.json')['owners']
        if member.id in owners:
            if ctx.author.id not in owners:
                return await ctx.send(f'I can\'t {ctx.command.name} my creator, bitch')
            else:
                pass

        if member.id == ctx.guild.owner.id:
            return await ctx.send(f'You can\'t {ctx.command.name} the owner, bitch')

        if ctx.author.top_role == member.top_role:
            return await ctx.send(f'You can\'t {ctx.command.name} someone who has the same permissions as you...')

        if ctx.author.top_role < member.top_role:
            return await ctx.send(f'Nope, you can\'t {ctx.command.name} someone higher than yourself.')

    except Exception:
        pass


def is_owner(ctx):
    return ctx.message.author.id in data.get('config.json')['owners']


def is_admin(ctx):
    return ctx.message.author.id in data.get('config.json')['admins']


def can_send(ctx):
    return isinstance(ctx.channel, DMChannel) or ctx.channel.permissions_for(ctx.guild.me).send_messages


def can_embed(ctx):
    return isinstance(ctx.channel, DMChannel) or ctx.channel.permissions_for(ctx.guild.me).embed_links


def can_upload(ctx):
    return isinstance(ctx.channel, DMChannel) or ctx.channel.permissions_for(ctx.guild.me).attach_files


def can_react(ctx):
    return isinstance(ctx.channel, DMChannel) or ctx.channel.permissions_for(ctx.guild.me).add_reactions


def is_nsfw(ctx):
    return isinstance(ctx.channel, DMChannel) or ctx.channel.is_nsfw()
