import json
import logging
import sys
import traceback

import discord
import requests
from discord.ext import commands
from discord.ext.commands import CommandNotFound, UserInputError, NoPrivateMessage, CheckFailure, DisabledCommand, \
    CommandInvokeError, CommandOnCooldown, CommandError, MissingRequiredArgument, TooManyArguments, BadArgument

logging.basicConfig(format="[%(asctime)s] [%(levelname)-8s] - %(message)s", level=logging.INFO)

bot = commands.Bot(
    command_prefix="?",
    description="Bot that does cool stuff.",
    help_attrs=dict(hidden=True)
)


def load_config():
    with open('config.json') as f:
        return json.load(f)


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, CommandNotFound):
        await bot.send_message(ctx.message.channel,
                               "CommandNotFound:\nThis command does not exist.")
    elif isinstance(error, UserInputError):
        await bot.send_message(ctx.message.channel,
                               "UserInputError")
    elif isinstance(error, NoPrivateMessage):
        await bot.send_message(ctx.message.channel,
                               "NoPrivateMessage:\nThis command cannot be used through private messages.")
    elif isinstance(error, CheckFailure):
        await bot.send_message(ctx.message.channel,
                               "CheckFailure:\nOne of the requirements for this command was not met.")
    elif isinstance(error, DisabledCommand):
        await bot.send_message(ctx.message.channel,
                               "DisabledCommand:\nThis command is not enabled.")
    elif isinstance(error, CommandInvokeError):
        await bot.send_message(ctx.message.channel,
                               "CommandInvokeError:\nSomething went wrong while trying to execute your command.")
    elif isinstance(error, CommandOnCooldown):
        await bot.send_message(ctx.message.channel,
                               "CommandOnCooldown:\nThis command is on cooldown.")
    elif isinstance(error, CommandError):
        await bot.send_message(ctx.message.channel,
                               "CommandError:\nSomething went wrong while trying to execute your command.")
    elif isinstance(error, MissingRequiredArgument):
        await bot.send_message(ctx.message.channel,
                               "MissingRequiredArgument:\nOne or more parameters required to execute this command are missing.")
    elif isinstance(error, TooManyArguments):
        await bot.send_message(ctx.message.channel,
                               "TooManyArguments:\nToo many arguments were given to the command.")
    elif isinstance(error, BadArgument):
        await bot.send_message(ctx.message.channel,
                               "BadArgument:\nInvalid argument.")
    else:
        await bot.send_message(ctx.message.channel,
                               "Something went very, very wrong...")

    print('Exception thrown while executing command {}'.format(ctx.command), file=sys.stderr)
    traceback.print_tb(error.original.__traceback__)
    print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)


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
    else:
        await bot.say("You are not the bot owner!")


@bot.command(
    name="setplaying",
    hidden=True,
    pass_context=True
)
async def set_playing(ctx, *, playing=None):
    if ctx.message.author.id == bot.config['discord']['owner_client_id']:
        await bot.change_status(game=discord.Game(name=playing))
        await bot.say("Playing status set.")
    else:
        await bot.say("You are not the bot owner!")

if __name__ == '__main__':

    bot.config = load_config()

    extensions = [
        'cogs.warcraftlogs',
        'cogs.rnjesus',
        # 'cogs.simulationcraft'
        'cogs.sounds'
    ]

    for extension in extensions:
        try:
            logging.info('Loading extension {}'.format(extension))
            bot.load_extension(extension)
        except Exception as e:
            logging.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))

    bot.run(bot.config['discord']['discord_token'])
