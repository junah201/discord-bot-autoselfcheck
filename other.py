from logging import error
import discord
import json,datetime
from channels.log_channels import *
from embed.help_embed import *
from variable import *

async def user_data_backup(bot):
    try:
        channel = bot.get_channel(int(log_json_backup_channel))
        if channel == None:
            channel = await bot.fetch_channel(int(log_json_backup_channel))
        print(f"channel {channel}")
        await channel.send(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        file = discord.File("user_data.json")
        await channel.send(file=file)
        file = discord.File("main.py")
        await channel.send(file=file)
    except Exception as ex:
        print(f"user_data_backup 실패 : {ex}")

async def send_embed_log(bot,channel,embed):
    try:
        channel = bot.get_channel(int(channel))
        if channel == None:
            channel = await bot.fetch_channel(int(channel))
        await channel.send(embed=embed)
    except Exception as ex:
        print(f"send_embed_log 실패 : {ex}")

async def send_log(bot,channel,msg):
    try:
        channel = bot.get_channel(int(channel))
        if channel == None:
            channel = await bot.fetch_channel(int(channel))
        await channel.send(msg)
    except Exception as ex:
        print(f"send_log 실패 : {ex}")

async def send_DM(bot,data,user_id,user_data):
    print("자가진단 실행 후 메시지 준비 중...")
    try:
        #user는 메시지 전송용 discord.user 오브젝트
        user = await bot.fetch_user(int(user_id))
        erorr = "not erorr"
    except:
        erorr = "erorr"
    
    print(f"send_dm user : {user}")
    print(erorr)
    
    with open("area_code.json", "r",encoding="utf-8-sig") as json_file:
        area_code=json.load(json_file)
    try:
        #유저 id를 찾지 못하여 discord user 오브젝트를 못 얻었을 경우
        if erorr == "erorr":
            print("자가 진단 후 메시지 전송 실패...")
            embed = discord.Embed(title="자가 진단 후 메시지 전송 실패",description=f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 에 {user_data[user_id]['name']}(<@{user_id}>) 님의 자가진단이 실시되었습니다만 확인 메시지가 전송되지 않았습니다.\n자가진단결과 : {data['message']}", color=0x62c1cc)
            await send_embed_log(log_auto_self_check_after_send_failure_channel,embed)
            return
        #자가진단을 실패하였을 경우
        if data.get("code") != "SUCCESS":
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
            return

        #정상 작동
        user_data[user_id]["failure"] = 0
        embed = discord.Embed(title="자가 진단 완료", description=f"일시 : `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n<:greencheck:847787187192725516>성공적으로 `{user_data[user_id]['name']}`님의 자가진단을 수행하였습니다.", color=0x62c1cc)
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
        print("자가진단 성공 후 메시지 발송 완료...")
        #최종 전송 및 로그 전송
        await user.send(embed=embed)
        await send_log(bot,log_auto_self_check_success_channel,"[{}]`{}`님의 자가진단 완료".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),user_data[user_id]['name']))
        print("자가진단 성공 후 메시지 발송 완료...")

    except Exception as ex:
        print(f'에러가 발생 했습니다 {ex}')
        print("자가 진단 후 메시지 전송 실패...")
        try:
            await send_log(log_send_failure,f"<@{user_id}>`{user_data[user_id]['name'][0]}*{user_data[user_id]['name'][-1]}`님의 자가진단 후 메시지 전송 실패\n{data['message']}\n{ex}\n")
        except:
            pass