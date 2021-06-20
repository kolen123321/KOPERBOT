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
                embed=discord.Embed(color=0x0be541)
                embed.add_field(name="Koper Verify", value="Здравствуй, я бот регистрации в системе Koper Verify, для того что бы зарегистрироваться придумайте пароль и отправьте его мне.", inline=False)
                await reaction.member.send(embed=embed)
    
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
                    embed=discord.Embed(color=0x0be541)
                    embed.add_field(name="Koper Verify", value="Вы успешно зарегестрировались, теперь вы можете авторизоваться на сайте: http://lavomerka.ml/login/ или можете зайти в банк: http://kooper.ml/", inline=False)
                    await ctx.author.send(embed=embed)
                else:
                    if register['message'] == 'Данное имя пользователя уже занято':
                        embed=discord.Embed(color=0x0be541)
                        embed.add_field(name="Koper Verify", value="Вы уже зарегестрировались", inline=False)
                        await ctx.author.send(embed=embed)
                    else:
                        await ctx.author.send(f"{register['message']}, попробуйте позже")


def setup(bot):
    bot.add_cog(Verify(bot))