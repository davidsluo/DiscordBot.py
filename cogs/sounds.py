from discord.ext import commands


class Sounds:
    def __init__(self, bot):
        self.bot = bot

    # TODO: figure out how to programmatically add these.
    # TODO: figure out if I can include the mp3 files

    async def play_sound(self, ctx, filename, volume=0.4):
        v_channel = ctx.message.author.voice

        if v_channel:
            client = await self.bot.join_voice_channel(v_channel.voice_channel)

            player = client.create_ffmpeg_player('sounds/' + filename)

            player.volume = volume
            player.start()

            player.join()
            await client.disconnect()

    @commands.command(
        name="notprepared",
        # alias=["notprepared"],
        description="YOU ARE NOT PREPARED",
        brief="YOU ARE NOT PREPARED",
        pass_context=True,
        no_pm=True
    )
    async def not_prepared(self, ctx):
        await self.play_sound(ctx, 'not_prepared.mp3')

    @commands.command(
        name="prepared",
        # aliases=["prepared"],
        description="YOU ARE NOW PREPARED",
        brief="YOU ARE NOW PREPARED",
        pass_context=True,
        no_pm=True
    )
    async def prepared(self, ctx):
        await self.play_sound(ctx, 'prepared.mp3')

    @commands.command(
        name="setback",
        # aliases=["setback"],
        description="TEMPEST KEEP WAS MERELY A SETBACK",
        brief="MERELY A SETBACK",
        pass_context=True,
        no_pm=True
    )
    async def setback(self, ctx):
        await self.play_sound(ctx, 'setback.mp3')

    @commands.command(
        name="gabe",
        aliases=["bork"],
        description="Gabe the dog.",
        brief="Bork",
        pass_context=True,
        no_pm=True
    )
    async def bork(self, ctx):
        await self.play_sound(ctx, 'bork.mp3')


def setup(bot):
    bot.add_cog(Sounds(bot))
