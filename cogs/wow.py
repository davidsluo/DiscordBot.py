import logging

import requests
from discord.ext import commands

battle_net_api = {
    "US": "https://us.api.battle.net/",
    "EU": "https://eu.api.battle.net/",
    "KR": "https://kr.api.battle.net/",
    "TW": "https://tw.api.battle.net/",
    "CN": "https://api.battlenet.com.cn/",
    "SEA": "https://sea.api.battle.net/",
}

wow_page_template = "http://us.battle.net/wow/en/character/{}/{}/advanced"

character_info_pattern = "{}wow/character/{}/{}?fields=items,guild,talents,progression&locale=en_US&apikey={}"
race_info_pattern = "{}wow/data/character/races?locale=en_US&apikey={}"
class_info_pattern = "{}wow/data/talents?locale=en_US&apikey={}"

response_pattern = "{}-{} is an iLevel {} {} {} in the guild {}.\n{}"


# TODO: simulate dps? make sure response from blizzard api is code 200
class WoWSearch:
    def __init__(self, bot):

        self.bot = bot
        self.battle_net_api_key = bot.config['battle_net_api_key']

        self.__load_races()
        self.__load_classes()

    def __load_races(self):
        request_url = race_info_pattern.format(battle_net_api["US"], self.battle_net_api_key)

        r = requests.get(request_url)

        response = r.json()

        self.races = {}

        for i in response['races']:
            self.races[i['id']] = i['name']

    def __load_classes(self):
        request_url = class_info_pattern.format(battle_net_api["US"], self.battle_net_api_key)

        r = requests.get(request_url)

        response = r.json()

        self.classes = {}

        for i in response:
            self.classes[int(i)] = {
                "class": response[i]["class"].title(),
                "specs": [j["name"] for j in response[i]["specs"]]
            }

    def __get_character_info(self, character: str, realm: str):
        request_url = character_info_pattern.format(battle_net_api["US"], realm, character, self.battle_net_api_key)

        r = requests.get(request_url)

        response = r.json()

        if r.status_code != 200:
            logging.error(
                "Invalid status code while getting character info: " + str(r.status_code) + "\n" + request_url)
            return r.status_code, response['reason']
        else:
            character_info = {
                'name': response['name'],
                'realm': response['realm'],
                'class': self.classes[response['class']]['class'],
                'spec': response['talents'][0]['spec']['name'],
                'ilvl': response['items']['averageItemLevelEquipped'],
                'guild': response['guild']['name'],
                'progression': response['progression']['raids']
            }

            return r.status_code, character_info

    def __get_guild_info(self, guild: str, realm: str):
        pass
        # TODO: this

    @commands.group(
        name="plookup",
        description="Get a character's iLevel, class, etc. Character and realm names are case sensitive",
        brief="Get WoW character info",
        aliases=["playerlookup"],
        pass_context=True
    )
    async def player_lookup(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Invalid subcommand: " + ctx.subcommand_passed)

    @player_lookup.command(name="info")
    async def get_info(self, player: str):
        logging.info("Getting character info for " + player + "...")

        await self.bot.say("Finding character " + player + "...")

        region = "US"

        if region in battle_net_api.keys():
            character = player.split('-', 1)

            if len(character) < 2:
                await self.bot.say(
                    "Invalid syntax. Type the character and realm name exactly as it appears in game.\n"
                    "Ex: PixelToast-Zul'jin.")
            else:

                name = character[0]
                realm = character[1]

                status_code, info = self.__get_character_info(name, realm)

                if status_code == 200:
                    message = response_pattern.format(
                        info['name'],
                        info['realm'],
                        info['ilvl'],
                        info['spec'],
                        info['class'],
                        info['guild'],
                        wow_page_template.format(info['realm'].replace("'", "").lower(), info['name'])
                    )

                    await self.bot.say(message)

                else:
                    await self.bot.say("Error code: " + str(status_code) + ". Reason: " + info)

    @player_lookup.command(name="progress")
    async def progression(self, player: str):
        await self.bot.say(player)


def setup(bot):
    bot.add_cog(WoWSearch(bot))
