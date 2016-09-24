import datetime
import os
import subprocess
import time

from discord.ext import commands

from cogs.utils import wow
from cogs.utils.wow import validate_character

# 0 = region
# 1 = realm slug
# 2 = character name
# 3 = file_path
command_pattern = "cogs/simulator/simc armory={0},{1},{2} html={3}"

output_file_path = "static/{0}-{1}-{2}_{3}.html"

file_url_pattern = "http://{0}/{1}-{2}-{3}_{4}.html"


class SimulationCraft:
    def __init__(self, bot):
        self.bot = bot

        if not os.path.exists("static") or not os.path.isdir("static"):
            os.makedirs("static")

    @commands.command(
        name="sim",
        aliases=["simcraft", "simulate"],
        description="Run your character through a quick simulation.",
        brief="Simulation Craft",
        pass_context=True
    )
    # @commands.cooldown(
    #     rate=1,
    #     per=300,
    #     type=BucketType.user
    # )
    async def sim(self, ctx, character, region="US"):
        data = validate_character(character, self.bot.config['api_keys']['battle_net'], region=region)

        if data:
            name, realm, region = data
            await self.bot.send_typing(ctx.message.channel)

            timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H.%M.%S')
            output_file = output_file_path.format(region.lower(), wow.get_realm_slug(realm), name, timestamp)
            file_url = file_url_pattern.format(self.bot.config['simulationcraft']['host'], region.lower(), wow.get_realm_slug(realm), name, timestamp)
            command = command_pattern.format(region.lower(), wow.get_realm_slug(realm), name, output_file)

            subprocess.call(command, shell=True)

            if self.bot.config['simulationcraft']['webserver']:
                await self.bot.say(file_url)
            else:
                with open(output_file, 'rb') as f:
                    await self.bot.send_file(ctx.message.channel, f)
        else:
            await self.bot.say("Character name could not be verified.")


def setup(bot):
    bot.add_cog(SimulationCraft(bot))
