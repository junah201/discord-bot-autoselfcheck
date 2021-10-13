import get_covid19_data
import nextcord as discord
from nextcord.ext import commands
import json, hcskr
import datetime

from variable import *
from embed.help_embed import *

import get_covid19_data
import hcskr

class selfcheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 자가진단(self,ctx):
        await ctx.send(f"수동자가진단은 `{PREFIX}진단참여`을 이용해주시기 바랍니다.")

    @commands.command()
    async def 진단참여(self,ctx):
        user_id = str(ctx.author.id)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        if user_id in user_data.keys():
            name = user_data[user_id]['name']
            birth = user_data[user_id]["birth"]
            area = user_data[user_id]["area"]
            school_name = user_data[user_id]["school_name"]
            school_type = user_data[user_id]["school_type"]
            passward = user_data[user_id]["passward"]
            print(f"수동진단참여 :[{name}]님의 자가진단 준비중")
            try:
                data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                err = False
            except:
                err = True

            if "Cannot connect to host hcs.eduro.go.kr:443 ssl:True" in data['message'] or err == True:
                print(data)
                print("err")
                i=0
                while True:
                    user = await self.bot.fetch_user(int(ADMIN_ID))
                    await user.send(f"무지성 트라이 {i+1}트 : {user_data[user_id]['name']}")
                    i+=1
                    try:
                        data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                    except:
                        pass
                    if "Cannot connect to host hcs.eduro.go.kr:443 ssl:True" not in data['message'] or i>5:
                        print(data)
                        break
            
            if data["code"]=="SUCCESS":
                print("수동 자가진단 성공")
                await ctx.send(f"[{data['regtime']}] 자가진단 완료!\n{data['message']}")
            else:
                print(f"수동 자가진단 실패 : {data}")
                await ctx.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 자가진단 실패!\n{data['message']}")
                await ctx.send(f"입력된 정보가 정상인데도 자가진단 실패가 뜬다면 재시도 하시거나 관리자(white201#0201)에게 문의 부탁드립니다.")
        else:
            await ctx.send(f"유저 데이터에 등록된 정보가 없습니다. `{PREFIX}정보등록`으로 등록해주십시오.")
            
    @commands.command()
    async def 자가진단실시(self,ctx):
        user = str(ctx.author.id)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        if user in user_data.keys():
            user_data[user]["possible"] = True
            with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            await ctx.send("자가진단이 내일부터 실시될 예정입니다.")
        else:
            await ctx.send("유저데이터에 해당 유저가 없습니다.")

    @commands.command()
    async def 자가진단중지(self,ctx):
        user = str(ctx.author.id)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        if user in user_data.keys():
            user_data[user]["possible"] = False
            with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            await ctx.send("자가진단이 내일부터 실시되지 않을 예정입니다.")
        else:
            await ctx.send("유저데이터에 해당 유저가 없습니다.")

def setup(bot):
    bot.add_cog(selfcheck(bot))