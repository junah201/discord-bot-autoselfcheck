  
#-*- coding:utf-8 -*-

import discord
from discord.ext import commands, tasks
import time, datetime
import hcskr
import random
import json
import os, sys

bot = commands.Bot(command_prefix='?')
#KST = datetime.timezone(datetime.timedelta(hours=9))

start_minute=0

@tasks.loop(seconds=60)
async def auto_self_check():
    global start_minute
    print("{}무한루프가 돌아가는 중...".format(datetime.datetime.now()))
    if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == start_minute:
        with open("user_data.json", "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        
        start_minute=random.randrange(1,16)

        for i in user_data.keys():
            name = user_data[i]["name"]
            birth = user_data[i]["birth"]
            area = user_data[i]["area"]
            school_name = user_data[i]["school_name"]
            school_type = user_data[i]["school_type"]
            passward = user_data[i]["passward"]
            print(f"[{name}]님의 자가진단 준비중")
            data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
            await send_DM(data,i,start_minute,user_data) #i가 유저 id

auto_self_check.start()

@bot.event
async def on_ready():
    print("봇 실행 완료")
    now = datetime.datetime.now()
    user = await bot.fetch_user(523017072796499968)
    game = discord.Game("?명령어")
    await bot.change_presence(status=discord.Status.online, activity=game)
    embed = discord.Embed(title="봇 실행 완료", description=f"{now} 부로 봇이 실행되었습니다.", color=0x62c1cc)
    await user.send(embed=embed)
   
@bot.event
async def on_error(event, *args, **kwargs):
    user = await bot.fetch_user(523017072796499968)
    exc = sys.exc_info() #sys를 활용해서 에러를 확인합니다.
    await user.send(f"에러 발생 : {str(exc[0].__name__)} : {str(exc[1])}")

async def send_DM(data,user_id,start_minute,user_data):
    print("자가진단 실행 후 메시지 준비 중...")
    user = await bot.fetch_user(user_id)
    if user is not None:
        if data["code"]=="SUCCESS":
            now = datetime.datetime.now()
            embed = discord.Embed(title="자가 진단 완료", description="{} 부로 {} 님의 자가진단이 성공적으로 실시되었습니다.\n(API 출력메시지 : {})\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],data["message"]), color=0x62c1cc)
            await user.send(embed=embed)
            user = await bot.fetch_user(523017072796499968)
            await user.send("{}님의 자가진단 완료".format(user_data[user_id]["name"]))
        else:
            now = datetime.datetime.now()
            embed = discord.Embed(title="자가 진단 실패", description="{} 부로 {} 님의 자가진단이 실시되었습니다만.\n{}\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],data["message"]), color=0x62c1cc)
            await user.send(embed=embed)
            user = await bot.fetch_user(523017072796499968)
            await user.send("{}님의 자가진단 실패\n{}".format(user_data[user_id]["name"],data["message"]))
    else:
        user = await bot.fetch_user(523017072796499968)
        await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title="도움말", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]\n(예 : ?정보등록 홍길동 721027 서울시 길동고 고등학교 1234)\n(예 : ?정보등록 홍길동 050201 충청남도 길동중 중학교 2580)", inline=False)
    embed.add_field(name="?정보삭제", value="?정보삭제\n※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="?정보확인", value="?정보확인\n※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="기타",value="자동자가진단은 7시 00분에서 7시 16분 사이에 랜덤하게 작동하며,\n자동자가진단 DM 메시지를 통하여 그 다음날의 작동 시간을 알 수 있습니다.", inline=False)
    embed.add_field(name="정보",value="봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)")
    await ctx.send(embed=embed)

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title="도움말", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]\n(예 : ?정보등록 홍길동 721027 서울시 길동고 고등학교 1234)\n(예 : ?정보등록 홍길동 050201 충청남도 길동중 중학교 2580)", inline=False)
    embed.add_field(name="?정보삭제", value="?정보삭제\n※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="?정보확인", value="?정보확인\n※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="기타",value="자동자가진단은 7시 00분에서 7시 16분 사이에 랜덤하게 작동하며,\n자동자가진단 DM 메시지를 통하여 그 다음날의 작동 시간을 알 수 있습니다.", inline=False)
    embed.add_field(name="정보",value="봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)")
    await ctx.send(embed=embed)
    
@bot.command()
async def 서버목록(ctx):
    servers = bot.guilds
    embed = discord.Embed(title="서버목록", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    msg = ''
    for server in servers:
        msg+=f"{server}\n"
    embed.add_field(name=f"현재 {len(servers)}개의 서버에서 실행 중 입니다.",value=f"{msg}")
    embed.add_field(name="정보",value="봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)")
    await ctx.send(embed=embed)
    
@bot.command()
async def 정보등록(ctx,name=None,birth=None,area=None,school_name=None,school_type=None,passward=None):
    if name!=None and birth!=None and area!=None and school_name!=None and school_type!=None and passward!=None:
        with open("user_data.json", "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        user_data[str(ctx.author.id)] = {
            "uesr_id":str(ctx.author.id),
            "name":name,
            "birth":birth,
            "area":area,
            "school_name":school_name,
            "school_type":school_type,
            "passward":passward
            }
        print(user_data[str(ctx.author.id)])
        with open("user_data.json", "w",encoding='UTF-8') as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)
        now = datetime.datetime.now()
        embed = discord.Embed(title="정보 등록 완료", description="{} 부로 {} 님의 정보 등록이 완료되었습니다.\n구체적인 등록 정보는 개인DM을 확인해주세요.\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)".format(now.strftime('%Y-%m-%d %H:%M:%S'),ctx.author),color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(523017072796499968)
        embed = discord.Embed(title="정보 등록 완료", description=f"[{ctx.author}]님이 [{ctx.guild}] 서버 - [{ctx.channel}] 채널에서 정보등록을 완료하셨습니다.\n입력값 : [{ctx.message.content}]\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)", color=0x62c1cc)
        await user.send(embed = embed)
        user = await bot.fetch_user(ctx.author.id)
        if user is not None:
            embed = discord.Embed(title="정보 등록 완료[보안메시지]", description="{} 부로 {} 님의 정보 등록이 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2]), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 등록 실패", description="모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n형식  :  ?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)", color=0x62c1cc)
        await ctx.send(embed = embed)
        user = await bot.fetch_user(523017072796499968)
        embed = discord.Embed(title="정보 등록 실패", description=f"[{ctx.author}]님이 [{ctx.guild}] 서버 - [{ctx.channel}] 채널에서 정보등록을 실패하셨습니다.\n입력값 : [{ctx.message.content}]\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)", color=0x62c1cc)
        await user.send(embed = embed)
        
@bot.command()
async def 정보삭제(ctx):
    with open("user_data.json", "r",encoding='UTF-8') as json_file:
        user_data=json.load(json_file)
    print(type(ctx.author.id))

    if user_data.get(str(ctx.author.id)):
        data = user_data.pop(str(ctx.author.id))
        
        with open("user_data.json", "w",encoding='UTF-8') as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)

        now = datetime.datetime.now()
        embed = discord.Embed(title="정보 삭제 완료", description="{} 부로 {} 님의 정보 삭제가 완료되었습니다.\n구체적인 삭제 정보는 개인DM을 확인해주세요.\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED)".format(now.strftime('%Y-%m-%d %H:%M:%S'),data["name"]), color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="정보 삭제 완료[보안메시지]", description="{} 부로 {} 님의 정보 삭제가 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)".format(now.strftime('%Y-%m-%d %H:%M:%S'),data["name"],data["name"],data["birth"],data["area"],data["school_name"],data["school_type"],data["passward"][:2]), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")

@bot.command()
async def 정보확인(ctx):
    with open("user_data.json", "r",encoding='UTF-8') as json_file:
        user_data=json.load(json_file)
    if user_data.get(str(ctx.author.id)):
        embed = discord.Embed(title="정보 확인", description="개인DM으로 정보를 보냈습니다.\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)", color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="정보 확인[보안메시지]", description="이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n정보수정을 원하신다면 ?정보등록으로 새로 등록해주시기 바랍니다.\n이미 등록된 데이터가 있어도 새로 등록한 데이터를 기준으로 작동합니다.\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)".format(user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2]), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 확인 실패",description="디스코드 아이디에 해당하는 데이터가 없습니다. 관리자에게 문의 부탁드립니다.\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)", color=0x62c1cc)
        await ctx.send(embed=embed)
        
@bot.command()
async def 관리자정보확인(ctx):
    if str(ctx.author.id) == '523017072796499968':
        with open("user_data.json", "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        embed = discord.Embed(title="관리자 정보 확인", description="개인DM으로 정보를 보냈습니다.\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)", color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="관리자 정보 확인[보안메시지]", description="{}".format(str(user_data)), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("비 관리자는 해당 명령어를 사용할 수 없습니다.")


@bot.command()
async def 관리자전체자가진단(ctx):
    if str(ctx.author.id) == '523017072796499968':
        with open("user_data.json", "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        start_minute=random.randrange(1,16)
        for i in user_data.keys():
            name = user_data[i]["name"]
            birth = user_data[i]["birth"]
            area = user_data[i]["area"]
            school_name = user_data[i]["school_name"]
            school_type = user_data[i]["school_type"]
            passward = user_data[i]["passward"]
            print(f"[{name}]님의 자가진단 준비중")
            data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
            await send_DM(data,i,start_minute,user_data)
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("비 관리자가 해당 명령어를 사용할 수 없습니다.")
   

token = os.environ["BOT_TOKEN"]
bot.run(token) 

