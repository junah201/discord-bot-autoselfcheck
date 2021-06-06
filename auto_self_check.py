#-*- coding: UTF8-*-

import discord
from discord.ext import commands, tasks
import time, datetime
import hcskr
import random
import json
import os, sys
import socket
import asyncio

host_name = socket.gethostbyaddr(socket.gethostname())[0]

bot = commands.Bot(command_prefix='?')
#KST = datetime.timezone(datetime.timedelta(hours=9))

start_minute=2
last_day = "2021-05-29"
#start_minute=datetime.datetime.now().minute

end_msg = "\n\n개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=0&scope=bot)"
#end_msg = "\n\n봇 : 자동자가진단#4767 | 개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359?permissions=0?scope=bot)"
json_file_name = "user_data.json"
last_notice = []

log_add_success_channel = "847490299638186054"
log_add_failure_channel = "847731541915467797"
log_bot_start_channel = "847732651912593439"
log_auto_self_check_failure_channel = "847793169683972146"
log_auto_self_check_success_channel = "847775280650518568"
log_auto_self_check_after_send_failure_channel ="847738621972578315"
log_json_backup_channel = "847830055916404766"
log_server_join = "848948171408539678"
log_server_remove = "848950238059560990"

area_list = ['서울시','부산시','대구시','인천시','광주시','대전시','울산시','세종시','경기도','강원도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주도','제주특별자치도']
back_area_list = ['서울', '서울시', '서울교육청', '서울시교육청', '서울특별시','부산', '부산광역시', '부산시', '부산교육청', '부산광역시교육청','대구', '대구광역시', '대구시', '대구교육청', '대구광역시교육청','인천', '인천광역시', '인천시', '인천교육청', '인천광역시교육청','광주', '광주광역시', '광주시', '광주교육청', '광주광역시교육청','대전', '대전광역시', '대전시', '대전교육청', '대전광역시교육청','울산', '울산광역시', '울산시', '울산교육청', '울산광역시교육청','세종', '세종특별시', '세종시', '세종교육청', '세종특별자치시', '세종특별자치시교육청','경기', '경기도', '경기교육청', '경기도교육청','강원', '강원도', '강원교육청', '강원도교육청','충북', '충청북도', '충북교육청', '충청북도교육청','충남', '충청남도', '충남교육청', '충청남도교육청','전북', '전라북도', '전북교육청', '전라북도교육청','전남', '전라남도', '전남교육청', '전라남도교육청','경북', '경상북도', '경북교육청', '경상북도교육청','경남', '경상남도', '경남교육청', '경상남도교육청','제주', '제주도', '제주특별자치시', '제주교육청', '제주도교육청', '제주특별자치시교육청', '제주특별자치도']
back_school_type_list = ['유치원', '유','유치','초등학교', '초','초등','중학교', '중','중등','고등학교', '고','고등','특수학교', '특','특수','특별']
school_type_list = ['유치원', '초등학교','중학교', '고등학교','특수학교']

@tasks.loop(seconds=60)
async def auto_self_check():
    global start_minute
    global last_day
    print(f"[{datetime.datetime.now()}] 무한루프가 돌아가는 중...")
    if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == start_minute and last_day != datetime.datetime.now().strftime('%Y-%m-%d') and datetime.datetime.today().weekday()<5:
        await user_data_backup()
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
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

