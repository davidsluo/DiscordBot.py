import logging

import requests
from discord.ext import commands

# guild/realm/region/key
request_pattern = "https://www.warcraftlogs.com:443/v1/reports/guild/{}/{}/{}?api_key={}"
warcraft_logs_url_pattern = "https://www.warcraftlogs.com/reports/{}"


class WarcraftLogs:
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.config["guild"]
        self.realm_slug = bot.config["realm_slug"]
        self.region = bot.config["region"]
        self.warcraft_logs_api_key = bot.config["warcraft_logs_api_key"]

    @commands.command(
        name="logs",
        aliases=["log"],
        description="Get the latest logs.",
        brief="Get the latest logs."
    )
    async def logs(self):
        logging.info("Getting last night's logs.")

        request_url = request_pattern.format(self.guild, self.realm_slug, self.region, self.warcraft_logs_api_key)

        r = requests.get(request_url)

        if r.status_code == 200:
            json = r.json()
            if len(json) > 0:
                await self.bot.say("Latest log:\n" + warcraft_logs_url_pattern.format(json[-1]['id']))
            else:
                await self.bot.say("No logs for guild configured.")
        else:
            await self.bot.say("Error while retrieving logs.")


def setup(bot):
    bot.add_cog(WarcraftLogs(bot))
