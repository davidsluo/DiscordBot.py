import requests
from discord.ext import commands


class Wikipedia:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="wikipedia",
        aliases=["wiki"],
        description="Search the English Wikipedia.",
        brief="Search Wikipedia."
    )
    async def wikipedia(self, *, query):
        search_payload = {
            "action": "opensearch",
            "format": "json",
            "search": query,
            "namespace": 0,
            "limit": 5,
            "redirects": "resolve"
        }
        r = requests.get("https://en.wikipedia.org/w/api.php", search_payload)

        if r.status_code == 200:
            results = r.json()

            print(r.url)

            if len(results[2]) >= 1:
                if ("{0} may refer to:".format(query).lower()) in (results[2][0].lower()):
                    message = "**{0}** may refer to:\n```-{1}```{2}" \
                        .format(query, '\n-'.join(results[1][1:]), results[2][0])
                    await self.bot.say(message)
                else:
                    message = '`{0}`\n{1}'.format(results[2][0], results[3][0])
                    await self.bot.say(message)
            else:
                await self.bot.say_delete(("Not results found for **{}**.".format(query)))
        else:
            await self.bot.say_delete("Error while searching Wikipedia.")


def setup(bot):
    bot.add_cog(Wikipedia(bot))
