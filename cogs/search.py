import re
import urllib

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


class Bing:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="bing",
        aliases=["b"],
        description="Search Bing.",
        brief="Search Bing."
    )
    async def search(self, *, query):
        search_payload = {"q": query, "count": 1, "responseFilter": "webPages"}
        search_header = {"Ocp-Apim-Subscription-Key": self.bot.config['api_keys']["bing"]}

        r = requests.get("https://api.cognitive.microsoft.com/bing/v5.0/search", params=search_payload,
                         headers=search_header)

        response = r.json()

        if r.status_code == 200:
            if response["webPages"]:
                results = response["webPages"]["value"]

                formatted_results = []

                for result in results:
                    match = re.search("(?<=(r=))(.*?)(?=(&p))", result['url'])

                    if match:
                        url = urllib.parse.unquote(match.group(0))
                        formatted_results.append("**{0}**\n{1}".format(result['name'], url))

                message = "Showing **{0}** results for **{1}**\n{2}.".format(
                    len(formatted_results),
                    query,
                    "\n".join(formatted_results)
                )

                await self.bot.say(message)

            else:
                await self.bot.say_delete("No results for {}.".format(query))
        elif r.status_code == 429:
            await self.bot.say_delete(response["error"]["message"])
        else:
            await self.bot.say_delete("Error while searching Bing.")


def setup(bot):
    bot.add_cog(Wikipedia(bot))
    bot.add_cog(Bing(bot))
