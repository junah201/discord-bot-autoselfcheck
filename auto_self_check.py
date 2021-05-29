#-*- coding:utf-8 -*-

import discord
from discord.ext import commands, tasks
import time, datetime
import hcskr
import random
import json
import os, sys
import socket

host_name = socket.gethostbyaddr(socket.gethostname())[0]

bot = commands.Bot(command_prefix='?')
#KST = datetime.timezone(datetime.timedelta(hours=9))

start_minute=0
last_day = ""
#start_minute=datetime.datetime.now().minute

end_msg = "\n\n개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)"
#end_msg = "\n\n봇 : 자동자가진단#4767 | 개발자 : white#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)"
json_file_name = "user_data.json"

log_add_success_channel = "847490299638186054"
log_add_failure_channel = "847731541915467797"
log_bot_start_channel = "847732651912593439"
log_auto_self_check_failure_channel = "847793169683972146"
log_auto_self_check_success_channel = "847775280650518568"
log_auto_self_check_after_send_failure_channel ="847738621972578315"
log_json_backup_channel = "847830055916404766"


@tasks.loop(seconds=60)
async def auto_self_check():
    global start_minute
    print("[{}] 무한루프가 돌아가는 중...".format(datetime.datetime.now()))
    if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == start_minute and last_day != datetime.datetime.now().strftime('%Y-%m-%d'):
        with open(json_file_name, "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        
        start_minute=random.randrange(1,16)
        last_day = datetime.datetime.now().strftime('%Y-%m-%d')
        for user_id in user_data.keys():
            name = user_data[user_id]["name"]
            birth = user_data[user_id]["birth"]
            area = user_data[user_id]["area"]
            school_name = user_data[user_id]["school_name"]
            school_type = user_data[user_id]["school_type"]
            passward = user_data[user_id]["passward"]
            user_id = user_data[user_id]["uesr_id"]
            print(f"[{name}]님의 자가진단 준비중")
            data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
            await send_DM(data,user_id,start_minute,user_data)


@bot.event
async def on_ready():
    print("봇 실행 완료")
    now = datetime.datetime.now()
    game = discord.Game("?명령어 | 노동 ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    embed = discord.Embed(title="봇 실행 완료", description=f"[{now}] 에 [{host_name}] 에서 봇이 실행되었습니다.", color=0x62c1cc)
    await send_embed_log(log_bot_start_channel,embed)
    await user_data_backup()
    auto_self_check.start() #무한루프 실행
   
@bot.event
async def on_error(event, *args, **kwargs):
    user = await bot.fetch_user(523017072796499968)
    exc = sys.exc_info() #sys를 활용해서 에러를 확인합니다.
    await user.send(f"에러 발생 : {event} : {str(exc[0].__name__)} : {str(exc[1])}")

async def user_data_backup():
    with open(json_file_name, "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
    await send_log(log_json_backup_channel,"```"+str(user_data)+"```")


async def send_embed_log(channel,embed):
    channel = bot.get_channel(int(channel))
    await channel.send(embed=embed)

async def send_log(channel,msg):
    channel = bot.get_channel(int(channel))
    await channel.send(msg)

async def send_DM(data,user_id,start_minute,user_data):
    print("자가진단 실행 후 메시지 준비 중...")
    try:
        user = await bot.fetch_user(int(user_id))
        erorr = "not erorr"
    except:
        erorr = "erorr"
        pass

    if erorr != "erorr":
        if data["code"]=="SUCCESS":
            now = datetime.datetime.now()
            embed = discord.Embed(title="자가 진단 완료", description="[{}] 부로 {} 님의 자가진단이 성공적으로 실시되었습니다.\n(API 출력메시지 : {})\n다음 자동자가진단은 7시 {}분에 실시될 예정입니다.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],data["message"],start_minute,end_msg), color=0x62c1cc)
            await user.send(embed=embed)
            await send_log(log_auto_self_check_success_channel,"[{}]{}님의 자가진단 완료".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"]))
            print("자가진단 성공 후 메시지 발송 완료...")
        else:
            now = datetime.datetime.now()
            embed = discord.Embed(title="자가 진단 실패", description="[{}] 부로 {} 님의\n자가진단이 실시되었습니다만 자가진단에 실패하셨습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n\n{}{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],user_data[user_id]["name"],user_data[user_id]["birth"],user_data[user_id]["area"],user_data[user_id]["school_name"],user_data[user_id]["school_type"],user_data[user_id]["passward"][:2],data["message"],end_msg), color=0x62c1cc)
            await user.send(embed=embed)
            embed = discord.Embed(title="자가 진단 실패",description="[{}]\n<@{}>님의 자가진단 실패\n{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_id,data["message"]), color=0x62c1cc)
            await send_embed_log(log_auto_self_check_failure_channel,embed)
            print("자가진단 실패 후 메시지 발송 완료...")
    else:
        print("자가 진단 후 메시지 전송 실패...")
        now = datetime.datetime.now()
        embed = discord.Embed(title="자가 진단 후 메시지 전송 실패",description=f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 에 {user_data[user_id]['name']}(<@{user_id}>) 님의 자가진단이 실시되었습니다만 확인 메시지가 전송되지 않았습니다.\n자가진단결과 : {data['message']}", color=0x62c1cc)
        await send_embed_log(log_auto_self_check_after_send_failure_channel,embed)

@bot.command()
async def 도움말(ctx):
    embed = discord.Embed(title="도움말", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]```?정보등록 홍길동 721027 서울시 길동고 고등학교 1234``````?정보등록 홍길동 050201 충청남도 길동중 중학교 2580```", inline=False)
    embed.add_field(name="?정보삭제", value="?정보삭제\n※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="?정보확인", value="?정보확인\n※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="기타",value="자동자가진단은 7시 00분에서 7시 16분 사이에 랜덤하게 작동하며,\n자동자가진단 DM 메시지를 통하여 그 다음날의 작동 시간을 알 수 있습니다.", inline=False)
    embed.add_field(name="정보",value=end_msg)
    await ctx.send(embed=embed)

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title="도움말", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]```?정보등록 홍길동 721027 서울시 길동고 고등학교 1234``````?정보등록 홍길동 050201 충청남도 길동중 중학교 2580```", inline=False)
    embed.add_field(name="?정보삭제", value="?정보삭제\n※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="?정보확인", value="?정보확인\n※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="기타",value="자동자가진단은 7시 00분에서 7시 16분 사이에 랜덤하게 작동하며,\n자동자가진단 DM 메시지를 통하여 그 다음날의 작동 시간을 알 수 있습니다.", inline=False)
    embed.add_field(name="정보",value=end_msg)
    await ctx.send(embed=embed)
    
@bot.command()
async def 서버목록(ctx):
    servers = bot.guilds
    embed = discord.Embed(title="서버목록", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    msg = ''
    for server in servers:
        msg+=f"{server}\n"
    embed.add_field(name=f"현재 {len(servers)}개의 서버에서 실행 중 입니다.",value=f"{msg}", inline=False)
    await ctx.send(embed=embed)
    
@bot.command()
async def 정보등록(ctx,name=None,birth=None,area=None,school_name=None,school_type=None,passward=None):
    if name!=None and birth!=None and area!=None and school_name!=None and school_type!=None and passward!=None:
        with open(json_file_name, "r",encoding='UTF-8') as json_file:
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

        with open(json_file_name, "w",encoding='UTF-8') as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)
        now = datetime.datetime.now()
        embed = discord.Embed(title="정보 등록 완료", description="[{}] 에 {} 님의 정보 등록이 완료되었습니다.\n구체적인 등록 정보는 개인DM을 확인해주세요.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),ctx.author,end_msg),color=0x62c1cc)
        await ctx.send(embed=embed)
        
        embed = discord.Embed(title="정보 등록 완료", description=f"이름 : [{ctx.author}]\n서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```{end_msg}", color=0x62c1cc)
        #embed.add_field(name="입력값",value=f"```{ctx.message.content}```{end_msg}")
        await send_embed_log(log_add_success_channel,embed)

        user = await bot.fetch_user(ctx.author.id)
        if user is not None:
            embed = discord.Embed(title="정보 등록 완료[보안메시지]", description="{} 부로 {} 님의 정보 등록이 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2],end_msg), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 등록 실패", description=f"모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n형식  :  ?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg})", color=0x62c1cc)
        await ctx.send(embed = embed)
        embed = discord.Embed(title="정보 등록 실패", description=f"[{ctx.author}]님이 [{ctx.guild}] 서버 - [{ctx.channel}] 채널에서 정보등록을 실패하셨습니다.\n입력값 : ```{ctx.message.content}```{end_msg}",color=0x62c1cc)
        await send_embed_log(log_add_failure_channel,embed)
        
@bot.command()
async def 정보삭제(ctx):
    with open(json_file_name, "r",encoding='UTF-8') as json_file:
        user_data=json.load(json_file)

    if user_data.get(str(ctx.author.id)):
        data = user_data.pop(str(ctx.author.id))
        
        with open(json_file_name, "w",encoding='UTF-8') as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)

        now = datetime.datetime.now()
        embed = discord.Embed(title="정보 삭제 완료", description="{} 부로 {} 님의 정보 삭제가 완료되었습니다.\n구체적인 삭제 정보는 개인DM을 확인해주세요.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),data["name"],end_msg), color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))

        embed = discord.Embed(title="정보 삭제 완료[보안메시지]", description="{} 부로 {} 님의 정보 삭제가 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),data["name"],data["name"],data["birth"],data["area"],data["school_name"],data["school_type"],data["passward"][:2],end_msg), color=0x62c1cc)
        await user.send(embed=embed)

@bot.command()
async def 정보확인(ctx):
    with open(json_file_name, "r",encoding='UTF-8') as json_file:
        user_data=json.load(json_file)

    if user_data.get(str(ctx.author.id)):
        embed = discord.Embed(title="정보 확인", description=f"개인DM으로 정보를 보냈습니다.{end_msg})", color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="정보 확인[보안메시지]", description="이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n정보수정을 원하신다면 ?정보등록으로 새로 등록해주시기 바랍니다.\n이미 등록된 데이터가 있어도 새로 등록한 데이터를 기준으로 작동합니다.{}".format(user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2],end_msg), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 확인 실패",description=f"디스코드 아이디에 해당하는 데이터가 없습니다. 관리자에게 문의 부탁드립니다.{end_msg})", color=0x62c1cc)
        await ctx.send(embed=embed)
  
@bot.command()
async def 관리자정보확인(ctx):
    if str(ctx.author.id) == '523017072796499968':
        with open(json_file_name, "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        embed = discord.Embed(title="관리자 정보 확인", description=f"개인DM으로 정보를 보냈습니다.{end_msg})", color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="관리자 정보 확인[보안메시지]", description="서버 위치 : {}\n\n```{}```".format(host_name,str(user_data)), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def 관리자전체자가진단(ctx):
    if str(ctx.author.id) == '523017072796499968':
        with open(json_file_name, "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        global start_minute
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
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def 관리자전체공지(ctx,*,msg):
    if str(ctx.author.id) == '523017072796499968':
        with open(json_file_name, "r",encoding='UTF-8') as json_file:
            user_data=json.load(json_file)
        for user_id in user_data.keys():
            user = await bot.fetch_user(user_id)
            await user.send(msg)
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

token = os.environ["BOT_TOKEN"]
bot.run(token)
