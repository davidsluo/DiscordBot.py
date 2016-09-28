import json

from discord import InvalidArgument
from discord.ext import commands


class Sounds:
    def __init__(self, bot):
        self.bot = bot
        # TODO: save this all to json or something later
        # TODO: verify that files exist
        self.sounds = {}

        self.load_sound_commands()

        for name, command_args in self.sounds.items():
            kwargs = command_args
            kwargs['name'] = name

            self.add_sound_command(kwargs)

    def load_sound_commands(self):
        with open('sounds/sound_commands.json', 'r') as f:
            self.sounds = json.loads(f.read())

    def save_sound_commands(self):
        with open('sounds/sound_commands.json', 'w') as f:
            f.write(json.dumps(self.sounds, indent=4))

    def add_sound_command(self, kwargs):
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
            async def sound_command(ctx, volume=vol):
                await self.play_sound(ctx.message.author.voice.voice_channel, filename=filename, volume=volume)

            return sound_command

        command = make_command(kwargs)
        command.instance = self
        self.bot.add_command(command)

    async def play_sound(self, v_channel, filename, volume=0.4):

        if v_channel:
            try:
                client = await self.bot.join_voice_channel(v_channel)

                player = client.create_ffmpeg_player('sounds/' + filename)

                player.volume = volume
                player.start()

                player.join()
                await client.disconnect()
            except InvalidArgument:
                await self.bot.say("Channel must be a voice channel.")


def setup(bot):
    bot.add_cog(Sounds(bot))
