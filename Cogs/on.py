import nextcord as discord
from nextcord import embeds
from nextcord.ext import commands

import os,datetime,json,sys
import koreanbots

from variable import *
from channels.log_channels import *
from embed.help_embed import *

import other

class on(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):  
        print(f"{self.bot.user} 실행 완료")
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 ")
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        embed = discord.Embed(title="봇 실행 완료", description=f"[{datetime.datetime.now()}] 에 [{host_name}] 에서 봇이 실행되었습니다.", color=0x62c1cc)
        await other.send_log(self.bot,log_bot_start_channel,f"`[{datetime.datetime.now()}] [{host_name}] 에서 봇이 실행되었습니다.`")
        await other.user_data_backup(self.bot)

    @commands.Cog.listener()
    async def on_error(self,event, *args, **kwargs):
        exc = sys.exc_info() #sys를 활용해서 에러를 확인합니다.
        user = await self.bot.fetch_user(int(ADMIN_ID))
        today = datetime.datetime.today().strftime("%Y_%m_%d")
        now = datetime.datetime.now()
        file = "./logs/error/" + today + '.txt'

        if os.path.isfile(file):
            f = open(file, 'a', encoding='utf-8')
            f.write(f'\n[ {now.hour}:{now.minute}:{now.second} ] {event} : {str(exc[0].__name__)} : {str(exc[1])}')
            f.close()
        else:
            f = open(file, 'w', encoding='utf-8')
            f.write(f'[ {now.hour}:{now.minute}:{now.second} ] {event} : {str(exc[0].__name__)} : {str(exc[1])}')
            f.close()


        await user.send(f"에러 발생 : {event} : {str(exc[0].__name__)} : {str(exc[1])}")

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        kb = koreanbots.Koreanbots(self.bot, KOR_TOKEN, run_task=True)
        print(f"서버 갱신 완료 : {kb}")
        await other.send_log(self.bot,log_server_join,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] `{guild.member_count-1}명`이 있는 [{guild}] 서버에 자가진단 봇이 추가되었습니다.")
        try:
            channels = guild.channels
            global help_embed
            system_channel = guild.system_channel.id
            if system_channel != None:
                channel = self.bot.get_channel(int(system_channel))
                await channel.send(embed = help_embed)
        except:
            pass
        #해당 리스트에 있는 단어가 채널이름에 있을 경우 도움말 표시
        try:
            for i in channels:
                if i.id != system_channel and str(i.type) == "text":
                    if i.name in ["채팅","챗","수다","chat","Chat"]:
                        channel = self.bot.get_channel(int(i.id))
                        await channel.send(embed = help_embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        await other.send_log(self.bot,log_server_remove,f"`[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {guild.member_count}명이 있는 [{guild}] 서버에 자가진단 봇이 삭제되었습니다.`")

    @commands.Cog.listener()
    async def on_command(self,ctx):
        today = datetime.datetime.today().strftime("%Y_%m_%d")
        now = datetime.datetime.now()
        file = "./logs/command/" + today + '.txt'
        if isinstance(ctx.channel, discord.abc.PrivateChannel) != True:
            if os.path.isfile(file):
                f = open(file, 'a', encoding='utf-8')
                f.write(f'\n[ {now.hour}:{now.minute}:{now.second} ] {ctx.author}님이 {ctx.guild}에서 {ctx.command} 명령어를 사용했습니다.')
                f.close()
            else:
                f = open(file, 'w', encoding='utf-8')
                f.write(f'[ {now.hour}:{now.minute}:{now.second} ] {ctx.author}님이 {ctx.guild}에서 {ctx.command} 명령어를 사용했습니다.')
                f.close()
        else:
            if os.path.isfile(file):
                f = open(file, 'a', encoding='utf-8')
                f.write(f'\n[ {now.hour}:{now.minute}:{now.second} ] {ctx.author}님이 DM에서 {ctx.command} 명령어를 사용했습니다.')
                f.close()
            else:
                f = open(file, 'w', encoding='utf-8')
                f.write(f'[ {now.hour}:{now.minute}:{now.second} ] {ctx.author}님이 DM에서 {ctx.command} 명령어를 사용했습니다.')
                f.close()

def setup(bot):
    bot.add_cog(on(bot))