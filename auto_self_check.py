#-*- coding: UTF8-*-

import discord
from discord.ext import commands, tasks
import datetime
import hcskr
import random
import json
import os, sys
import socket
import asyncio
import koreanbots
from dotenv import load_dotenv

import get_school_data
import get_covid19_data

from embed.help_embed import *
from channels.log_channels import *

load_dotenv()

JSON_FILE_NAME = os.getenv('JSON_FILE_NAME')
print(f"json_file_name : {JSON_FILE_NAME}")

TOKEN = os.getenv("TOKEN")
print(f"token : {TOKEN}")

host_name = socket.gethostbyaddr(socket.gethostname())[0]
print(f"host_name : {host_name}")

PREFIX = os.getenv("PREFIX")
print(f"prefix : {PREFIX}")

ADMIN_ID = os.getenv("ADMIN_ID")
print(f"admin_id : {ADMIN_ID}")

KOR_TOKEN = os.getenv("KOR_TOKEN")
print(f"kor_token : {KOR_TOKEN}")

bot = commands.Bot(command_prefix=PREFIX)
#KST = datetime.timezone(datetime.timedelta(hours=9))

start_minute=1
last_day = "2021-08-31"

last_notice = []
last_personal_notice = ""

area_list = ['서울시','부산시','대구시','인천시','광주시','대전시','울산시','세종시','경기도','강원도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주도','제주특별자치도']
back_area_list = ['서울', '서울시', '서울교육청', '서울시교육청', '서울특별시','부산', '부산광역시', '부산시', '부산교육청', '부산광역시교육청','대구', '대구광역시', '대구시', '대구교육청', '대구광역시교육청','인천', '인천광역시', '인천시', '인천교육청', '인천광역시교육청','광주', '광주광역시', '광주시', '광주교육청', '광주광역시교육청','대전', '대전광역시', '대전시', '대전교육청', '대전광역시교육청','울산', '울산광역시', '울산시', '울산교육청', '울산광역시교육청','세종', '세종특별시', '세종시', '세종교육청', '세종특별자치시', '세종특별자치시교육청','경기', '경기도', '경기교육청', '경기도교육청','강원', '강원도', '강원교육청', '강원도교육청','충북', '충청북도', '충북교육청', '충청북도교육청','충남', '충청남도', '충남교육청', '충청남도교육청','전북', '전라북도', '전북교육청', '전라북도교육청','전남', '전라남도', '전남교육청', '전라남도교육청','경북', '경상북도', '경북교육청', '경상북도교육청','경남', '경상남도', '경남교육청', '경상남도교육청','제주', '제주도', '제주특별자치시', '제주교육청', '제주도교육청', '제주특별자치시교육청', '제주특별자치도']
back_school_type_list = ['유치원', '유','유치','초등학교', '초','초등','중학교', '중','중등','고등학교', '고','고등','특수학교', '특','특수','특별']
school_type_list = ['유치원', '초등학교','중학교', '고등학교','특수학교']

kb = koreanbots.Koreanbots(bot, KOR_TOKEN, run_task=True)
print(kb)

