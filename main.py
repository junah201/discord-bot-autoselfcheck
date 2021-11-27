#-*- coding: UTF8-*-
#Thank you, Danny!

import nextcord as discord
from nextcord.ext import commands
import json,koreanbots,os 
from variable import *

#bot 설정
with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
    user_data=json.load(json_file)
game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 ")
bot = commands.Bot(command_prefix=PREFIX,activit=game)

#Cogs 수집
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')

#한디리 업데이트
try:
    kb = koreanbots.Koreanbots(bot, KOR_TOKEN, run_task=True)
except:
    pass

#봇 실행
bot.run(TOKEN)