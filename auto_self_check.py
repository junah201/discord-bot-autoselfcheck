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
import school_data

host_name = socket.gethostbyaddr(socket.gethostname())[0]

bot = commands.Bot(command_prefix='?')
#KST = datetime.timezone(datetime.timedelta(hours=9))

start_minute=13
last_day = "2021-05-29"
#start_minute=datetime.datetime.now().minute

end_msg = "\n\n개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=8&scope=bot)"
#end_msg = "\n\n봇 : 자동자가진단#4767 | 개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359?permissions=0?scope=bot)"

last_notice = []
last_personal_notice = ""

log_add_success_channel = "847490299638186054"
log_add_failure_channel = "847731541915467797"
log_bot_start_channel = "847732651912593439"
log_auto_self_check_failure_channel = "847793169683972146"
log_auto_self_check_success_channel = "847775280650518568"
log_auto_self_check_after_send_failure_channel ="847738621972578315"
log_json_backup_channel = "847830055916404766"
log_server_join = "848948171408539678"
log_server_remove = "848950238059560990"
log_today = "852145484239732756"

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

        success_user = 0
        failure_user = 0

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
            try:
                await send_DM(data,user_id,start_minute,user_data)
                if data["code"]=="SUCCESS":
                    success_user += 1
                else:
                    failure_user += 1
            except:
                print("send_DM 실패")
                failure_user += 1
        await send_log(log_today, f"{len(bot.guilds)}개의 서버에서 {success_user+failure_user}번의 자가진단이 실시되었습니다.\n(성공 : {success_user}명, 실패 : {failure_user}명)")