@bot.event
async def on_guild_join(guild):
    await send_log(log_server_join,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 부로 [{guild}] 서버에 자가진단 봇이 추가되었습니다.")

@bot.event
async def on_guild_remove(guild):
    await send_log(log_server_remove,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 부로 [{guild}] 서버에 자가진단 봇이 삭제되었습니다.")

async def user_data_backup():
    channel = bot.get_channel(int(log_json_backup_channel))
    await channel.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

    file = discord.File("user_data.json")
    await channel.send(file=file)
    file = discord.File("auto_self_check.py")
    await channel.send(file=file)



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
            embed = discord.Embed(title="자가 진단 완료", description="[{}] 부로 `{}` 님의 자가진단이 성공적으로 실시되었습니다.\n(API 출력메시지 : {})\n다음 자동자가진단은 `7시 {}분`에 실시될 예정입니다.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],data["message"],start_minute,end_msg), color=0x62c1cc)
            await user.send(embed=embed)
            await send_log(log_auto_self_check_success_channel,"[{}]{}님의 자가진단 완료".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"]))
            print("자가진단 성공 후 메시지 발송 완료...")
        else:
            now = datetime.datetime.now()
            embed = discord.Embed(title="자가 진단 실패", description="[{}] 부로 [{}] 님의\n자가진단이 실시되었습니다만 자가진단에 실패하셨습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n\n{}{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],user_data[user_id]["name"],user_data[user_id]["birth"],user_data[user_id]["area"],user_data[user_id]["school_name"],user_data[user_id]["school_type"],user_data[user_id]["passward"][:2],data["message"],end_msg), color=0x62c1cc)
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
async def 명령어(ctx):
    embed = discord.Embed(title="도움말", description="자동자가진단 봇에 대한 도움말 입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]```?정보등록 홍길동 721027 서울시 길동고 고등학교 1234``````?정보등록 홍길동 050201 충청남도 길동중 중학교 2580```※정보등록은 `개인DM`으로 하는 것을 보안상 추천 드립니다.", inline=False)
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
        if area not in back_area_list:
            embed = discord.Embed(title="정보 등록 실패", description=f"지역은 아래 항목 중 하나로 입력해주셔야 합니다.\n(입력값 : {area})")
            embed.add_field(name="지역 리스트",value=f"```{area_list}```", inline=False)
            embed.add_field(name="입력 형식",value=f"?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
            await ctx.send(embed=embed)
        elif len(passward) != 4 or passward.isdigit()==False:
            embed = discord.Embed(title="정보 등록 실패", description=f"비밀번호는 숫자 4글자의 형태로 입력해주셔야 합니다.\n(입력값 : {passward})")
            embed.add_field(name="입력 형식",value=f"?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
            await ctx.send(embed=embed)
        elif len(birth)!=6 or birth.isdigit() == False:
            embed = discord.Embed(title="정보 등록 실패", description=f"생년월일는 숫자 6글자의 형태로 입력해주셔야 합니다.\n(입력값 : {birth})")
            embed.add_field(name="입력 형식",value=f"?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
            await ctx.send(embed=embed)
        elif school_type not in back_school_type_list:
            embed = discord.Embed(title="정보 등록 실패", description=f"학교 타입은 아래 항목 중 하나로 입력해주셔야 합니다.\n(입력값 : {school_type})")
            embed.add_field(name="지역 리스트",value=f"```{school_type_list}```", inline=False)
            embed.add_field(name="입력 형식",value=f"?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
            await ctx.send(embed=embed)
        else:
            with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
                user_data=json.load(json_file)
            user_data[str(ctx.author.id)] = {"uesr_id":str(ctx.author.id),"name":name,"birth":birth,"area":area,"school_name":school_name,"school_type":school_type,"passward":passward}

            with open(json_file_name, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            now = datetime.datetime.now()
            if str(ctx.guild)!="None":
                embed = discord.Embed(title="정보 등록 완료", description="[{}] 에 `{}` 님의 정보 등록이 완료되었습니다.\n구체적인 등록 정보는 개인DM을 확인해주세요.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),ctx.author,end_msg),color=0x62c1cc)
                await ctx.send(embed=embed)

            embed = discord.Embed(title="정보 등록 완료", description=f"이름 : [{ctx.author}]\n서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```{end_msg}", color=0x62c1cc)
            #embed.add_field(name="입력값",value=f"```{ctx.message.content}```{end_msg}")
            await send_embed_log(log_add_success_channel,embed)

            user = await bot.fetch_user(ctx.author.id)
            if user is not None:
                embed = discord.Embed(title="정보 등록 완료[보안메시지]", description="[{}] 부로 `{}` 님의 정보 등록이 완료되었습니다.\n```이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**```{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2],end_msg), color=0x62c1cc)
                await user.send(embed=embed)

            else:
                user = await bot.fetch_user(523017072796499968)
                await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 등록 실패", description=f"모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n형식  :  ?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg})", color=0x62c1cc)
        await ctx.send(embed = embed)
        embed = discord.Embed(title="정보 등록 실패", description=f"[{ctx.author}]님이 [{ctx.guild}] 서버 - [{ctx.channel}] 채널에서 정보등록을 실패하셨습니다.\n입력값 : ```{ctx.message.content}```{end_msg}",color=0x62c1cc)
        await send_embed_log(log_add_failure_channel,embed)
    #등록 후 서버일 경우  등록 채팅 삭제
    if str(ctx.guild) != "None":
        msg = await ctx.send("유저 개인정보 보호를 위해 `3초` 후 삭제합니다.")
        await asyncio.sleep(1)
        await msg.edit(content="유저 개인정보 보호를 위해 `2초` 후 삭제합니다.")
        await asyncio.sleep(1)
        await msg.edit(content="유저 개인정보 보호를 위해 `1초` 후 삭제합니다.")
        await asyncio.sleep(1)
        await ctx.message.delete()
        await msg.edit(content="유저 개인정보 보호를 위해 삭제하였습니다. 등록정보는 `?정보확인` 명령어 혹은 개인DM을 확인해주십시오")

@bot.command()
async def 정보삭제(ctx):
    with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
        user_data=json.load(json_file)

    if user_data.get(str(ctx.author.id)):
        data = user_data.pop(str(ctx.author.id))

        with open(json_file_name, "w",encoding='utf-8-sig') as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)

        now = datetime.datetime.now()
        embed = discord.Embed(title="정보 삭제 완료", description="[{}] 부로 {} 님의 정보 삭제가 완료되었습니다.\n구체적인 삭제 정보는 개인DM을 확인해주세요.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),data["name"],end_msg), color=0x62c1cc)
        await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))

        embed = discord.Embed(title="정보 삭제 완료[보안메시지]", description="[{}] 부로 {} 님의 정보 삭제가 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),data["name"],data["name"],data["birth"],data["area"],data["school_name"],data["school_type"],data["passward"][:2],end_msg), color=0x62c1cc)
        await user.send(embed=embed)
    else:
        now = datetime.datetime.now()
        embed = discord.Embed(title="정보 삭제 실패", description="[{}] 에  <@{}> 님의 정보 삭제를 실패하셨습니다.\n디스코드 아이디[{}]로 등록된 정보가 없습니다.\n구체적인 문의는 관리자[white201#0201]님께 문의 부탁드립니다.".format(now.strftime('%Y-%m-%d %H:%M:%S'),ctx.author.id,ctx.author.id,end_msg), color=0x62c1cc)
        await ctx.send(embed=embed)

@bot.command()
async def 정보확인(ctx):
    with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
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
        global json_file_name
        await ctx.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d')}]\nhost name : {host_name}\njson file name : {json_file_name}")
        file = discord.File("user_data.json")
        await ctx.send(file=file)
        file = discord.File("auto_self_check.py")
        await ctx.send(file=file)
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def 관리자전체자가진단(ctx):
    if str(ctx.author.id) == '523017072796499968':
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
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
        global last_notice
        last_notice = []
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
            user_data=json.load(json_file)
        for user_id in user_data.keys():
            user = await bot.fetch_user(user_id)
            temp_msg = await user.send(msg)
            last_notice.append(temp_msg)
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def 관리자전체공지수정(ctx,*,msg):
    if str(ctx.author.id) == '523017072796499968':
        global last_notice
        for last_msg in last_notice:
            await last_msg.edit(content=str(msg))
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def 수정(ctx,*,msg):
    await ctx.send("3초 후 삭제합니다.")
    await asyncio.sleep(3)
    await ctx.message.delete()





token = 'ODQ2NjUwNjE4NzAxMjgzMzU5.YKym1Q.O1KtKTGHRJszDSVJKZ71Kq0QYuM'
#token = 'Nzk4NDI0NTk5NDk4MDYzODky.X_002g.Wgrp8Mr_gfpJrhBbd4UQHAUkVVo'
bot.run(token)
