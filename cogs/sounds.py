from discord import InvalidArgument
from discord.ext import commands


class Sounds:
    def __init__(self, bot):
        self.bot = bot
        # TODO: save this all to json or something later
        # TODO: verify that files exist
        self.sounds = {
            "not_prepared.mp3": {
                "name": "notprepared",
                "description": "YOU ARE NOT PREPARED",
                "brief": "YOU ARE NOT PREPARED",
            },
            "prepared.mp3": {
                "name": "prepared",
                "description": "YOU ARE NOW PREPARED",
                "brief": "YOU ARE NOW PREPARED",
            },
            "setback.mp3": {
                "name": "setback",
                "description": "TEMPEST KEEP WAS MERELY A SETBACK",
                "brief": "MERELY A SETBACK",
            },
            "bork.mp3": {
                "name": "gabe",
                "aliases": ["bork"],
                "description": "Gabe the dog.",
                "brief": "Bork",
            }
        }

        self.update_sound_commands()

    def update_sound_commands(self):
        for filename, command_args in self.sounds.items():
            kwargs = command_args

            def make_command(filename_, kwargs_):
                vol = kwargs.pop('volume') if kwargs.get('volume', None) else 0.4

                @commands.command(
                    pass_context=True,
                    no_pm=True,
                    **kwargs_
                )
                async def sound_command(ctx, volume=vol):
                    await self.play_sound(ctx.message.author.voice.voice_channel, filename=filename_, volume=volume)

                return sound_command

            command = make_command(filename, kwargs)
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
