import get_covid19_data
import discord
from discord.ext import commands
import json
import datetime
import os

from variable import *
from embed.help_embed import *

import get_covid19_data, get_school_data

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 시간(self,ctx):
        await ctx.send(f"{datetime.datetime.now().strftime('%Y%m%d')}")

    @commands.command()
    async def 코로나(self,ctx):
        covid19_data = await get_covid19_data.get_covid19_decide()
        msg = ""
        for area in ["합계","서울","부산","대구","인천","광주","대전","울산","세종","경기","강원","충북","충남","전북","전남","경북","경남","제주","검역"]:
            msg += f"\n> {area} : {covid19_data[area]}"
        embed = discord.Embed(title="코로나 확진자",description=f"{msg}{end_msg}", color=0x62c1cc)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def 확진자(self,ctx):
        covid19_data = await get_covid19_data.get_covid19_decide()
        msg = ""
        for area in ["합계","서울","부산","대구","인천","광주","대전","울산","세종","경기","강원","충북","충남","전북","전남","경북","경남","제주","검역"]:
            msg += f"\n> {area} : {covid19_data[area]}"
        embed = discord.Embed(title="코로나 확진자",description=f"{msg}{end_msg}", color=0x62c1cc)
        await ctx.send(embed=embed)

    @commands.command()
    async def 확찐자(self,ctx):
        await ctx.send("그건 바로 너! 다이어트 하세요!")

    @commands.command()
    async def 학사일정(self,ctx, day=None,user: discord.User=None):
        if day == None:
            day = str(datetime.datetime.now().strftime('%Y%m%d'))
        if user==None:
            user = str(ctx.author.id)
        else:
            user = str(user.id)

        if len(day) == 8 and day.isdigit():
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)

            if user in user_data:
                user_data_keys = user_data[user].keys()
                if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
                    user_data[user]["area_code"] = await get_school_data.get_area_code(user_data[user]["area"])
                    user_data[user]["school_code"] = await get_school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
                    with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                        json.dump(user_data,json_file,ensure_ascii = False, indent=4)
                schedule = await get_school_data.get_school_schedule(user_data[user]["school_code"],user_data[user]["area_code"],day)
                await ctx.send(f"일시 : `{day}`\n일정 : {schedule}")
            else:
                await ctx.send(f"해당 유저의 데이터가 없습니다. `{PREFIX}정보등록`으로 유저 데이터를 입력해주십시오.")
        else:
            await ctx.send(f"날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `{datetime.datetime.now().strftime('%Y%m%d')}`)")

    @commands.command()
    async def 시간표(self,ctx, day=None,user: discord.User=None):
        if day == None:
            day = str(datetime.datetime.now().strftime('%Y%m%d'))
        print(day)
        if user==None:
            user = str(ctx.author.id)
        else:
            user = str(user.id)

        if len(day) == 8 and day.isdigit():
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)

            if user in user_data:
                user_data_keys = user_data[user].keys()
                if "school_grade" not in user_data_keys and "school_class" not in user_data_keys:
                    await ctx.send(f"입력된 학년반 데이터가 없습니다. `{PREFIX}학년반정보입력` 으로 입력해주십시오.")
                else:
                    if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
                        user_data[user]["area_code"] = await get_school_data.get_area_code(user_data[user]["area"])
                        user_data[user]["school_code"] = await get_school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
                        with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                            json.dump(user_data,json_file,ensure_ascii = False, indent=4)

                    timetable = await get_school_data.get_school_timetable(user_data[user]["school_code"],user_data[user]["area_code"],day,user_data[user]["school_type"],user_data[user]["school_grade"],user_data[user]["school_class"])
                    print(f"time : {timetable}")
                    msg = ""
                    if timetable != None:
                        for i in range(len(timetable)):
                            msg += f"{i+1}교시 : {timetable[i]}\n"
                    else:
                        msg = "시간표 데이터가 없습니다."
                    embed = discord.Embed(title="시간표",description=f"일시 : `{day}`\n\n{msg}{end_msg}", color=0x62c1cc)
                    #\n학년 : `{user_data[user]["school_grade"]}` 반 : `{user_data[user]["school_class"]}
                    await ctx.send(embed= embed)
            else:
                await ctx.send(f"해당 유저의 데이터가 없습니다. `{PREFIX}정보등록`으로 유저 데이터를 입력해주십시오.")
        else:
            await ctx.send("날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `20210612`)")

    @commands.command()
    async def 급식(self,ctx,day=None,user: discord.User=None):
        if day == None:
            day = str(datetime.datetime.now().strftime('%Y%m%d'))
        if user==None:
            user = str(ctx.author.id)
        else:
            user = str(user.id)
        print(day)
        if len(day) == 8 and day.isdigit():
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)

            if user in user_data:
                user_data_keys = user_data[user].keys()
                if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
                    user_data[user]["area_code"] = await get_school_data.get_area_code(user_data[user]["area"])
                    user_data[user]["school_code"] = await get_school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
                    with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                        json.dump(user_data,json_file,ensure_ascii = False, indent=4)
                    
                cafeteria = await get_school_data.get_school_cafeteria(user_data[user]["school_code"],user_data[user]["area_code"],day)
                print(f"cafeteria : {cafeteria}")
                if cafeteria != None:
                    embed = discord.Embed(title="급식 정보", description=f"일시 : `{day}`", color=0x62c1cc)
                    msg = ""
                    for i in cafeteria:
                        msg += f"{i}\n"

                    embed.add_field(name="급식",value=f">>> {msg}", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(f"`{day}`의 급식 정보가 없습니다.")   
            else:
                await ctx.send(f"해당 유저의 데이터가 없습니다. `{PREFIX}정보등록`으로 유저 데이터를 입력해주십시오.")
        else:
            await ctx.send("날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `20210612`)")


    @commands.command()
    async def 내일급식(self,ctx,user:discord.User=None):
        day=datetime.datetime.now() + datetime.timedelta(days=1)
        day = day.strftime('%Y%m%d')
        if user==None:
            user = str(ctx.author.id)
        else:
            user = str(user.id)
        print(day)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)

        if user not in user_data:
            await ctx.send(f"해당 유저의 데이터가 없습니다. `{PREFIX}정보등록`으로 유저 데이터를 입력해주십시오.")
            return

        user_data_keys = user_data[user].keys()

        if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
            user_data[user]["area_code"] = await get_school_data.get_area_code(user_data[user]["area"])
            user_data[user]["school_code"] = await get_school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
            with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            
        cafeteria = await get_school_data.get_school_cafeteria(user_data[user]["school_code"],user_data[user]["area_code"],day)

        if cafeteria == None:
            await ctx.send(f"`{day}`의 급식 정보가 없습니다.")
            return

        embed = discord.Embed(title="급식 정보", description=f"일시 : `{day}`", color=0x62c1cc)
        msg = ""
        for i in cafeteria:
            msg += f"{i}\n"

        embed.add_field(name="급식",value=f">>> {msg}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def 어제급식(self,ctx,user:discord.User=None): 
        day=datetime.datetime.now() - datetime.timedelta(days=1)
        day = day.strftime('%Y%m%d')
        if user==None:
            user = str(ctx.author.id)
        else:
            user = str(user.id)
        print(day)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)

        if user not in user_data:
            await ctx.send(f"해당 유저의 데이터가 없습니다. `{PREFIX}정보등록`으로 유저 데이터를 입력해주십시오.")
            return

        user_data_keys = user_data[user].keys()
        if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
            user_data[user]["area_code"] = await get_school_data.get_area_code(user_data[user]["area"])
            user_data[user]["school_code"] = await get_school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
            with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
                
        cafeteria = await get_school_data.get_school_cafeteria(user_data[user]["school_code"],user_data[user]["area_code"],day)

        if cafeteria != None:
            embed = discord.Embed(title="급식 정보", description=f"일시 : `{day}`", color=0x62c1cc)
            msg = ""
            for i in cafeteria:
                msg += f"{i}\n"

            embed.add_field(name="급식",value=f">>> {msg}", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"`{day}`의 급식 정보가 없습니다.")

def setup(bot):
    bot.add_cog(info(bot))