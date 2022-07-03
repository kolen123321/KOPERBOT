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
                embed.add_field(name="Koper Verify", value="Hello, I am a registration bot in the Koper Verify system, in order to register, come up with a password and send it to me.", inline=False)
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
                    embed.add_field(name="Koper Verify", value="You have successfully registered, now you can log in on the site: http://lavomerka.ml/login / or you can go to the bank: http://kooper.ml/", inline=False)
                    await ctx.author.send(embed=embed)
                else:
                    if register['message'] == 'This username is already occupied':
                        embed=discord.Embed(color=0x0be541)
                        embed.add_field(name="Koper Verify", value="Have you already registered", inline=False)
                        await ctx.author.send(embed=embed)
                    else:
                        await ctx.author.send(f"{register['message']}, try again later")


def setup(bot):
    bot.add_cog(Verify(bot))
