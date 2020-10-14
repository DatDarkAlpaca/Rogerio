from asyncio import create_subprocess_shell, subprocess, sleep
from subprocess import CREATE_NEW_PROCESS_GROUP
from signal import CTRL_C_EVENT

from discord.ext import commands, tasks
from discord import File

from utils import permissions, data
from utils.stream import *

from os import kill, system


# Converts strings into booleans:
def string_to_bool(value):
    value = value.lower()

    if value == 'true' or value == '1' or value == 'yes':
        return True
    elif value == 'false' or value == '0' or value == 'no' or value.isspace():
        return False
    else:
        return False


class MinecraftAdmin(commands.Cog):
    def __init__(self, bot):
        self.server_subproc, self.reply, self.message = None, None, None

        self.enabled_read, self.running, self.turned_on = False, False, False
        self.config = data.get('config.json')
        self.bot = bot

        # Tasks:
        self.send_stream.start()

    # Unload the tasks:
    def cog_unload(self):
        self.send_stream.cancel()

    @commands.command()
    async def server_start(self, ctx, stream: str = '0'):
        # Check if the server is running:
        if self.running:
            await ctx.send('Rogerio already started the server. You can use "> stop server" tho, {}!'
                           .format(ctx.message.author.mention))
            return

        # Check whether the user has enough permissions:
        if permissions.is_owner(ctx) or permissions.is_admin(ctx):
            self.running = True

            # Change cwd to server directory:
            chdir(self.config['server_dir'])

            # Open the subprocess:
            java_cmd = self.config['java_command']
            self.server_subproc = await create_subprocess_shell(java_cmd, stdout=subprocess.PIPE,
                                                                stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                                                cwd=self.config['server_dir'],
                                                                creationflags=CREATE_NEW_PROCESS_GROUP)
            # Send a little message:
            if not string_to_bool(stream):
                await ctx.send('Rogerio has turned on the server, Mr. {}'.format(ctx.message.author.mention))
            else:
                self.enabled_read = string_to_bool(stream)
                await ctx.send('Rogerio has turned on the server **with streams**, Mr. {}!'.format(ctx.message.author.mention))

        # Change cwd back to the bot directory:
        chdir(self.config['bot_dir'])

    # Stops the server via minecraft commands, then closes the process:
    @commands.command()
    async def server_close(self, ctx):
        # Close the server:
        await self.execute(ctx, 'stop')

        # TODO: Find a way to wait the entire subprocess stop its execution rather than waiting ten seconds..
        await sleep(delay=10)

        # Close the process:
        await self.server_abrupt(ctx)

    # Stop the server abruptly (also deletes the temp stream file):
    @commands.command()
    async def server_abrupt(self, ctx):
        # Performs the necessary checks:
        self.initial_check(ctx)

        # Change variables:
        self.running, self.turned_on = False, False

        # Delete the temporary stream file:
        delete_stream(self.config)

        # Kill the subprocess with a signal and the java.exe process:
        kill(self.server_subproc.pid, CTRL_C_EVENT)
        system("taskkill /f /im java.exe")

        # Clear the subprocess holder:
        self.server_subproc = None

        await ctx.send('Rogerio closed the server, {}! :)'.format(ctx.message.author.mention))

    @tasks.loop(seconds=0.1)
    async def send_stream(self):
        try:
            if self.running:
                if not self.server_subproc.stdout:
                    return

                # Get the data:
                data_out = await self.server_subproc.stdout.readline()
                self.reply = data_out.decode().strip()

                # Reply that represents the end of the 'loading phase' of the server:
                if 'For help, type "help"' in self.reply:
                    self.turned_on = True

                # Appends the current stream's line to a temporary file:
                save_stream(self.config, self.reply)

            if self.enabled_read and self.reply:
                for id in self.config['valid_channels']:
                    channel = self.bot.get_channel(id)

                    # Check if it's the first message then send/edit:
                    if self.message is None and channel is not None:
                        self.message = await channel.send(self.reply)
                    elif self.message is not None:
                        await sleep(0.05)
                        await self.message.edit(content=self.reply)

        except UnicodeDecodeError as u:
            print('[Unicode]: {}'.format(u))
        except TypeError as t:
            print('[TypeError]: {}'.format(t))
        except Exception as e:
            print('[Error]: {}'.format(e))

    @send_stream.before_loop
    async def before_send(self):
        print('[Stream]: Waiting for the bot to load...')
        await self.bot.wait_until_ready()

    # Switches the stream state:
    @commands.command()
    async def turn_stream(self, ctx, value: str):
        # Performs the necessary checks:
        self.initial_check(ctx)

        # Switches the variable if no value is passed:
        if value == '':
            self.enabled_read = not self.enabled_read

        # Modifies the stream boolean variable:
        self.enabled_read = string_to_bool(value)

        if string_to_bool(value):
            await ctx.send('Rogerio has turned the stdout stream on for reading, {}!'.format(ctx.message.author.mention))
        else:
            await ctx.send('Rogerio has turned the stdout stream off, {}!'.format(ctx.message.author.mention))

    # Writes to stdin:
    @commands.command()
    async def execute(self, ctx, *args):
        # Performs the necessary checks:
        self.initial_check(ctx)

        # Check if there is an open subprocess:
        if not self.server_subproc:
            return

        cmd = ' '.join(args)
        self.server_subproc.stdin.write((cmd + '\n').encode())

        await ctx.send('Command written: {}'.format(cmd))

    # -=-=-= :  Helper Commands :  =-=-=-=- #

    # Checks whether the server is truly turned on:
    @commands.command()
    async def check_turned(self, ctx):
        if self.turned_on:
            await ctx.send('{}, the server is **READY!**'.format(ctx.message.author.mention))
        else:
            await ctx.send('{}, the server is still not ready!'.format(ctx.message.author.mention))

    # Sends a file with the current server properties:
    @commands.command()
    async def retrieve_properties(self, ctx):
        # Check whether the user has enough permissions.
        if permissions.is_owner(ctx) or permissions.is_admin(ctx):
            # Change back to the bot directory just in case:
            chdir(self.config['bot_dir'])

            try:
                with open('{}\\server.properties'.format(self.config['server_dir']), encoding='utf-8', mode='r+'):
                    for id in self.config['valid_channels']:
                        channel = self.bot.get_channel(id)

                        await channel.send(file=File('{}\\server.properties'
                                                     .format(self.config['server_dir']), 'Properties.txt'))
            except Exception as e:
                print('[Error]: {}'.format(e))

    # Modify server.properties:
    @commands.command()
    async def modify_properties(self, ctx, argument: str, *args):
        properties_path = '{}\\server.properties'.format(self.config['server_dir'])
        value = ' '.join(args)

        # Checks the argument passed and modifies it in the file:
        data.modify_existing_argument(properties_path, argument, value)

        await ctx.send('Modified the argument {} for you, {}!'.format(argument, ctx.message.author.mention))

    # Checks the permissions and whether the server is turned on:
    def initial_check(self, ctx):
        if not permissions.is_owner(ctx) or not permissions.is_admin(ctx) or not self.running:
            return

    # -=-=-= :  Stream Commands :  =-=-=-=- #

    # Sends the current stream:
    @commands.command()
    async def retrieve_stream(self, ctx):
        self.initial_check(ctx)

        # Change back to the bot directory (just in case):
        chdir(self.config['bot_dir'])

        with open(self.config['temp_stream'], encoding='utf-8', mode='r+'):
            for id in self.config['valid_channels']:
                channel = self.bot.get_channel(id)

                if channel:
                    try:
                        # Try to send the file:
                        await channel.send(file=File(self.config['temp_stream'], 'Stream.txt'))
                    except Exception as e:
                        print('[Error]: {}'.format(e))

    # Resets the message editing position:
    @commands.command()
    async def bring_stream(self, ctx):
        self.initial_check(ctx)

        if self.message is not None:
            self.message = None
            await ctx.send('Brought the console back down!, {}'.format(ctx.message.author.mention))
        else:
            await ctx.send('I don\'t think the server or the stream are turned on.')


def setup(bot):
    bot.add_cog(MinecraftAdmin(bot))
