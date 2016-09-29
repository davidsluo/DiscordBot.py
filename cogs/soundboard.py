import argparse
import json
from pathlib import Path

import requests
from discord import InvalidArgument
from discord.ext import commands
from requests import RequestException


class Soundboard:
    def __init__(self, bot):
        self.bot = bot
        # TODO: save this all to json or something later
        # TODO: verify that files exist
        self.sounds = {}

        self.load_sound_commands()

        for name, command_args in self.sounds.items():
            kwargs = command_args.copy()
            kwargs['name'] = name

            self.add_sound_command(**kwargs)

    def load_sound_commands(self):
        with open('sounds/sound_commands.json', 'r') as f:
            self.sounds = json.loads(f.read())

    def save_sound_commands(self):
        with open('sounds/sound_commands.json', 'w') as f:
            f.write(json.dumps(self.sounds, indent=4))

    def add_sound_command(self, **kwargs):
        def make_command(kwargs_):
            vol = kwargs_.pop('volume') if kwargs_.get('volume', None) else 0.4

            filename = kwargs_.pop('filename')

            if filename is None:
                raise ValueError("Filename cannot be None.")

            @commands.command(
                pass_context=True,
                no_pm=True,
                **kwargs_
            )
            # wtf why do i need self here i dont even
            async def sound_command(self, ctx, volume=vol):
                v_channel = ctx.message.author.voice.voice_channel
                if v_channel:
                    try:
                        client = await ctx.bot.join_voice_channel(v_channel)

                        player = client.create_ffmpeg_player('sounds/' + filename)

                        player.volume = volume
                        player.start()

                        player.join()
                        await client.disconnect()
                    except InvalidArgument:
                        await self.bot.say_delete("Channel must be a voice channel.")

            return sound_command

        command = make_command(kwargs)
        command.instance = self
        self.bot.add_command(command)

    def remove_sound_command(self, name):
        if name in self.sounds.keys():
            # self.sounds.pop(name)
            return self.bot.remove_command(name)
        else:
            return None

    @commands.group(
        pass_context=True,
        description="Add and remove sounds from the Soundboard.",
        brief="Edit the Soundboard."
    )
    async def soundboard(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say_delete(
                "Invalid subcommand. Use {}help soundboard for more info about this command.".format(
                    self.bot.command_prefix))

    @soundboard.command(
        name="add",
        description="Add a sound to the soundboard.",
        brief="Add a sound.",
        help="""
            -name (-n)
            Required
            The name of the command to register the new sound under. Must be one word. Cannot be the same as an already existing command.

            -link (-l)
            Required
            The link to the audio file to be played. If not specified, then this command must be called through a comment on a file upload to discord.

            -description (-desc, -d)
            Optional
            A description of what the audio file is.

            -brief (-b)
            Optional
            A shorter description to be shown on the help page for the Soundboard. If not specified, the first line of the description will be used.
            """,
        pass_context=True
    )
    async def add_sound(self, ctx, *args):
        await self.bot.send_typing(ctx.message.channel)

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("-name", "-n")
        parser.add_argument("-link", "-l")
        parser.add_argument("-description", "-desc", "-d")
        parser.add_argument("-brief", "-b")
        parsed_args = vars(parser.parse_args(args=args))

        if not parsed_args['link']:
            try:
                parsed_args['link'] = ctx.message.attachments[0]['url']
            except (IndexError, KeyError):
                await self.bot.say_delete("Link or upload of sound file required.")
                return

        if not parsed_args['name']:
            await self.bot.say_delete("Name of command required.")
            return

        try:
            r = requests.get(parsed_args['link'], timeout=3)

            filename = r.url.split('/')[-1]

            if r.status_code != 200:
                await self.bot.say_delete("Error while downloading file.")
                return

            # Checks if file already exists
            # Append _ to filename if necessary
            while True:
                if Path("sounds/" + filename).is_file():
                    components = filename.split('.')
                    extension = components.pop(-1)
                    name = '.'.join(components)

                    filename = '{0}_.{1}'.format(name, extension)
                else:
                    break
            # TODO: Verify that file is decodeable by ffmpeg?
            with open('sounds/' + filename, 'wb') as f:
                f.write(r.content)

            self.sounds[parsed_args['name']] = {
                'filename': filename,
                'brief': (parsed_args['brief'] if parsed_args['brief'] else ""),
                'description': (parsed_args['description'] if parsed_args['description'] else "")
            }

            self.save_sound_commands()

            self.add_sound_command(
                filename=filename,
                name=parsed_args['name'],
                brief=(parsed_args['brief'] if parsed_args['brief'] else ""),
                description=(parsed_args['description'] if parsed_args['description'] else "")
            )

            await self.bot.say(parsed_args['name'] + " successfully added.")
        except RequestException:
            await self.bot.say_delete("Failed to connect to url. Perhaps broken link?")

    @soundboard.command(
        name="remove",
        description="Remove a sound from the soundboard. Requires Manage Server permission to run.",
        brief="Remove a sound.",
        pass_context=True
    )
    async def remove_sound(self, ctx, name):
        if ctx.message.author.server_permissions.manage_server:
            if name in self.sounds.keys():
                self.remove_sound_command(name)
                self.sounds.pop(name)
                self.save_sound_commands()
                await self.bot.say(name + " removed.")
            else:
                await self.bot.say_delete("Sound does not exist.")
        else:
            # await self.bot.say("asdf")
            await self.bot.say_delete("You do not have permission!")


def setup(bot):
    bot.add_cog(Soundboard(bot))
