import json
import logging

from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

# fileHandler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# fileHandler.setFormatter(formatter)
# logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

bot = commands.Bot(
    command_prefix="?",
    description="Bot that does cool stuff.")


def load_config():
    with open('config.json') as f:
        return json.load(f)


if __name__ == '__main__':
    config = load_config()

    extensions = ['cogs.wow']

    bot.config = config

    for extension in extensions:
        try:
            logger.info('Loading extension {}'.format(extension))
            bot.load_extension(extension)
        except Exception as e:
            logger.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(config['discord_token'])

