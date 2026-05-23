import discord
from discord.ext import commands
import os

TOKEN = os.getenv("MTUwNzM1MzAwNzc5MTE0OTEzNw.GWjAOY.YfIgLL1v0Hy850Lj2Xao0WIkE9PVJtsyLz30RU")

print("토큰 확인:", TOKEN)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("봇 실행 성공!")

@bot.command()
async def 핑(ctx):
    await ctx.send("퐁!")

bot.run(TOKEN)
