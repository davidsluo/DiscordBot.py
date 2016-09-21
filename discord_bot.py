import json
import logging

from discord.ext import commands

logging.basicConfig(format="[%(asctime)s] [%(levelname)-8s] - %(message)s", level=logging.INFO)

bot = commands.Bot(
    command_prefix="?",
    description="Bot that does cool stuff.")


def load_config():
    with open('config.json') as f:
        return json.load(f)


if __name__ == '__main__':
    config = load_config()

    extensions = [
        # 'cogs.wow',
        'cogs.warcraftlogs'
    ]

    bot.config = config

    for extension in extensions:
        try:
            logging.info('Loading extension {}'.format(extension))
            bot.load_extension(extension)
        except Exception as e:
            logging.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(config['discord_token'])

