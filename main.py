import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "money.json"

# 데이터 불러오기
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# 데이터 저장
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

money = load_data()

@bot.event
async def on_ready():
    print(f"{bot.user} 실행됨!")

@bot.command()
async def 도움(ctx):
    embed = discord.Embed(
        title="📋 명령어 목록",
        description="""
!도움 → 명령어 보기
!잔액 → 내 잔액 확인
!송금 @유저 금액 → 돈 보내기
!입금확인 이름 금액 → 관리자 확인용
""",
        color=0x00ffcc
    )
    await ctx.send(embed=embed)

@bot.command()
async def 잔액(ctx):
    user = str(ctx.author.id)

    if user not in money:
        money[user] = 0
        save_data(money)

    embed = discord.Embed(
        title="💰 잔액 확인",
        description=f"{ctx.author.mention}님의 잔액은 `{money[user]}원` 입니다.",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command()
async def 송금(ctx, member: discord.Member, amount: int):
    sender = str(ctx.author.id)
    receiver = str(member.id)

    if sender not in money:
        money[sender] = 0

    if receiver not in money:
        money[receiver] = 0

    if money[sender] < amount:
        await ctx.send("❌ 잔액 부족")
        return

    money[sender] -= amount
    money[receiver] += amount

    save_data(money)

    embed = discord.Embed(
        title="💸 송금 완료",
        description=f"{ctx.author.mention} ➜ {member.mention}\n`{amount}원` 송금 완료",
        color=0xffcc00
    )
    await ctx.send(embed=embed)

@bot.command()
async def 입금확인(ctx, 이름, 금액):
    embed = discord.Embed(
        title="🏦 입금 확인 요청",
        description=f"""
이름: `{이름}`
금액: `{금액}원`

관리자가 확인 후 처리합니다.
사정이 있으면 늦을 수 있습니다.
3일 이상 지연 시 2500원 추가 지급.
""",
        color=0x3399ff
    )

    await ctx.send(embed=embed)

bot.run(TOKEN)
