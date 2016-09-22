import json
import logging
import sys
import traceback

from discord.ext import commands

logging.basicConfig(format="[%(asctime)s] [%(levelname)-8s] - %(message)s", level=logging.INFO)

bot = commands.Bot(
    command_prefix="?",
    description="Bot that does cool stuff.")


def load_config():
    with open('config.json') as f:
        return json.load(f)


@bot.event
async def on_command_error(error, ctx):
    await bot.send_message(ctx.message.channel, "Something went wrong. Probably a syntax error.")
    print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
    traceback.print_tb(error.original.__traceback__)
    print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

# @commands.command(
#     name="setname",
#     hidden=True
# )
# async def set_name(name):



if __name__ == '__main__':
    config = load_config()

    extensions = [
        'cogs.warcraftlogs',
        'cogs.rnjesus'
    ]

    bot.config = config

    for extension in extensions:
        try:
            logging.info('Loading extension {}'.format(extension))
            bot.load_extension(extension)
        except Exception as e:
            logging.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(config['discord']['discord_token'])
