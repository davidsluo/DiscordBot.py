import logging

import requests
from discord.ext import commands

# guild/realm/region/key
request_pattern = "https://www.warcraftlogs.com:443/v1/reports/guild/{}/{}/{}?api_key={}"
warcraft_logs_url_pattern = "https://www.warcraftlogs.com/reports/{}#type={}"


class WarcraftLogs:
    def __init__(self, bot):
        self.bot = bot

        self.api_key = bot.config['api_keys']["warcraft_logs"]
        self.config = bot.config['wow_progress']

        self.guild = self.config["guild"]
        self.realm_slug = self.config["realm_slug"]
        self.region = self.config["region"]

        self.request_url = request_pattern.format(self.guild, self.realm_slug, self.region, self.api_key)

    async def _get_logs(self, section='summary'):
        logging.info("Getting the latest logs.")

        r = requests.get(self.request_url)

        if r.status_code == 200:
            json = r.json()
            if len(json) > 0:
                await self.bot.say(
                    "Latest {} log:\n".format(section) + warcraft_logs_url_pattern.format(json[-1]['id'], section))
            else:
                await self.bot.say("No logs for guild configured.")
        else:
            await self.bot.say("Error while retrieving logs: " + r.status_code + ".")

    @commands.group(
        pass_context=True,
        name="logs",
        aliases=["log"],
        description="Get info about logs.",
        brief="Logs"
    )
    async def logs(self, ctx):
        logging.info("Getting logs.")

        await self.bot.send_typing(ctx.message.channel)

        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.summary)

    @logs.command(
        name="summary",
        aliases=["s"],
        description="Get a summary of the latest logs.",
        brief="Log summary",
        invoke_without_command=True
    )
    async def summary(self):
        await self._get_logs()

    @logs.command(
        name="healing",
        aliases=["h"],
        description="Get latest healing logs.",
        brief="Healing logs"
    )
    async def healing(self):
        await self._get_logs('healing')

    @logs.command(
        name="damage",
        aliases=["d"],
        description="Get latest damage logs.",
        brief="Damage logs"
    )
    async def dps(self):
        await self._get_logs('damage-done')

    @logs.command(
        name="tank",
        aliases=["t"],
        description="Get latest tanking logs.",
        brief="Tanking logs"
    )
    async def tank(self):
        await self._get_logs('damage-taken')

    @logs.command(
        name="interrupts",
        aliases=["i"],
        description="Get latest interrupt logs.",
        brief="Interrupt logs"
    )
    async def interrupts(self):
        await self._get_logs('interrupts')

    @logs.command(
        name="dispels",
        aliases=["dis"],
        description="Get latest dispel logs.",
        brief="Dispel logs"
    )
    async def dispels(self):
        await self._get_logs('dispels')


def setup(bot):
    bot.add_cog(WarcraftLogs(bot))
