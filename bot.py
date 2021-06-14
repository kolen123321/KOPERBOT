from discord.ext import commands
import discord, json
from config import Config

config = Config().data

intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)

bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help")

for cog in config['cogs']:
    bot.load_extension(f"cogs.{cog}")

bot.run(config['bot']['token'])