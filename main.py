#-*- coding: UTF8-*-
#Thank you, Danny!
import nextcord as discord
from nextcord.ext import commands

import koreanbots,os

from variable import *

bot = commands.Bot(command_prefix=PREFIX)
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')
        '''
try:
    kb = koreanbots.Koreanbots(bot, KOR_TOKEN, run_task=True)
except:
    pass'''

bot.run(TOKEN)