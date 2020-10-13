from utils.bot import Bot, HelpFormat
from utils.data import get
from cogs.extension_loader import ExtensionLoader


# JSON File:
config = get('config.json')

# Bot Instance:
bot = Bot(
    command_prefix=config['prefix'], prefix=config['prefix'],
    owner_ids=config['owners'], command_attrs=dict(hidden=True), help_command=HelpFormat()
)


# Extension Loading:
ExtensionLoader(bot).load_extensions()


# Run:
try:
    bot.run(config['token'])
except Exception as e:
    print('[Bot]: Failed to log-in. {}'.format(e))
