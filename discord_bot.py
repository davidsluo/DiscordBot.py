import asyncio
import json
import logging
import sys
import traceback
from enum import IntEnum

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, UserInputError, NoPrivateMessage, CheckFailure, DisabledCommand, \
    CommandInvokeError, CommandOnCooldown, CommandError, MissingRequiredArgument, TooManyArguments, BadArgument

logging.basicConfig(format="[%(asctime)s] [%(levelname)-8s] - %(message)s", level=logging.INFO)


class DeleteDelays(IntEnum):
    ten_mins = 600
    five_mins = 300
    one_min = 60
    default = one_min


class BotWrapper(commands.Bot):
    def __init__(self, *args, **options):
        super().__init__(*args, **options)

    def say_delete(self, *args, delete_after=DeleteDelays.default, **kwargs):
        return super().say(*args, delete_after=delete_after, **kwargs)


bot = BotWrapper(
    command_prefix="?",
    description="Bot that does cool stuff.",
    help_attrs=dict(hidden=True)
)


def load_config():
    with open('config.json') as f:
        return json.load(f)


# noinspection PyUnresolvedReferences
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, CommandNotFound):
        message = await bot.send_message(
            ctx.message.channel,
            "CommandNotFound:\nThis command does not exist.")
    elif isinstance(error, UserInputError):
        message = await bot.send_message(
            ctx.message.channel,
            "UserInputError")
    elif isinstance(error, NoPrivateMessage):
        message = await bot.send_message(
            ctx.message.channel,
            "NoPrivateMessage:\nThis command cannot be used through private messages.")
    elif isinstance(error, CheckFailure):
        message = await bot.send_message(
            ctx.message.channel,
            "CheckFailure:\nOne of the requirements for this command was not met.")
    elif isinstance(error, DisabledCommand):
        message = await bot.send_message(
            ctx.message.channel,
            "DisabledCommand:\nThis command is not enabled.")
    elif isinstance(error, CommandInvokeError):
        message = await bot.send_message(
            ctx.message.channel,
            "CommandInvokeError:\nSomething went wrong while trying to execute your command.")
    elif isinstance(error, CommandOnCooldown):
        message = await bot.send_message(
            ctx.message.channel,
            "CommandOnCooldown:\nThis command is on cooldown.")
    elif isinstance(error, CommandError):
        message = await bot.send_message(
            ctx.message.channel,
            "CommandError:\nSomething went wrong while trying to execute your command.")
    elif isinstance(error, MissingRequiredArgument):
        message = await bot.send_message(
            ctx.message.channel,
            "MissingRequiredArgument:\nOne or more parameters required to execute this command are missing.")
    elif isinstance(error, TooManyArguments):
        message = await bot.send_message(
            ctx.message.channel,
            "TooManyArguments:\nToo many arguments were given to the command.")
    elif isinstance(error, BadArgument):
        message = await bot.send_message(
            ctx.message.channel,
            "BadArgument:\nInvalid argument.")
    else:
        message = await bot.send_message(
            ctx.message.channel,
            "Something went very, very wrong...")

    async def delayed_delete():
        await asyncio.sleep(DeleteDelays.default)
        await bot.delete_message(message)

    discord.compat.create_task(delayed_delete(), loop=bot.loop)

    print('Exception thrown while executing command {}'.format(ctx.command), file=sys.stderr)
    traceback.print_tb(error.original.__traceback__)
    print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)


if __name__ == '__main__':

    bot.config = load_config()

    extensions = [
        'cogs.core',
        'cogs.warcraftlogs',
        'cogs.rnjesus',
        # 'cogs.simulationcraft'
        'cogs.soundboard',
        'cogs.search'
    ]

    for extension in extensions:
        try:
            logging.info('Loading extension {}'.format(extension))
            bot.load_extension(extension)
        except Exception as e:
            logging.error('Failed to load extension {}\n{}: {}'.format(extension, type(e).__name__, e))
            # traceback.print_exc(e)

    bot.run(bot.config['discord']['discord_token'])
