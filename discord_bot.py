import json
import logging

import discord
import requests
from discord.ext import commands

logging.basicConfig(format="[%(asctime)s] [%(levelname)-8s] - %(message)s", level=logging.INFO)

bot = commands.Bot(
    command_prefix="?",
    description="Bot that does cool stuff.")


def load_config():
    with open('config.json') as f:
        return json.load(f)


# @bot.event
# async def on_command_error(error, ctx):
#     await bot.send_message(ctx.message.channel, "Something went wrong. Probably a syntax error.")
#     print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
#     traceback.print_tb(error.original.__traceback__)
#     print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)


@bot.command(
    name="setname",
    hidden=True,
    pass_context=True
)
async def set_name(ctx, *, name):
    if ctx.message.author.id == bot.config['discord']['owner_client_id']:
        await bot.change_nickname(ctx.message.server.me, name)

        await bot.say("Bot name set to " + name + ".")
    else:
        await bot.say("You are not the bot owner!")


@bot.command(
    name="setavatar",
    hidden=True,
    pass_context=True
)
async def set_avatar(ctx, image_url):
    if ctx.message.author.id == bot.config['discord']['owner_client_id']:
        try:
            r = requests.get(image_url)

            await bot.edit_profile(avatar=r.content)
            await bot.say("Bot avatar set.")
        except requests.exceptions.MissingSchema:
            await bot.say("Invalid URL.")
        except discord.errors.InvalidArgument:
            await bot.say("Not a valid avatar.")


if __name__ == '__main__':
    bot.config = load_config()

    extensions = [
        'cogs.warcraftlogs',
        'cogs.rnjesus'
    ]

    for extension in extensions:
        try:
            logging.info('Loading extension {}'.format(extension))
            bot.load_extension(extension)
        except Exception as e:
            logging.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(bot.config['discord']['discord_token'])
