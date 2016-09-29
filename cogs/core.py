import discord
import requests
from discord.ext import commands


class Core:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="setname",
        hidden=True,
        pass_context=True
    )
    async def set_name(self, ctx, *, name):
        if ctx.message.author.id == self.bot.config['discord']['owner_client_id']:
            await self.bot.change_nickname(ctx.message.server.me, name)

            await self.bot.say_delete("Bot name set to {}.".format(name))
        else:
            await self.bot.say_delete("You are not the bot owner!")

    @commands.command(
        name="setavatar",
        hidden=True,
        pass_context=True
    )
    async def set_avatar(self, ctx, image_url):
        if ctx.message.author.id == str(self.bot.config['discord']['owner_client_id']):
            try:
                r = requests.get(image_url)

                await self.bot.edit_profile(avatar=r.content)
                await self.bot.say_delete("Bot avatar set.")
            except requests.exceptions.MissingSchema:
                await self.bot.say_delete("Invalid URL.")
            except discord.errors.InvalidArgument:
                await self.bot.say_delete("Not a valid avatar.")
        else:
            await self.bot.say_delete("You are not the bot owner!")

    @commands.command(
        name="setplaying",
        hidden=True,
        pass_context=True
    )
    async def set_playing(self, ctx, *, playing=None):
        if ctx.message.author.id == self.bot.config['discord']['owner_client_id']:
            await self.bot.change_status(game=discord.Game(name=playing))
            await self.bot.say_delete("Playing status set.")
        else:
            await self.bot.say_delete("You are not the self.bot owner!")

    @commands.command(
        name="getinvitelink",
        aliases=["invitelink", "invite", "link"],
        description="Get the link to invite this self.bot to your Discord server.",
        brief="Get the invite link for this self.bot."
    )
    async def get_invite_link(self):
        await self.bot.say("https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0".format(
            self.bot.config['discord']['bot_client_id']))

    @commands.command(
        name="clean",
        aliases=["purge"],
        description="Clear this bot's messages from the chat history.",
        brief="Clean the chat log.",
        pass_context=True
    )
    async def clean(self, ctx):
        # async def clean(self, ctx, clear_bot=True):
        def is_bot(message):
            return message.author == ctx.message.server.me

        # def is_author(message):
        #     return message.author == ctx.message.author
        #
        # if clear_bot:
        #     deleted = await self.bot.purge_from(ctx.message.channel, limit=1000, check=is_bot)
        # else:
        #     deleted = await self.bot.purge_from(ctx.message.channel, limit=1000, check=is_author)

        deleted = await self.bot.purge_from(ctx.message.channel, limit=1000, check=is_bot)

        await self.bot.say("Deleted {} message(s).".format(len(deleted)))


def setup(bot):
    bot.add_cog(Core(bot))
