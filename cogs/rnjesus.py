import random

from discord.ext import commands


class RNJesus:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True,
        name="roll",
        aliases=["rand", "random", "rng"],
        description="Do some random shit.",
        brief="Pray to RNJesus."
    )
    async def roll(self, ctx, max=100.0):
        await self.bot.send_typing(ctx.message.channel)

        if not isinstance(max, (int, float)):
            await self.bot.say_delete("Range must be a number.")
        elif 1 <= max <= 1e250:
            rand = random.randint(1, max)

            await self.bot.say("{} rolls {} (1-{})".format(ctx.message.author.mention, rand, int(max)),
                               delete_after=None)
        else:
            await self.bot.say_delete("Range must be between 1 and 1e250.")

    @commands.command(
        name="decide",
        description="Decide between two or more choices.",
        brief="Let RNJesus take the wheel."
    )
    async def decide(self, choice1, choice2, *other_choices):
        choices = [choice1, choice2]

        for choice in other_choices:
            choices.append(choice)

        decision = random.choice(choices)

        await self.bot.say("The decision is: `{}`.".format(decision))

    @commands.command(
        name="flip",
        description="Flip a coin.",
        brief="Flip a coin."
    )
    async def flip(self):
        result = random.choice(("heads", "tails"))

        await self.bot.say("Flipped a coin. It landed `{}`.".format(result))


def setup(bot):
    bot.add_cog(RNJesus(bot))
