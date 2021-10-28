#-*- coding: UTF8-*-
#Thank you, Danny!
import nextcord as discord
from nextcord.ext import commands

import koreanbots,os

from variable import *

bot = commands.Bot(command_prefix=PREFIX)
game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 ")
await self.bot.change_presence(status=discord.Status.online, activity=game)

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')
        '''
try:
    kb = koreanbots.Koreanbots(bot, KOR_TOKEN, run_task=True)
except:
    pass'''

bot.run(TOKEN)