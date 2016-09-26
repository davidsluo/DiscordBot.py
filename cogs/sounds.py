from discord.ext import commands

class Sounds:
    def __init__(self, bot):
        self.bot = bot

    # TODO: figure out how to programmatically add these.
    # TODO: figure out if I can include the mp3 files

    @commands.command(
        name="notprepared",
        # alias=["notprepared"],
        description="YOU ARE NOT PREPARED",
        brief="YOU ARE NOT PREPARED",
        pass_context=True,
        no_pm=True
    )
    async def not_prepared(self, ctx):
        v_channel = ctx.message.author.voice

        if v_channel:
            client = await self.bot.join_voice_channel(v_channel.voice_channel)

            player = client.create_ffmpeg_player('sounds/not_prepared.mp3')

            player.volume = .40
            player.start()

            player.join()
            await client.disconnect()

    @commands.command(
        name="prepared",
        # alias=["prepared"],
        description="YOU ARE NOW PREPARED",
        brief="YOU ARE NOW PREPARED",
        pass_context=True,
        no_pm=True
    )
    async def prepared(self, ctx):
        v_channel = ctx.message.author.voice

        if v_channel:
            client = await self.bot.join_voice_channel(v_channel.voice_channel)

            player = client.create_ffmpeg_player('sounds/prepared.mp3')

            player.volume = .30
            player.start()

            player.join()
            await client.disconnect()

    @commands.command(
        name="setback",
        # alias=["setback"],
        description="TEMPEST KEEP WAS MERELY A SETBACK",
        brief="MERELY A SETBACK",
        pass_context=True,
        no_pm=True
    )
    async def setback(self, ctx):
        v_channel = ctx.message.author.voice

        if v_channel:
            client = await self.bot.join_voice_channel(v_channel.voice_channel)

            player = client.create_ffmpeg_player('sounds/setback.mp3')

            player.volume = .40
            player.start()

            player.join()
            await client.disconnect()


def setup(bot):
    bot.add_cog(Sounds(bot))
