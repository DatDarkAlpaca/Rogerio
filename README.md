# Rogerio
TODO: redo
A Discord bot that turns on my minecraft server when I'm away.
Don't mind the mess. It's a mess.

To add this to your server, simply add "config.json" and add the following:

{
    "token": "Your_Secret_Token",

    "prefix": "!",

    "owners": [10000000000000, 10000101010010101],
    "valid_channels": [9417535875879524, 1000000000000],
    "admins": [1111111111111111],

    "ignored_cogs": ["__init__.py"],

    "server_dir": "C:\\Your\\Server\\Directory",
    "bot_dir": "D:\\Your\\Bot\\Directory",

    "temp_stream": "logs\\stream\\temp_stream.txt",
    "error_dir": "logs\\errors\\errors.txt",

    "java_command": "java -Xmx2048M -Xms2048M -jar server.jar nogui"
}
