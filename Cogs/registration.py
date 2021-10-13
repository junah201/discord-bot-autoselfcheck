import nextcord as discord
from nextcord.ext import commands

from variable import *
import datetime,json

from embed.help_embed import *
from channels.log_channels import *

import get_school_data,other

class registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 정보등록(self,ctx,name=None,birth=None,area=None,school_name=None,school_type=None,passward=None):
        #서버에서 정보등록 명령어를 사용하였을 경우
        if str(ctx.guild) != "None":
            await ctx.send("개인정보 보호를 위해 봇과 개인메시지로 정보등록을 해주시기 바랍니다.")
            return

        #입력되지 않은 요소가 있을 경우
        if name==None or birth==None or area==None or school_name==None or school_type==None or passward==None:
            embed = discord.Embed(title="정보 등록 실패", description=f"모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n> 형식  :  `{PREFIX}정보등록 이름 생년월일 지역 학교이름 학교타입 비밀번호`\n> 예시 : `{PREFIX}정보등록 홍길동 721027 서울시 하나고 고등학교 1234`\n> 입력값 : `{PREFIX}정보등록 {name} {birth} {area} {school_name} {school_type} {passward}`{end_msg}", color=0x62c1cc)
            await ctx.send(embed = embed)
            embed = discord.Embed(title="정보 등록 실패", description=f"아이디 : [{ctx.author}]\n일시 : [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n 서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
            await other.send_embed_log(self.bot,log_add_failure_channel,embed)
            return

        #정상적이지 않은 지역값이 입력된 경우
        if area not in back_area_list:
            embed = discord.Embed(title="정보 등록 실패", description=f"지역은 아래 항목 중 하나로 입력해주셔야 합니다.\n> 형식  :  `{PREFIX}정보등록 이름 생년월일 지역 학교이름 학교타입 비밀번호`\n> 예시 : `{PREFIX}정보등록 홍길동 721027 서울시 하나고 고등학교 1234`\n> 입력값 : `{PREFIX}정보등록 {name} {birth} {area} {school_name} {school_type} {passward}`", color=0x62c1cc)
            embed.add_field(name="지역 리스트",value=f"```{area_list}```{end_msg}", inline=False)
            await ctx.send(embed = embed)
            embed = discord.Embed(title="정보 등록 실패", description=f"아이디 : [{ctx.author}]\n일시 : [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n 서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
            await other.send_embed_log(self.bot,log_add_failure_channel,embed)
            return

        #정상적이지 않은 비밀번호가 입력된 경우
        if len(passward) != 4 or passward.isdigit()==False:
            embed = discord.Embed(title="정보 등록 실패", description=f"비밀번호는 숫자 4글자의 형태로 입력해주셔야 합니다. (비밀번호 입력값 `{passward}`)\n> 형식  :  `{PREFIX}정보등록 이름 생년월일 지역 학교이름 학교타입 비밀번호`\n> 예시 : `{PREFIX}정보등록 홍길동 721027 서울시 하나고 고등학교 1234`\n> 입력값 : `{PREFIX}정보등록 {name} {birth} {area} {school_name} {school_type} {passward}`{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)
            embed = discord.Embed(title="정보 등록 실패", description=f"아이디 : [{ctx.author}]\n일시 : [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n 서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
            await other.send_embed_log(self.bot,log_add_failure_channel,embed)
            return

        #정상적이지 않은 생년월일이 입력된 경우
        if len(birth)!=6 or birth.isdigit() == False:
            embed = discord.Embed(title="정보 등록 실패", description=f"생년월일는 숫자 6글자의 형태로 입력해주셔야 합니다. (생년월일 입력값 `{birth}`)\n> 형식  :  `{PREFIX}정보등록 이름 생년월일 지역 학교이름 학교타입 비밀번호`\n> 예시 : `{PREFIX}정보등록 홍길동 721027 서울시 하나고 고등학교 1234`\n> 입력값 : `{PREFIX}정보등록 {name} {birth} {area} {school_name} {school_type} {passward}`{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)
            embed = discord.Embed(title="정보 등록 실패", description=f"아이디 : [{ctx.author}]\n일시 : [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n 서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
            await other.send_embed_log(self.bot,log_add_failure_channel,embed)
            return

        #정상적이지 않은 학교타입이 입력된 경우
        if school_type not in back_school_type_list:
            embed = discord.Embed(title="정보 등록 실패", description=f"학교 타입은 아래 항목 중 하나로 입력해주셔야 합니다. (학교타입 입력값 `{school_type}`)\n> 형식  :  `{PREFIX}정보등록 이름 생년월일 지역 학교이름 학교타입 비밀번호`\n> 예시 : `{PREFIX}정보등록 홍길동 721027 서울시 하나고 고등학교 1234`\n> 입력값 : `{PREFIX}정보등록 {name} {birth} {area} {school_name} {school_type} {passward}`", color=0x62c1cc)
            embed.add_field(name="학교 타입 리스트",value=f"```{school_type_list}```{end_msg}", inline=False)
            await ctx.send(embed=embed)
            embed = discord.Embed(title="정보 등록 실패", description=f"아이디 : [{ctx.author}]\n일시 : [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n 서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
            await other.send_embed_log(self.bot,log_add_failure_channel,embed)
            return

        #모든 입력 값이 정상일 경우
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)

        user_data[str(ctx.author.id)] = {
            "uesr_id" : str(ctx.author.id),
            "name" : name,
            "birth" : birth,
            "area" : area,
            "school_name" : school_name,
            "school_type" : school_type,
            "passward" : passward,
            "possible" : True,
            "failure" : 0,
            "schedule": None,
            "cafeteria": None,
            "timetable": None,
            "area_covid19_decide": None,
            "all_covid19_decide": None
            }

        user_data[str(ctx.author.id)]["area_code"] = await get_school_data.get_area_code(user_data[str(ctx.author.id)]["area"])
        user_data[str(ctx.author.id)]["school_code"] = await get_school_data.get_school_code(user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["area_code"])
        
        with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)

        embed = discord.Embed(title="정보 등록 완료", description=f"<@{ctx.author.id}> 님의 정보 등록이 완료되었습니다.\n`{PREFIX}진단참여`명령어를 사용하여 등록된 정보가 정상적으로 작동하는지 확인하시는 것을 추천드립니다.\n```이름 : {user_data[str(ctx.author.id)]['name']}\n생년월일 : {user_data[str(ctx.author.id)]['birth']}\n지역 : {user_data[str(ctx.author.id)]['area']}\n학교 이름 : {user_data[str(ctx.author.id)]['school_name']}\n학교 타입 : {user_data[str(ctx.author.id)]['school_type']}\n비밀번호 : {user_data[str(ctx.author.id)]['passward'][:2]}**```{end_msg}",color=0x62c1cc)
        await ctx.send(embed=embed)
        
        embed = discord.Embed(title="정보 등록 완료", description=f"이름 : [{ctx.author}]\n서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```", color=0x62c1cc)
        await other.send_embed_log(self.bot,log_add_success_channel,embed)

        #정보등록 후 상태 메시지 변경 (유저 수 갱신)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 ")
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    @commands.command()
    async def 정보삭제(self,ctx):
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)

        if user_data.get(str(ctx.author.id)) == None:
            embed = discord.Embed(title="정보 삭제 실패", description=f"<@{ctx.author.id}> 님의 정보 삭제에 실패하였습니다.\n해당 디스코드 아이디로 등록된 정보가 없습니다.\n계정 변경 시 `@white201#0201` 혹은 [서포트 서버](https://discord.gg/X5fBrVb8wC)로 문의부탁드립니다.{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)
            return

        data = user_data.pop(str(ctx.author.id))

        with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)
        if str(ctx.guild)!="None":
            embed = discord.Embed(title="정보 삭제 완료", description=f"{data['name']} 님의 정보 삭제를 완료하였습니다.\n구체적인 삭제 정보는 개인DM을 확인해주세요.{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)

        user = await self.bot.fetch_user(str(ctx.author.id))
        embed = discord.Embed(title="정보 삭제 완료[보안메시지]", description="부로 {} 님의 정보 삭제가 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data['name'],data['name'],data["birth"],data["area"],data["school_name"],data["school_type"],data["passward"][:2],end_msg), color=0x62c1cc)
        await user.send(embed=embed)

        await other.send_log(self.bot,log_add_remove,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {data['name']}님의 정보 삭제 완료!")
        #정보등록 후 상태 메시지 변경 (유저 수 갱신)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 ")
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    @commands.command()
    async def 정보확인(self,ctx):
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)

        if user_data.get(str(ctx.author.id))==None:
            embed = discord.Embed(title="정보 확인 실패",description=f"디스코드 아이디에 해당하는 데이터가 없습니다. 관리자에게 문의 부탁드립니다.{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)
            return

        if ctx.guild != None:
            embed = discord.Embed(title="정보 확인", description=f"개인DM으로 정보를 보냈습니다.{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)

        user = await self.bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="정보 확인[보안메시지]", description=f"```이름 : {user_data[str(ctx.author.id)]['name']}\n생년월일 : {user_data[str(ctx.author.id)]['birth']}\n지역 : {user_data[str(ctx.author.id)]['area']}\n학교 이름 : {user_data[str(ctx.author.id)]['school_name']}\n학교 타입 : {user_data[str(ctx.author.id)]['school_type']}\n비밀번호 : {user_data[str(ctx.author.id)]['passward'][:2]}**```\n※정보수정을 원하신다면 `{PREFIX}정보등록`으로 새로 등록해주시기 바랍니다.\n※이미 등록된 데이터가 있어도 새로 등록한 데이터를 기준으로 작동합니다.{end_msg}", color=0x62c1cc)
            await user.send(embed=embed)

    @commands.command()
    async def 학년반정보입력(self,ctx, school_grade:str=None, school_class:str=None):
        if school_grade == None or school_class == None:
            await ctx.send(f"`{PREFIX}학년반정보입력 [학년] [반]`의 형식으로 입력해주십시오. (예 : `{PREFIX}학년반정보입력 1 3`)")
        else:
            print(f"[{ctx.author.name}] grade : {school_grade}, class : {school_class}")
            if school_grade.isdigit() and school_class.isdigit() and int(school_grade) < 7 and int(school_class) < 40:
                with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                    user_data=json.load(json_file)

                user_data[str(ctx.author.id)]["school_grade"] = school_grade
                user_data[str(ctx.author.id)]["school_class"] = school_class

                with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
                    json.dump(user_data,json_file,ensure_ascii = False, indent=4)

                embed = discord.Embed(title="정보 입력 완료",description=f"학년 : `{school_grade}` \n반 : `{school_class}`{end_msg}", color=0x62c1cc)
                await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(registration(bot))
    