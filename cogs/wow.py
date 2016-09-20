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

# TODO: load this list from api
raids = [
    "Molten Core", "Blackwing Lair", "Ruins of Ahn'Qiraj", "Ahn'Qiraj Temple", "Karazhan", "Magtheridon's Lair",
    "Gruul's Lair", "Serpentshrine Cavern", "Tempest Keep", "The Battle for Mount Hyjal", "Black Temple", "The Sunwell",
    "Vault of Archavon", "Naxxramas", "The Obsidian Sanctum", "The Eye of Eternity", "Ulduar", "Onyxia's Lair",
    "Trial of the Crusader", "Icecrown Citadel", "The Ruby Sanctum", "Baradin Hold", "Blackwing Descent",
    "The Bastion of Twilight", "Throne of the Four Winds", "Firelands", "Dragon Soul", "Mogu'shan Vaults",
    "Heart of Fear", "Terrace of Endless Spring", "Throne of Thunder", "Siege of Orgrimmar", "Highmaul",
    "Blackrock Foundry", "Hellfire Citadel", "The Emerald Nightmare", "The Nighthold"
]

# TODO: simulate dps? make sure response from blizzard api is code 200
class WoWSearch:
    def __init__(self, bot):

        self.bot = bot
        self.battle_net_api_key = bot.config['battle_net_api_key']

        # self.__load_races()
        self.__load_classes()

    # is this method really necessary?
    @staticmethod
    def __api_request(url):

        # TODO: make this method accept fields as arguments and create the URL itself.
        r = requests.get(url)

        return r.status_code, r.json()

    def __load_races(self):
        request_url = race_info_pattern.format(battle_net_api["US"], self.battle_net_api_key)

        status, response = self.__api_request(request_url)

        if status == 200:
            self.races = {}

            for i in response['races']:
                self.races[i['id']] = i['name']

        else:
            raise Exception("Failed to load races from Blizzard API. Status code: " + status)

    def __load_classes(self):
        request_url = class_info_pattern.format(battle_net_api["US"], self.battle_net_api_key)

        status, response = self.__api_request(request_url)

        if status == 200:

            self.classes = {}

            for i in response:
                self.classes[int(i)] = {
                    "class": response[i]["class"].title(),
                    "specs": [j["name"] for j in response[i]["specs"]]
                }

        else:
            raise Exception("Failed to load classes from Blizzard API. Status code: " + status)

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
    # figure out how to make this call the info command if no subcommand is given.
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

                request_url = character_info_pattern.format(battle_net_api["US"], realm, name, self.battle_net_api_key)

                r = requests.get(request_url)

                status, response = self.__api_request(request_url)

                if r.status_code != 200:
                    logging.error(
                        "Invalid status code while getting character info: " + str(r.status_code) + "\n" + request_url)

                    await self.bot.say("Error code: " + str(status) + ". Reason: " + response['reason'])
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

                    message = response_pattern.format(
                        character_info['name'],
                        character_info['realm'],
                        character_info['ilvl'],
                        character_info['spec'],
                        character_info['class'],
                        character_info['guild'],
                        wow_page_template.format(
                            character_info['realm'].replace("'", "").lower(),
                            character_info['name']
                        )
                    )

                    await self.bot.say(message)

    @player_lookup.command(name="progress")
    async def progression(self, player: str, raid: str = "latest"):
        logging.info("Getting " + raid + " progression for " + player + "...")

        def search_for_raid(r: str):
            for rd in raids:
                if r.lower() in rd.lower():
                    return rd

            return None

        raid_title = search_for_raid(raid)
        if raid == "latest" or raid_title is not None:
            pass
            await self.bot.say("valid raid: " + raid_title)
            # TODO: the rest of this method
        else:
            logging.error("Invalid raid tier: " + raid)
            await self.bot.say("Raid not found: " + raid)


def setup(bot):
    bot.add_cog(WoWSearch(bot))
