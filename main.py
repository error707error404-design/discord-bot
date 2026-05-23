import discord
from discord.ext import commands
import os
import json

# =========================
# 토큰
# =========================
TOKEN = os.getenv("TOKEN")

# =========================
# 디스코드 설정
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# 저장 파일
# =========================
DATA_FILE = "money.json"

# =========================
# 데이터 불러오기
# =========================
def load_data():

    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}

# =========================
# 데이터 저장
# =========================
def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

money = load_data()

# =========================
# 봇 실행
# =========================
@bot.event
async def on_ready():

    print(f"{bot.user} 실행됨!")

# =========================
# 핑
# =========================
@bot.command()
async def 핑(ctx):

    embed = discord.Embed(
        title="🏓 핑 테스트",
        description="퐁!",
        color=0x57F287
    )

    await ctx.send(embed=embed)

# =========================
# 도움말
# =========================
@bot.command()
async def 도움(ctx):

    embed = discord.Embed(
        title="📋 명령어 목록",
        description="""
`!핑`
→ 봇 테스트

`!도움`
→ 명령어 목록 보기

`!잔액`
→ 현재 잔액 확인

`!지급 @유저 금액`
→ 돈 지급

`!송금 @유저 금액`
→ 유저에게 송금

`!입금확인 이름 금액`
→ 입금 확인 요청
""",
        color=0x5865F2
    )

    embed.set_footer(text="Discord Economy Bot")

    await ctx.send(embed=embed)

# =========================
# 잔액
# =========================
@bot.command()
async def 잔액(ctx):

    user_id = str(ctx.author.id)

    if user_id not in money:
        money[user_id] = 0
        save_data(money)

    amount = money[user_id]

    embed = discord.Embed(
        title="💰 잔액 확인",
        description=f"{ctx.author.mention}님의 잔액은\n\n`{amount}원` 입니다.",
        color=0x57F287
    )

    await ctx.send(embed=embed)

# =========================
# 지급
# =========================
@bot.command()
async def 지급(ctx, user: discord.Member, amount: int):

    user_id = str(user.id)

    if user_id not in money:
        money[user_id] = 0

    money[user_id] += amount

    save_data(money)

    embed = discord.Embed(
        title="💸 지급 완료",
        description=f"{user.mention}에게 `{amount}원` 지급 완료!",
        color=0xFEE75C
    )

    await ctx.send(embed=embed)

# =========================
# 송금
# =========================
@bot.command()
async def 송금(ctx, user: discord.Member, amount: int):

    sender_id = str(ctx.author.id)
    receiver_id = str(user.id)

    if sender_id not in money:
        money[sender_id] = 0

    if receiver_id not in money:
        money[receiver_id] = 0

    if money[sender_id] < amount:

        embed = discord.Embed(
            title="❌ 오류",
            description="잔액이 부족합니다.",
            color=0xED4245
        )

        await ctx.send(embed=embed)
        return

    money[sender_id] -= amount
    money[receiver_id] += amount

    save_data(money)

    embed = discord.Embed(
        title="💸 송금 완료",
        description=(
            f"{ctx.author.mention} ➜ {user.mention}\n\n"
            f"`{amount}원` 송금 완료!"
        ),
        color=0x57F287
    )

    await ctx.send(embed=embed)

# =========================
# 입금 확인
# =========================
@bot.command()
async def 입금확인(ctx, 이름=None, 금액=None):

    if 이름 is None or 금액 is None:

        embed = discord.Embed(
            title="❌ 사용 방법",
            description="`!입금확인 이름 금액`",
            color=0xED4245
        )

        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="🏦 입금 확인 요청",
        description=f"""
👤 이름: `{이름}`
💰 금액: `{금액}원`

관리자가 확인 후 처리합니다.

⏰ 사정이 있을 경우 늦어질 수 있습니다.
🎁 3일 이상 지연 시 2500원 추가 지급됩니다.
""",
        color=0x5865F2
    )

    embed.set_footer(text="입금 확인 시스템")

    await ctx.send(embed=embed)

# =========================
# 봇 실행
# =========================
bot.run(TOKEN, reconnect=True)
