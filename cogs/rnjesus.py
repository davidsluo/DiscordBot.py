import random

from discord.ext import commands


class RNJesus:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="rng",
        aliases=["rand", "random", "roll"],
        description="Do some random shit.",
        brief="Pray to RNJesus."
    )
    async def roll(self, ctx, max=100.0):
        await self.bot.send_typing(ctx.message.channel)

        if not isinstance(max, (int, float)):
            await self.bot.say("Range must be a number.")
        elif 1 <= max <= 1e250:
            rand = random.randint(1, max)

            await self.bot.say("@{} rolls {} (1-{})".format(ctx.message.author, rand, int(max)))
        else:
            await self.bot.say("Range must be between 1 and 1e250.")


def setup(bot):
    bot.add_cog(RNJesus(bot))