@tasks.loop(seconds=60)
async def auto_self_check():
    global start_minute
    global last_day

    print(f"[{datetime.datetime.now()}] 무한루프가 돌아가는 중...")
    #자가진단 실행 if문
    #if True:
    if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == start_minute and last_day != datetime.datetime.now().strftime('%Y-%m-%d') and datetime.datetime.today().weekday()<5:
        print("실행")
        await user_data_backup()
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)

        success_user = 0
        failure_user = 0

        start_minute=random.randrange(1,16)
        last_day = datetime.datetime.now().strftime('%Y-%m-%d')
        for user_id in user_data.keys():
            if user_data[user_id]["possible"] == True:
                name = user_data[user_id]['name']
                birth = user_data[user_id]["birth"]
                area = user_data[user_id]["area"]
                school_name = user_data[user_id]["school_name"]
                school_type = user_data[user_id]["school_type"]
                passward = user_data[user_id]["passward"]
                user_id = user_data[user_id]["uesr_id"]
                print(f"자동자가진단 : [{name}]님의 자가진단 준비중")

                try:
                    data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                    await send_DM(data,user_id,start_minute,user_data)
                except Exception as ex:
                    print("무지성 트라이 1트")
                    print(f"{user_data[user_id]['name']}:{ex}")
                    user = await bot.fetch_user(523017072796499968)
                    await user.send(f"{user_data[user_id]['name']}::{ex}")
                    try:
                        data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                        await send_DM(data,user_id,start_minute,user_data)
                    except Exception as ex:
                        print("무지성 트라이 2트")
                        print(f"{user_data[user_id]['name']}:{ex}")
                        user = await bot.fetch_user(523017072796499968)
                        await user.send(f"{user_data[user_id]['name']}::{ex}")
                        try:
                            data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                            await send_DM(data,user_id,start_minute,user_data)
                        except Exception as ex:
                            print("무지성 트라이 3트 후 포기")
                            print(f"{user_data[user_id]['name']}:{ex}")
                            user = await bot.fetch_user(523017072796499968)
                            await user.send(f"{user_data[user_id]['name']}::{ex}")
                            data = {}
                            data["code"]="ERROR"
                            pass

                if data["code"]=="SUCCESS":
                    success_user += 1
                else:
                    failure_user += 1

        print("완료")
        #채널
        await send_log(log_today, f"{len(bot.guilds)}개의 서버에서 {success_user+failure_user}번의 자가진단이 실시되었습니다.\n(성공 : {success_user}명, 실패 : {failure_user}명)")
        #합계
        '''
        channel = bot.get_channel(int(log_today_total))
        msg = str(f"합계 : {success_user+failure_user}")
        await channel.edit(name=msg)
        '''
        #성공
        channel = bot.get_channel(int(log_today_success))
        msg = str(f"성공 : {success_user}")
        await channel.edit(name=msg)
        #실패
        '''
        channel = bot.get_channel(int(log_today_failure))
        msg = str(f"실패 : {failure_user}")
        await channel.edit(name=msg)
        '''

    #정보 수집 if문
    #if True:
    if datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 0:
        print("===정보 수집 시작===")
        
        await user_data_backup()
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        #코로나19 확진자 수 수집
        covid19_data = await get_covid19_data.get_covid19_decide()
        with open("area_code.json", "r",encoding="utf-8-sig") as json_file:
            area_code=json.load(json_file)

        for user_id in user_data.keys():
            #기본값 설정
            user_data[user_id]["schedule"] = None
            user_data[user_id]["cafeteria"] = None
            user_data[user_id]["timetable"] = None
            user_data[user_id]['area_covid19_decide'] = None
            user_data[user_id]['all_covid19_decide'] = None

            #possible이 True 일때만 데이터 수집
            if user_data[user_id]["possible"] == True:
                try:
                    #학사일정 수집 후 방학 또는 개학일 때 자가진단 실행 여부 조정
                    user_data[user_id]["schedule"] = await get_school_data.get_school_schedule(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'))
                    if "방학" in user_data[user_id]["schedule"]:
                        #user_data[user_id]["possible"] = False
                        #user = await bot.fetch_user(int(user_id))
                        #await user.send(f"오늘부터 자가진단이 실시되지 않을 예정입니다.\n(사유 : 학사일정에 방학식이 확인됨)")
                        pass
                    elif "개학" in user_data[user_id]["schedule"]:
                        user_data[user_id]["possible"] = True
                        user = await bot.fetch_user(int(user_id))
                        await user.send(f"오늘부터 자가진단이 실시될 예정입니다.\n(사유 : 학사일정에 개학식이 확인됨)")
                except Exception as ex:
                    print(f"{user_data[user_id]['name']} : {ex}")

                try:    
                    #급식정보 수집
                    user_data[user_id]["cafeteria"] = await get_school_data.get_school_cafeteria(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'))
                except Exception as ex:
                    user = await bot.fetch_user(523017072796499968)
                    await user.send(f"급식 데이터 수집 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")

                try:
                    #시간표 정보 수집 전 학년 반 정보가 입력되었는지 확인
                    if "school_grade" in user_data[user_id].keys() and "school_class" in user_data[user_id].keys():
                        user_data[user_id]["timetable"] = await get_school_data.get_school_timetable(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'),user_data[user_id]["school_type"],user_data[user_id]["school_grade"],user_data[user_id]["school_class"])
                    else:
                        user_data[user_id]["timetable"] = "No information entered"
                except Exception as ex:
                    user = await bot.fetch_user(523017072796499968)
                    await user.send(f"시간표 데이터 수집 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")

                try:
                    #전체 코로나 정보에서 해당 지역의 코로나 정보만 수집
                    user_data[user_id]['area_covid19_decide'] = covid19_data[area_code[user_data[user_id]["area_code"]]]
                    user_data[user_id]['all_covid19_decide'] = covid19_data['합계']
                except Exception as ex:
                    user = await bot.fetch_user(523017072796499968)
                    await user.send(f"지역 코로나 데이터 수집 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")
                
                try:
                    #failure의 값이 5 이상이면 정보 삭제
                    if "failure" in user_data[user_id].keys():
                        if user_data[user_id]["failure"] >= 5:
                            user_data[user_id]['possible'] = False
                            user = await bot.fetch_user(int(user_id))
                            await user.send(f'5회 이상 자가진단에 실패하여, 자동자가진단이 중지 상태로 변경되었습니다.')

                except Exception as ex:
                    user = await bot.fetch_user(523017072796499968)
                    await user.send(f"failure 측정 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")
                with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
                    json.dump(user_data,json_file,ensure_ascii = False, indent=4)

        print("===정보 수집 완료===")

@bot.event
async def on_ready():  
    print(f"{bot.user} 실행 완료")
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)
    game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 중 ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    embed = discord.Embed(title="봇 실행 완료", description=f"[{datetime.datetime.now()}] 에 [{host_name}] 에서 봇이 실행되었습니다.", color=0x62c1cc)
    await send_log(log_bot_start_channel,f"`[{datetime.datetime.now()}] [{host_name}] 에서 봇이 실행되었습니다.`")
    await user_data_backup()
    auto_self_check.start()

@bot.event
async def on_error(event, *args, **kwargs):
    exc = sys.exc_info() #sys를 활용해서 에러를 확인합니다.
    user = await bot.fetch_user(523017072796499968)
    await user.send(f"에러 발생 : {event} : {str(exc[0].__name__)} : {str(exc[1])}")

@bot.event
async def on_guild_join(guild):
    channels = guild.channels
    await send_log(log_server_join,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] `{guild.member_count-1}명`이 있는 [{guild}] 서버에 자가진단 봇이 추가되었습니다.")
    global help_embed
    system_channel = guild.system_channel.id
    channel = bot.get_channel(int(system_channel))
    await channel.send(embed = help_embed)
    #해당 리스트에 있는 단어가 채널이름에 있을 경우 도움말 표시
    try:
        for i in channels:
            if i.id != system_channel and str(i.type) == "text":
                if i.name in ["채팅","챗","수다","chat","Chat"]:
                    channel = bot.get_channel(int(i.id))
                    await channel.send(embed = help_embed)
    except:
        pass

@bot.event
async def on_guild_remove(guild):
    await send_log(log_server_remove,f"`[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {guild.member_count}명이 있는 [{guild}] 서버에 자가진단 봇이 삭제되었습니다.`")

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
    with open("area_code.json", "r",encoding="utf-8-sig") as json_file:
        area_code=json.load(json_file)
    try:
        if erorr != "erorr":
            if data["code"]=="SUCCESS":
                user_data[user_id]["failure"] = 0
                embed = discord.Embed(title="자가 진단 완료", description=f"일시 : `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n<:greencheck:847787187192725516>성공적으로 `{user_data[user_id]['name']}`님의 자가진단을 수행하였습니다.\n다음 자동자가진단은 `7시 {start_minute}분`에 실시될 예정입니다.", color=0x62c1cc)
                #학사일정 정보 전송을 위해 학사일정 정보가 있는지 확인 후 전송
                if user_data[user_id]["schedule"] != None and str(user_data[user_id]["schedule"]) != "null":
                    embed.add_field(name = "오늘의 학사일정",value = f"\n일정 : `{user_data[user_id]['schedule']}`")
                #시간표 정보 전송을 위해 학년반 정보가 있는지 확인 후 전송
                if user_data[user_id]["timetable"] != None and str(user_data[user_id]["timetable"]) != "null" and user_data[user_id]["timetable"] != "No information entered":
                    timetable = user_data[user_id]["timetable"]
                    msg = ""
                    for i in range(len(timetable)):
                        msg += f"{i+1}교시 : {timetable[i]}\n"
                    embed.add_field(name = "오늘의 시간표",value = f">>> {msg}")
                #학년반정보가 등록되지 않아서 시간표 정보 출력이 불가능 할 경우
                else:
                    embed.add_field(name = "오늘의 시간표",value = f"학년반 정보가 없습니다. `{PREFIX}학년반정보입력`으로 입력해주십시오.")
                #급식 정보 전송
                if user_data[user_id]["cafeteria"] != None and str(user_data[user_id]["cafeteria"]) != "null":
                    msg = ""
                    for i in user_data[user_id]["cafeteria"]:
                        msg += f"> {i}\n"
                    msg = msg[:-1]
                    embed.add_field(name = "오늘의 급식",value=f"{msg}")
                #코로나 확진자 수 전송
                if user_data[user_id]['all_covid19_decide'] !=None and user_data[user_id]['area_covid19_decide'] != None:
                    embed.add_field(name = "코로나 확진자",value=f"전국 : {user_data[user_id]['all_covid19_decide']}명, {area_code[user_data[user_id]['area_code']]} : {user_data[user_id]['area_covid19_decide']}명\n※{(datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d')} 0시 기준")
                #최종 전송 및 로그 전송
                await user.send(embed=embed)
                await send_log(log_auto_self_check_success_channel,"[{}]`{}`님의 자가진단 완료".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]['name']))
                print("자가진단 성공 후 메시지 발송 완료...")
            #자가진단을 실패하였을 경우
            else:
                embed = discord.Embed(title="자가 진단 실패", description="[{}] 부로 [{}] 님의\n자가진단이 실시되었습니다만 자가진단에 실패하셨습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**\n\n{}{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]['name'],user_data[user_id]['name'],user_data[user_id]["birth"],user_data[user_id]["area"],user_data[user_id]["school_name"],user_data[user_id]["school_type"],user_data[user_id]["passward"][:2],data["message"],end_msg), color=0x62c1cc)
                await user.send(embed=embed)
                log_embed = discord.Embed(title="자가 진단 실패",description="[{}]\n{}[{}]님의 자가진단 실패\n{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]['name'],user_id,data["message"]), color=0x62c1cc)
                await send_embed_log(log_auto_self_check_failure_channel,log_embed)
                print("자가진단 실패 후 메시지 발송 완료...")
                #자가진단 실패시 유저데이터의 failure 값 증가
                if "failure" in user_data[user_id].keys():
                    user_data[user_id]["failure"] += 1
                else:
                    user_data[user_id]["failure"] = 1
            
            with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
                json.dump(user_data,json_file,ensure_ascii = False, indent=4)
                
        #유저 id를 찾지 못하여 discord user 오브젝트를 못 얻었을 경우
        else:
            print("자가 진단 후 메시지 전송 실패...")
            embed = discord.Embed(title="자가 진단 후 메시지 전송 실패",description=f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 에 {user_data[user_id]['name']}(<@{user_id}>) 님의 자가진단이 실시되었습니다만 확인 메시지가 전송되지 않았습니다.\n자가진단결과 : {data['message']}", color=0x62c1cc)
            await send_embed_log(log_auto_self_check_after_send_failure_channel,embed)
    except Exception as ex:
        print(f'에러가 발생 했습니다 {ex}')
        print("자가 진단 후 메시지 전송 실패...")
        try:
            await send_log(log_send_failure,f"<@{user_id}>`{user_data[user_id]['name'][0]}*{user_data[user_id]['name'][-1]}`님의 자가진단 후 메시지 전송 실패\n{data['message']}\n{ex}\n")
        except:
            pass

@bot.command()
async def 명령어(ctx):
    global help_embed
    await ctx.send(embed=help_embed)

@bot.command()
async def 도움말(ctx):
    global help_embed
    await ctx.send(embed=help_embed)

@bot.command()
async def 서버목록(ctx):
    servers = bot.guilds
    await ctx.send(f"현재 {len(servers)}개의 서버에서 실행 중 입니다.")

@bot.command()
async def 서버갱신(ctx):
    kb = koreanbots.Koreanbots(bot, KOR_TOKEN, run_task=True)
    print(f"서버 갱신 완료 : {kb}")
    await ctx.send("https://koreanbots.dev/bots/863013480709750805")

@bot.command()
async def 유저수갱신(ctx):
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)
    game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 중 ")
    await bot.change_presence(status=discord.Status.online, activity=game)
    

@bot.command()
async def 정보등록(ctx,name=None,birth=None,area=None,school_name=None,school_type=None,passward=None):
    if str(ctx.guild) == "None":
        if name!=None and birth!=None and area!=None and school_name!=None and school_type!=None and passward!=None:
            if area not in back_area_list:
                embed = discord.Embed(title="정보 등록 실패", description=f"지역은 아래 항목 중 하나로 입력해주셔야 합니다.\n(입력값 : {area})")
                embed.add_field(name="지역 리스트",value=f"```{area_list}```", inline=False)
                embed.add_field(name="입력 형식",value=f"{PREFIX}정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="입력값",description=f"이름 : {name}\n생년월일 : {birth}\n지역 : {area}\n학교 이름 : {school_name}\n학교 타입 : {school_type}\n비밀번호 : {passward}")
                await ctx.send(embed = embed)
            elif len(passward) != 4 or passward.isdigit()==False:
                embed = discord.Embed(title="정보 등록 실패", description=f"비밀번호는 숫자 4글자의 형태로 입력해주셔야 합니다.\n(입력값 : {passward})")
                embed.add_field(name="입력 형식",value=f"{PREFIX}정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="입력값",description=f"이름 : {name}\n생년월일 : {birth}\n지역 : {area}\n학교 이름 : {school_name}\n학교 타입 : {school_type}\n비밀번호 : {passward}")
                await ctx.send(embed = embed)
            elif len(birth)!=6 or birth.isdigit() == False:
                embed = discord.Embed(title="정보 등록 실패", description=f"생년월일는 숫자 6글자의 형태로 입력해주셔야 합니다.\n(입력값 : {birth})")
                embed.add_field(name="입력 형식",value=f"{PREFIX}정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="입력값",description=f"이름 : {name}\n생년월일 : {birth}\n지역 : {area}\n학교 이름 : {school_name}\n학교 타입 : {school_type}\n비밀번호 : {passward}")
                await ctx.send(embed = embed)
            elif school_type not in back_school_type_list:
                embed = discord.Embed(title="정보 등록 실패", description=f"학교 타입은 아래 항목 중 하나로 입력해주셔야 합니다.\n(입력값 : {school_type})")
                embed.add_field(name="학교 타입 리스트",value=f"```{school_type_list}```", inline=False)
                embed.add_field(name="입력 형식",value=f"{PREFIX}정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", inline=False)
                await ctx.send(embed=embed)
                embed = discord.Embed(title="입력값",description=f"이름 : {name}\n생년월일 : {birth}\n지역 : {area}\n학교 이름 : {school_name}\n학교 타입 : {school_type}\n비밀번호 : {passward}")
                await ctx.send(embed = embed)
            else:
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

                if str(ctx.guild)!="None":
                    embed = discord.Embed(title="정보 등록 완료", description=f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 에 `{ctx.author}` 님의 정보 등록이 완료되었습니다.\n구체적인 등록 정보는 개인DM을 확인해주세요.{end_msg}",color=0x62c1cc)
                    await ctx.send(embed=embed)

                embed = discord.Embed(title="정보 등록 완료", description=f"이름 : [{ctx.author}]\n서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```", color=0x62c1cc)
                #embed.add_field(name="입력값",value=f"```{ctx.message.content}```{end_msg}")
                await send_embed_log(log_add_success_channel,embed)

                user_data[str(ctx.author.id)]["area_code"] = await get_school_data.get_area_code(user_data[str(ctx.author.id)]["area"])
                user_data[str(ctx.author.id)]["school_code"] = await get_school_data.get_school_code(user_data[str(ctx.author.id)]["school_name"],user_data[str(ctx.author.id)]["area_code"])
                
                with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
                    json.dump(user_data,json_file,ensure_ascii = False, indent=4)

                user = await bot.fetch_user(ctx.author.id)
                if user is not None:
                    embed = discord.Embed(title="정보 등록 완료[보안메시지]", description=f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 부로 \`{user_data[str(ctx.author.id)]['name']}` 님의 정보 등록이 완료되었습니다.\n```이름 : {user_data[str(ctx.author.id)]['name']}\n생년월일 : {user_data[str(ctx.author.id)]['birth']}\n지역 : {user_data[str(ctx.author.id)]['area']}\n학교 이름 : {user_data[str(ctx.author.id)]['school_name']}\n학교 타입 : {user_data[str(ctx.author.id)]['school_type']}\n비밀번호 : {user_data[str(ctx.author.id)]['passward'][:2]}**```{end_msg}",color=0x62c1cc)
                    await user.send(embed=embed)
                else:
                    user = await bot.fetch_user(523017072796499968)
                    await user.send("DM 보내기가 정상적으로 처리되지 않아서 관리자에게 로그 DM을 보냈습니다.")
        else:
            embed = discord.Embed(title="정보 등록 실패", description=f"모든 값이 들어오지 않았습니다.\n다시 한번 입력해주시기 바랍니다.\n형식  :  {PREFIX}정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]{end_msg}", color=0x62c1cc)
            await ctx.send(embed = embed)
            embed = discord.Embed(title="입력값",description=f"이름 : {name}\n생년월일 : {birth}\n지역 : {area}\n학교 이름 : {school_name}\n학교 타입 : {school_type}\n비밀번호 : {passward}")
            await ctx.send(embed = embed)
            embed = discord.Embed(title="정보 등록 실패", description=f"아이디 : [{ctx.author}]\n일시 : [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n 서버 : [{ctx.guild}]\n채널 : [{ctx.channel}]\n입력값 : ```{ctx.message.content}```",color=0x62c1cc)
            await send_embed_log(log_add_failure_channel,embed)
    else:
        await ctx.send("개인정보 보호를 위해 봇과 개인메시지로 정보등록을 해주시기 바랍니다.")
    #정보등록 후 상태 메시지 변경 (유저 수 갱신)
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)
    game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 중 ")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def 정보삭제(ctx):
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)

    if user_data.get(str(ctx.author.id)):
        data = user_data.pop(str(ctx.author.id))

        with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
            json.dump(user_data,json_file,ensure_ascii = False, indent=4)
        if str(ctx.guild)!="None":
            embed = discord.Embed(title="정보 삭제 완료", description="[{}] 부로 {} 님의 정보 삭제가 완료되었습니다.\n구체적인 삭제 정보는 개인DM을 확인해주세요.{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data['name'],end_msg), color=0x62c1cc)
            await ctx.send(embed=embed)

        user = await bot.fetch_user(str(ctx.author.id))
        embed = discord.Embed(title="정보 삭제 완료[보안메시지]", description="[{}] 부로 {} 님의 정보 삭제가 완료되었습니다.\n이름 : {}\n생년월일 : {}\n지역 : {}\n학교 이름 : {}\n학교 타입 : {}\n비밀번호 : {}**{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),data['name'],data['name'],data["birth"],data["area"],data["school_name"],data["school_type"],data["passward"][:2],end_msg), color=0x62c1cc)
        await user.send(embed=embed)

        await send_log(log_add_remove,f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {data['name']}님의 정보 삭제 완료!")
        #정보등록 후 상태 메시지 변경 (유저 수 갱신)
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        game = discord.Game(f" {PREFIX}명령어 | {len(user_data.keys())}명의 자가진단을 처리 중 ")
        await bot.change_presence(status=discord.Status.online, activity=game)
    else:
        embed = discord.Embed(title="정보 삭제 실패", description="[{}] 에  <@{}> 님의 정보 삭제를 실패하셨습니다.\n디스코드 아이디[{}]로 등록된 정보가 없습니다.\n구체적인 문의는 관리자[white201#0201]님께 문의 부탁드립니다.".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author.id,ctx.author.id,end_msg), color=0x62c1cc)
        await ctx.send(embed=embed)
    
@bot.command()
async def 정보확인(ctx):
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)

    if user_data.get(str(ctx.author.id)):
        if str(ctx.guild) != "None":
            embed = discord.Embed(title="정보 확인", description=f"개인DM으로 정보를 보냈습니다.{end_msg}", color=0x62c1cc)
            await ctx.send(embed=embed)
        user = await bot.fetch_user(str(ctx.author.id))
        if user is not None:
            embed = discord.Embed(title="정보 확인[보안메시지]", description=f"```이름 : {user_data[str(ctx.author.id)]['name']}\n생년월일 : {user_data[str(ctx.author.id)]['birth']}\n지역 : {user_data[str(ctx.author.id)]['area']}\n학교 이름 : {user_data[str(ctx.author.id)]['school_name']}\n학교 타입 : {user_data[str(ctx.author.id)]['school_type']}\n비밀번호 : {user_data[str(ctx.author.id)]['passward'][:2]}**```\n※정보수정을 원하신다면 `{PREFIX}정보등록`으로 새로 등록해주시기 바랍니다.\n※이미 등록된 데이터가 있어도 새로 등록한 데이터를 기준으로 작동합니다.{end_msg}", color=0x62c1cc)
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
        global JSON_FILE_NAME
        await ctx.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d')}]\nhost name : {host_name}\njson file name : {JSON_FILE_NAME}")
        file = discord.File("user_data.json")
        await ctx.send(file=file)
        file = discord.File("auto_self_check.py")
        await ctx.send(file=file)
    else:
        user = await bot.fetch_user(ctx.author.id)
        await user.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")


@bot.command()
async def 관리자전체자가진단(ctx):
    try:
        if str(ctx.author.id) == '523017072796499968':
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)
            global start_minute
            start_minute=random.randrange(1,16)
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
                    except Exception as ex:
                        print(f"{user_data[i]['name']}:{ex}")
                        user = await bot.fetch_user(523017072796499968)
                        await user.send(f"{user_data[i]['name']}::{ex}")
                        try:
                            data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                        except Exception as ex:
                            print(f"{user_data[i]['name']}:{ex}")
                            user = await bot.fetch_user(523017072796499968)
                            await user.send(f"{user_data[i]['name']}::{ex}")
                            try:
                                data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                            except Exception as ex:
                                print(f"{user_data[i]['name']}:{ex}")
                                user = await bot.fetch_user(523017072796499968)
                                await user.send(f"{user_data[i]['name']}::{ex}")
                                pass

                    await send_DM(data,i,start_minute,user_data)
        else:
            await ctx.send("관리자 권한이 없어 해당 명령어를 사용할 수 없습니다.")
    except Exception as ex:
        print(f"{user_data[i]['name']}:{ex}")
        user = await bot.fetch_user(523017072796499968)
        await user.send(f"{user_data[i]['name']}::{ex}")

@bot.command()
async def 관리자전체공지(ctx,*,msg):
    if str(ctx.author.id) == '523017072796499968':
        global last_notice
        last_notice = []
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        for user_id in user_data.keys():
            try:
                user = await bot.fetch_user(user_id)
                temp_msg = await user.send(msg)
                last_notice.append(temp_msg)
                print(f"{user_id}전송성공")
            except Exception as ex:
                user = await bot.fetch_user(523017072796499968)
                await user.send(f'에러가 발생 했습니다 {ex}')
                print(f'{user_id} : 에러가 발생 했습니다 {ex}')
                print(f"{user_id}님의 공지전송이 실패하였습니다.")

        await ctx.send(f"공지 전송 완료\n`{msg}`")
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
        with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
            user_data=json.load(json_file)
        user=None
        for i in user_data.keys():
            if user_data[i]['name'] == name and user_data[i]["birth"] == birth:
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
    await ctx.send(f"현재 핑은 `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}` 기준으로 `{str(round(bot.latency*1000))}ms` 입니다.")

@bot.command()
async def 급식(ctx, day=None,user: discord.User=None):
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


@bot.command()
async def 내일급식(ctx,user: discord.User=None): 
    day=datetime.datetime.now() + datetime.timedelta(days=1)
    day = day.strftime('%Y%m%d')
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)
    print(day)
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

@bot.command()
async def 어제급식(ctx,user: discord.User=None): 
    day=datetime.datetime.now() - datetime.timedelta(days=1)
    day = day.strftime('%Y%m%d')
    if user==None:
        user = str(ctx.author.id)
    else:
        user = str(user.id)
    print(day)
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

@bot.command()
async def 학년반정보입력(ctx, school_grade:str=None, school_class:str=None):
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

@bot.command()
async def 학교코드(ctx):
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)
    for i in user_data.keys():
        print(user_data[i]['name'])
        user_data[i]["area_code"] = await get_school_data.get_area_code(user_data[i]["area"])
        user_data[i]["school_code"] = await get_school_data.get_school_code(user_data[i]["school_name"],user_data[i]["area_code"])
        print(f"name : {user_data[i]['name']},area_code : {user_data[i]['area_code']}, school_code : {user_data[i]['school_code']}")
    with open(JSON_FILE_NAME, "w",encoding='UTF-8') as json_file:
        json.dump(user_data,json_file,ensure_ascii = False, indent=4)

@bot.command()
async def 시간표(ctx, day=None,user: discord.User=None):
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

@bot.command()
async def 학사일정(ctx, day=None,user: discord.User=None):
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
        await ctx.send("날짜는 숫자로 이루어진 8글자 형식으로 입력해주십시오. (예 : `20210612`)")

@bot.command()
async def 시간(ctx):
    await ctx.send(f"{datetime.datetime.now().strftime('%Y%m%d')}")

@bot.command()
async def 자가진단(ctx):
    await ctx.send(f"수동자가진단은 `{PREFIX}진단참여`을 이용해주시기 바랍니다.")

@bot.command()
async def 진단참여(ctx):
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
        except Exception as ex:
            print("무지성 트라이 1트")
            print(f"{user_data[user_id]['name']}:{ex}")
            user = await bot.fetch_user(523017072796499968)
            await user.send(f"{user_data[user_id]['name']}::{ex}")
            try:
                data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
            except Exception as ex:
                print("무지성 트라이 2트")
                print(f"{user_data[user_id]['name']}:{ex}")
                user = await bot.fetch_user(523017072796499968)
                await user.send(f"{user_data[user_id]['name']}::{ex}")
                try:
                    data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                except Exception as ex:
                    print("무지성 트라이 3트 후 포기")
                    print(f"{user_data[user_id]['name']}:{ex}")
                    user = await bot.fetch_user(523017072796499968)
                    await user.send(f"{user_data[user_id]['name']}::{ex}")
                    data = {}
                    data["code"]="ERROR"
                    data['message']="인증서 에러 또는 기타 에러 (봇 관리자에게 문의해주세요. white201#0201)"
                    pass

        if data["code"]=="SUCCESS":
            await ctx.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 자가진단 완료!")
        else:
            await ctx.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 자가진단 실패!\n{data['message']}")
    else:
        await ctx.send(f"유저 데이터에 등록된 정보가 없습니다. `{PREFIX}정보등록`으로 등록해주십시오.")
        
@bot.command()
async def 자가진단실시(ctx):
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

@bot.command()
async def 자가진단중지(ctx):
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
        
@bot.command()
async def test(ctx):
    await ctx.send("Hello World!")

@bot.command()
async def 코로나(ctx):
    covid19_data = await get_covid19_data.get_covid19_decide()
    await ctx.send(covid19_data)
    with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
        user_data=json.load(json_file)
    with open("area_code.json", "r",encoding="utf-8-sig") as json_file:
        area_code=json.load(json_file)
    
    await ctx.send(f"{area_code[user_data[str(ctx.author.id)]['area_code']]} : {covid19_data[area_code[user_data[str(ctx.author.id)]['area_code']]]}")

bot.run(TOKEN)