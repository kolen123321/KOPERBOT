import discord
from discord.ext import commands

from api import KoperApi
from config import Config

class Verify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = KoperApi()
        self.config = Config().data
        self.added = []

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.message_id == self.config['verify']['message_id']:
            if reaction.emoji.name == self.config['verify']['reaction']:
                await reaction.member.send("Привет, я бот регистрации в системе Koper Connect для того что бы зарегестрироваться придумай пароль и отправь его мне")
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author.bot:
            if type(ctx.channel) == discord.DMChannel:
                guild_id = self.config['guild_id']
                guild = discord.utils.get(self.bot.guilds, id=guild_id)
                member = discord.utils.get(guild.members, id=ctx.author.id)
                username = member.display_name.replace("📍", "").replace(" ", "").replace("🔑", "")
                code = self.api.connect.create_code(username)['code']
                register = self.api.connect.register(code, ctx.content)
                if register['success']:
                    await ctx.author.send("Вы успешно зарегестрировались, войти вы можете на сайте: http://lavomerka.ml/login/")
                else:
                    if register['message'] == 'Данное имя пользователя уже занято':
                        await ctx.author.send("Вы уже зарегестрировались")
                    else:
                        await ctx.author.send(f"{register['message']}, попробуйте позже")


def setup(bot):
    bot.add_cog(Verify(bot))