@bot.event
async def on_ready():
    print("봇 실행 완료")
    now = datetime.datetime.now()
    game = discord.Game(" ?명령어 | 노동  ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    embed = discord.Embed(title="봇 실행 완료", description=f"[{now}] 에 [{host_name}] 에서 봇이 실행되었습니다.", color=0x62c1cc)
    await send_log(log_bot_start_channel,f"`[{now}] [{host_name}] 에서 봇이 실행되었습니다.`")
    await user_data_backup()
    auto_self_check.start() #무한루프 실행

@bot.event
async def on_error(event, *args, **kwargs):
    user = await bot.fetch_user(523017072796499968)
    exc = sys.exc_info() #sys를 활용해서 에러를 확인합니다.
    await user.send(f"에러 발생 : {event} : {str(exc[0].__name__)} : {str(exc[1])}")

@bot.event
async def on_guild_join(guild):
    channels = guild.channels
    system_channel = guild.system_channel.id

    embed = discord.Embed(title="명령어", description="자동자가진단 봇에 대한 도움말 입니다. ?명령어 로 확인 가능합니다.\n평일날에만 자가진단이 작동하며, 공휴일 제외 기능을 추가할 예정입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]```?정보등록 홍길동 721027 서울시 길동고 고등학교 1234``````?정보등록 홍길동 050201 충청남도 길동중 중학교 2580```※정보등록은 `개인DM`으로 하는 것을 보안상 추천 드립니다.", inline=False)
    embed.add_field(name="?정보삭제", value="?정보삭제\n※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="?정보확인", value="?정보확인\n※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="기타명령어",value="`?학년반정보입력 [반] [번호]`\n`?급식`\n`?시간표`\n`?학사일정`", inline=False)
    embed.add_field(name="기타",value="자동자가진단은 7시 00분에서 7시 16분 사이에 랜덤하게 작동하며,\n자동자가진단 DM 메시지를 통하여 그 다음날의 작동 시간을 알 수 있습니다.", inline=False)
    embed.add_field(name="정보",value=end_msg)

    channel_list = ["채팅","챗","수다","chat","Chat"]

    for i in channels:
        if i.id != system_channel and str(i.type) == "text":
            if i.name in channel_list:
                channel = bot.get_channel(int(i.id))
                await channel.send(embed = embed)

    channel = bot.get_channel(int(system_channel))
    await channel.send(embed = embed)
    await send_log(log_server_join,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] `{guild.member_count-1}명`이 있는 [{guild}] 서버에 자가진단 봇이 추가되었습니다.")

@bot.event
async def on_guild_remove(guild):
    await send_log(log_server_remove,f"`[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{guild}] 서버에 자가진단 봇이 삭제되었습니다.`")

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
        #user는 메시지 전송용 discord.user 오브젝트
        user = await bot.fetch_user(int(user_id))
        erorr = "not erorr"
    except:
        erorr = "erorr"
        pass
    user_id = str(user_id)

    print(user_data[user_id])
    print(user_data[user_id].keys())
    print("school_code" in user_data[user_id].keys())
    if erorr != "erorr":
        if data["code"]=="SUCCESS":
            embed = discord.Embed(title="자가 진단 완료", description=f"일시 : `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n<:greencheck:847787187192725516>성공적으로 `{user_data[user_id]['name']}`님의 자가진단을 수행하였습니다.\n다음 자동자가진단은 `7시 {start_minute}분`에 실시될 예정입니다.", color=0x62c1cc)
            #학사일정 전송을 위해 학교코드, 지역코드가 있는지 확인 후 전송
            if "school_code" in user_data[user_id].keys() and "area_code" in user_data[user_id].keys() and str(user_data[user_id]["school_code"]) != "Null":
                schedule = await school_data.get_school_schedule(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'))
                if schedule != None:
                    msg = schedule
                else:
                    msg = "X"
                embed.add_field(name = "오늘의 학사일정",value = f"\n일정 : `{msg}`")

            #시간표 정보 전송을 위해 학년반 정보가 있는지 확인 후 전송
            if "school_grade" in user_data[user_id].keys() and "school_class" in user_data[user_id].keys():
                timetable = await school_data.get_school_timetable(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'),user_data[user_id]["school_type"],user_data[user_id]["school_grade"],user_data[user_id]["school_class"])
                if timetable != None:
                    msg = ""
                    for i in range(len(timetable)):
                        msg += f"{i+1}교시 : {timetable[i]}\n"
                    embed.add_field(name = "오늘의 시간표",value = f">>> {msg}")
            #학년반정보가 등록되지 않아서 시간표 정보 출력이 불가능 할 경우
            else:
                msg = "학년반 정보가 없습니다. `?학년반정보입력`으로 입력해주십시오."
                embed.add_field(name = "오늘의 시간표",value = f"`{msg}")

            #급식 정보 전송을 위해 학교코드, 지역코드가 있는지 확인 후 전송
            if "school_code" in user_data[user_id].keys() and "area_code" in user_data[user_id].keys() and str(user_data[user_id]["school_code"]) != "Null":
                cafeteria = await school_data.get_school_cafeteria(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'))
                if cafeteria != None:
                    msg = ""
                    for i in cafeteria:
                        msg += f"> {i}\n"
                    msg = msg[:-1]

                    embed.add_field(name = "오늘의 급식",value=f"{msg}")
            
            await user.send(embed=embed)
            await send_log(log_auto_self_check_success_channel,"[{}]`{}`님의 자가진단 완료".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"]))
            print("자가진단 성공 후 메시지 발송 완료...")
        #자가진단을 실패하였을 경우
        else:
            embed = discord.Embed(title="자가 진단 실패", description="[{}] 부로 [{}] 님의\n자가진단이 실시되었습니다만 자가진단에 실패하셨습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n\n{}{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],user_data[user_id]["name"],user_data[user_id]["birth"],user_data[user_id]["area"],user_data[user_id]["school_name"],user_data[user_id]["school_type"],user_data[user_id]["passward"][:2],data["message"],end_msg), color=0x62c1cc)
            await user.send(embed=embed)
            log_embed = discord.Embed(title="자가 진단 실패",description="[{}]\n{}[{}]님의 자가진단 실패\n{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]["name"],user_id,data["message"]), color=0x62c1cc)
            await send_embed_log(log_auto_self_check_failure_channel,log_embed)
            print("자가진단 실패 후 메시지 발송 완료...")
    #유저 id를 찾지 못하여 discord user 오브젝트를 못 얻었을 경우
    else:
        print("자가 진단 후 메시지 전송 실패...")
        embed = discord.Embed(title="자가 진단 후 메시지 전송 실패",description=f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 에 {user_data[user_id]['name']}(<@{user_id}>) 님의 자가진단이 실시되었습니다만 확인 메시지가 전송되지 않았습니다.\n자가진단결과 : {data['message']}", color=0x62c1cc)
        await send_embed_log(log_auto_self_check_after_send_failure_channel,embed)

@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title="명령어", description="자동자가진단 봇에 대한 도움말 입니다. ?명령어 로 확인 가능합니다.\n평일날에만 자가진단이 작동하며, 공휴일 제외 기능을 추가할 예정입니다.",color=0x62c1cc)
    embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]```?정보등록 홍길동 721027 서울시 길동고 고등학교 1234``````?정보등록 홍길동 050201 충청남도 길동중 중학교 2580```※정보등록은 `개인DM`으로 하는 것을 보안상 추천 드립니다.", inline=False)
    embed.add_field(name="?정보삭제", value="?정보삭제\n※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="?정보확인", value="?정보확인\n※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
    embed.add_field(name="기타명령어",value="`?학년반정보입력 [반] [번호]`\n`?급식`\n`?시간표`\n`?학사일정`", inline=False)
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
            #모든 입력 값이 정상일 경우
            with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
                user_data=json.load(json_file)

            user_data[str(ctx.author.id)] = {"uesr_id":str(ctx.author.id),"name":name,"birth":birth,"area":area,"school_name":school_name,"school_type":school_type,"passward":passward}

            now = datetime.datetime.now()
            if str(ctx.guild)!="None":
                embed = discord.Embed(title="정보 등록 완료", description="[{}] 에 `{}` 님의 정보 등록이 완료되었습니다.\n구체적인 등록 정보는 개인DM을 확인해주세요.{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),ctx.author,end_msg),color=0x62c1cc)
                await ctx.send(embed=embed)

            embed = discord.Embed(title="정보 등록 완료", description=f"이름 : [{ctx.author}]\n서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```", color=0x62c1cc)
            #embed.add_field(name="입력값",value=f"```{ctx.message.content}```{end_msg}")
            await send_embed_log(log_add_success_channel,embed)

            user_data[str(ctx.author.id)]["area_code"] = await school_data.get_area_code(user_data[str(ctx.author.id)]["area"])
            user_data[str(ctx.author.id)]["school_code"] = await school_data.get_school_code(user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["area_code"])
            
            with open(json_file_name, "w",encoding='utf-8-sig') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)

            user = await bot.fetch_user(ctx.author.id)
            if user is not None:
                embed = discord.Embed(title="정보 등록 완료[보안메시지]", description="[{}] 부로 `{}` 님의 정보 등록이 완료되었습니다.\n```이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**```{}".format(now.strftime('%Y-%m-%d %H:%M:%S'),user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2],end_msg), color=0x62c1cc)
                await user.send(embed=embed)
            else:
                user = await bot.fetch_user(523017072796499968)
                await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 등록 실패", description=f"모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n형식  :  ?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", color=0x62c1cc)
        await ctx.send(embed = embed)
        embed = discord.Embed(title="정보 등록 실패", description=f"[{ctx.author}]님이 [{ctx.guild}] 서버 - [{ctx.channel}] 채널에서 정보등록을 실패하셨습니다.\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
        await send_embed_log(log_add_failure_channel,embed)
    #등록 후 서버일 경우  등록 채팅 삭제
    if str(ctx.guild) != "None":
        msg = await ctx.send("유저 개인정보 보호를 위해 `5초` 후 삭제합니다.")
        await asyncio.sleep(1)
        await msg.edit(content="유저 개인정보 보호를 위해 `4초` 후 삭제합니다.")
        await asyncio.sleep(1)
        await msg.edit(content="유저 개인정보 보호를 위해 `3초` 후 삭제합니다.")
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
        if str(ctx.guild) != "None":
            embed = discord.Embed(title="정보 확인", description=f"개인DM으로 정보를 보냈습니다.{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="정보 확인[보안메시지]", description="```이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**```\n※정보수정을 원하신다면 `?정보등록`으로 새로 등록해주시기 바랍니다.\n※이미 등록된 데이터가 있어도 새로 등록한 데이터를 기준으로 작동합니다.{}".format(user_data[str(ctx.author.id)]["name"],user_data[str(ctx.author.id)]["birth"],user_data[str(ctx.author.id)]["area"],user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["school_type"],user_data[str(ctx.author.id)]["passward"][:2],end_msg), color=0x62c1cc)
            await user.send(embed=embed)
        else:
            user = await bot.fetch_user(523017072796499968)
            await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
    else:
        embed = discord.Embed(title="정보 확인 실패",description=f"디스코드 아이디에 해당하는 데이터가 없습니다. 관리자에게 문의 부탁드립니다.{end_msg}", color=0x62c1cc)
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
async def 관리자전체공지삭제(ctx,*,msg):
    if str(ctx.author.id) == '523017072796499968':
        global last_notice
        for last_msg in last_notice:
            await last_msg.delete()
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def 관리자개인공지(ctx,name,birth,*,msg):
    if str(ctx.author.id) == '523017072796499968':
        global last_personal_notice
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
            user_data=json.load(json_file)
        user=None
        for i in user_data.keys():
            if user_data[i]["name"] == name and user_data[i]["birth"] == birth:
                user=i
                break

        if user!=None:
            embed = discord.Embed(title="관리자 개인 메시지",description=f"{msg}\n\n발신인 : 관리자[{ctx.author}]", color=0x62c1cc)
            user = await bot.fetch_user(int(user))
            last_personal_notice = await user.send(embed=embed)
            await ctx.send("전송 완료!")
        else:
            await ctx.send("해당 유저가 없습니다.")
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

@bot.command()
async def Ping(ctx):
    for i in range(5):
        await ctx.send(f"현재 핑은 `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}` 기준으로 `{str(round(bot.latency*1000))}ms` 입니다.")

@bot.command()
async def 관리자종료(ctx):
    if str(ctx.author.id) == '523017072796499968':
        await ctx.bot.logout()
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")

'''
            if "school_code" in user_data[user_id].keys() and "area_code" in user_data[user_id].keys() and str(user_data[user_id]["school_code"]) != "Null":
                cafeteria = await school_data.get_school_cafeteria(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'))
                if cafeteria != None:
                    msg = ""
                    for i in cafeteria:
                        msg += f"> {i}\n"
                    msg = msg[:-1]

                    embed.add_field(name = "오늘의 급식",value=f"{msg}")
'''

@bot.command()
async def 급식(ctx, day:str=str(datetime.datetime.now().strftime('%Y%m%d')),user: discord.User=None):
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)
    print(day)
    if len(day) == 8 and day.isdigit():
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
            user_data=json.load(json_file)

        if user in user_data:
            user_data_keys = user_data[user].keys()
            if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
                user_data[user]["area_code"] = await school_data.get_area_code(user_data[user]["area"])
                user_data[user]["school_code"] = await school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
                with open(json_file_name, "w",encoding='UTF-8') as json_file:
                    json.dump(user_data,json_file,ensure_ascii = False, indent=4)
                
            cafeteria = await school_data.get_school_cafeteria(user_data[user]["school_code"],user_data[user]["area_code"],day)

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
            await ctx.send("해당 유저의 데이터가 없습니다. `?정보등록`으로 유저 데이터를 입력해주십시오.")
    else:
        await ctx.send("날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `20210612`)")

'''
import datetime

# 현재 시간 가져오기
current =  datetime.datetime.now()

# 1시간 후
one_hour_later = current + datetime.timedelta(hours=1)
# 1시간 전
one_hour_ago = current - datetime.timedelta(hours=1)

# 내일 시간
tomorrow = current  + datetime.timedelta(days=1)
# 어제 시간
yesterday = current - datetime.timedelta(days=1)

# 10분 후
ten_minutes_later = current + datetime.timedelta(minutes=10)
# 10분 전
ten_minutes_later = current - datetime.timedelta(minutes=10)
'''


@bot.command()
async def 내일급식(ctx,user: discord.User=None): 
    day=datetime.datetime.now() + datetime.timedelta(days=1)
    day = day.strftime('%Y%m%d')
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)
    print(day)
    with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
        user_data=json.load(json_file)

    if user in user_data:
        user_data_keys = user_data[user].keys()
        if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
            user_data[user]["area_code"] = await school_data.get_area_code(user_data[user]["area"])
            user_data[user]["school_code"] = await school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
            with open(json_file_name, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            
        cafeteria = await school_data.get_school_cafeteria(user_data[user]["school_code"],user_data[user]["area_code"],day)

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
        await ctx.send("해당 유저의 데이터가 없습니다. `?정보등록`으로 유저 데이터를 입력해주십시오.")

@bot.command()
async def 어제급식(ctx,user: discord.User=None): 
    day=datetime.datetime.now() - datetime.timedelta(days=1)
    day = day.strftime('%Y%m%d')
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)
    print(day)
    with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
        user_data=json.load(json_file)

    if user in user_data:
        user_data_keys = user_data[user].keys()
        if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
            user_data[user]["area_code"] = await school_data.get_area_code(user_data[user]["area"])
            user_data[user]["school_code"] = await school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
            with open(json_file_name, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            
        cafeteria = await school_data.get_school_cafeteria(user_data[user]["school_code"],user_data[user]["area_code"],day)

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
        await ctx.send("해당 유저의 데이터가 없습니다. `?정보등록`으로 유저 데이터를 입력해주십시오.")

@bot.command()
async def 학년반정보입력(ctx, school_grade:str=None, school_class:str=None):
    if school_grade == None or school_class == None:
        await ctx.send("`?학년반정보입력 [학년] [반]`의 형식으로 입력해주십시오. (예 : `?학년반정보입력 1 3`)")
    else:
        print(f"grade : {school_grade}, class : {school_class}")
        if school_grade.isdigit() and school_class.isdigit() and int(school_grade) < 7 and int(school_class) < 40:
            with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
                user_data=json.load(json_file)

            user_data[str(ctx.author.id)]["school_grade"] = school_grade
            user_data[str(ctx.author.id)]["school_class"] = school_class

            with open(json_file_name, "w",encoding='UTF-8') as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)

            embed = discord.Embed(title="정보 입력 완료",description=f"학년 : `{school_grade}` \n반 : `{school_class}`{end_msg}", color=0x62c1cc)
            await ctx.send(embed = embed)

@bot.command()
async def 학교코드(ctx):
    with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
        user_data=json.load(json_file)
    for i in user_data.keys():
        print(user_data[i]["name"])
        user_data[i]["area_code"] = await school_data.get_area_code(user_data[i]["area"])
        user_data[i]["school_code"] = await school_data.get_school_code(user_data[i]["school_name"],user_data[i]["area_code"])
        print("name : {},area_code : {}, school_code : {}".format(user_data[i]["name"],user_data[i]["area_code"],user_data[i]["school_code"]))
    with open(json_file_name, "w",encoding='UTF-8') as json_file:
        json.dump(user_data,json_file,ensure_ascii = False, indent=4)



@bot.command()
async def 시간표(ctx, day:str=str(datetime.datetime.now().strftime('%Y%m%d')),user: discord.User=None):
    print(day)
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)

    if len(day) == 8 and day.isdigit():
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
            user_data=json.load(json_file)

        user_data_keys = user_data[user].keys()

        if user in user_data:
            if "school_grade" not in user_data_keys and "school_class" not in user_data_keys:
                await ctx.send("입력된 학년반 데이터가 없습니다. `?학년반정보입력` 으로 입력해주십시오.")
            else:
                if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
                    user_data[user]["area_code"] = await school_data.get_area_code(user_data[user]["area"])
                    user_data[user]["school_code"] = await school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
                    with open(json_file_name, "w",encoding='UTF-8') as json_file:
                        json.dump(user_data,json_file,ensure_ascii = False, indent=4)

                timetable = await school_data.get_school_timetable(user_data[user]["school_code"],user_data[user]["area_code"],day,user_data[user]["school_type"],user_data[user]["school_grade"],user_data[user]["school_class"])
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
        await ctx.send("날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `20210612`)")

@bot.command()
async def 학사일정(ctx, day:str=str(datetime.datetime.now().strftime('%Y%m%d')),user: discord.User=None):
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)

    if len(day) == 8 and day.isdigit():
        with open(json_file_name, "r",encoding='utf-8-sig') as json_file:
            user_data=json.load(json_file)

        user_data_keys = user_data[user].keys()

        if user in user_data:
            if "school_code" not in user_data_keys and "area_code" not in user_data_keys:
                user_data[user]["area_code"] = await school_data.get_area_code(user_data[user]["area"])
                user_data[user]["school_code"] = await school_data.get_school_code(user_data[user]["school_name"],user_data[user]["area_code"])
                with open(json_file_name, "w",encoding='UTF-8') as json_file:
                    json.dump(user_data,json_file,ensure_ascii = False, indent=4)
            schedule = await school_data.get_school_schedule(user_data[user]["school_code"],user_data[user]["area_code"],day)
            await ctx.send(f"일시 : `{day}`\n일정 : {schedule}")
    else:
        await ctx.send("날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `20210612`)")

@bot.command()
async def 시간(ctx):
    await ctx.send(f"{datetime.datetime.now().strftime('%Y%m%d')}")

@bot.command()
async def 재시작(ctx):
    bot.logout()
    bot.run(token)

@bot.command()
async def test(ctx):
    embed = discord.Embed(title="test",description=f"<:greencheck:847787187192725516>", color=0x62c1cc)
    await ctx.send(embed=embed)

with open("config.json", "r",encoding='UTF-8') as json_file:
    config=json.load(json_file)
    
json_file_name = config["json_file"]
print(json_file_name)
token = config["token"]
bot.run(token)
