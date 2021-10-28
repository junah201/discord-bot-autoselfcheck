import nextcord as discord
from nextcord.ext import commands,tasks

from variable import *
from channels.log_channels import *

import json,hcskr,datetime

import other
import get_school_data, get_covid19_data

import time

class task(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task.start()

    @tasks.loop(seconds=60)
    async def task(self):
        print(f"[{datetime.datetime.now()}] 무한루프가 돌아가는 중...")
        #자가진단 실행 if문
        #if True:
        if datetime.datetime.now().hour==7 and datetime.datetime.now().minute==4 and datetime.datetime.today().weekday()<5:
            print("실행")
            print(1)
            await other.user_data_backup(self.bot)
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)

            success_user = 0
            failure_user = 0
            passed_user = 0
            count = 0

            for user_id in user_data.keys():
                count+=1
                if count%250==0:
                    user = await self.bot.fetch_user(int(ADMIN_ID))
                    await user.send(f"{count} 완료")
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
                        err = False
                    except:
                        err = True

                    if err == True or "Cannot connect to host hcs.eduro.go.kr:443 ssl:True" in data['message']:
                        print("인증서 에러")
                        i=0
                        while True:
                            print(f"무지성 트라이 {i+1}트 : {user_data[user_id]['name']}")
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
                            print(f"학생 검색 오류인지 테스트 중 {i+1}트 : {user_data[user_id]['name']}")
                            try:
                                data = await hcskr.asyncSelfCheck(name,birth,area,school_name,school_type,passward)
                            except:
                                pass
                            if data['message'] == "성공적으로 자가진단을 수행하였습니다.":
                                print(data)
                                break
                    
                    await other.send_DM(self.bot,data,user_id,user_data)                         

                    if data["code"]=="SUCCESS":
                        success_user += 1
                    else:
                        failure_user += 1
                else:
                    passed_user += 1

            print("완료")
            #채널
            with open(JSON_FILE_NAME, "r",encoding="utf-8-sig") as json_file:
                user_data=json.load(json_file)
            embed = discord.Embed(title=f"{datetime.datetime.now().strftime('%Y년 %m월 %d일')}", description=f"```=====================\n서버 : {len(self.bot.guilds)}\n전체 : {len(user_data.keys())}\n실시 : {success_user+failure_user}\n성공 : {success_user}\n실패 : {failure_user}\n패스 : {passed_user}```")
            await other.send_embed_log(self.bot,log_today,embed)

        #정보 수집 if문
        if False:
        #if datetime.datetime.now().hour == 6 and datetime.datetime.now().minute == 0:
            print("===정보 수집 시작===")
            start = time.time()
            await other.user_data_backup(self.bot)
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
                        print(user_data[user_id]["schedule"])
                        if "방학" in str(user_data[user_id]["schedule"]):
                            #user_data[user_id]["possible"] = False
                            #user = await self.bot.fetch_user(int(user_id))
                            #await user.send(f"오늘부터 자가진단이 실시되지 않을 예정입니다.\n(사유 : 학사일정에 방학식이 확인됨)")
                            pass
                        elif "개학" in str(user_data[user_id]["schedule"]):
                            user_data[user_id]["possible"] = True
                            user = await self.bot.fetch_user(int(user_id))
                            await user.send(f"오늘부터 자가진단이 실시될 예정입니다.\n(사유 : 학사일정에 개학식이 확인됨)")
                    except Exception as ex:
                        print(f"{user_data[user_id]['name']} : 학사일정 : {ex}")

                    try:    
                        #급식정보 수집
                        user_data[user_id]["cafeteria"] = await get_school_data.get_school_cafeteria(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'))
                    except Exception as ex:
                        print(f"{user_data[user_id]['name']} : 급식 : {ex}")
                        user = await self.bot.fetch_user(int(ADMIN_ID))
                        await user.send(f"급식 데이터 수집 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")

                    try:
                        #시간표 정보 수집 전 학년 반 정보가 입력되었는지 확인
                        if "school_grade" in user_data[user_id].keys() and "school_class" in user_data[user_id].keys():
                            user_data[user_id]["timetable"] = await get_school_data.get_school_timetable(user_data[user_id]["school_code"],user_data[user_id]["area_code"],datetime.datetime.now().strftime('%Y%m%d'),user_data[user_id]["school_type"],user_data[user_id]["school_grade"],user_data[user_id]["school_class"])
                        else:
                            user_data[user_id]["timetable"] = "No information entered"
                    except Exception as ex:
                        print(f"{user_data[user_id]['name']} : 시간표 : {ex}")
                        user = await self.bot.fetch_user(int(ADMIN_ID))
                        await user.send(f"시간표 데이터 수집 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")

                    try:
                        #전체 코로나 정보에서 해당 지역의 코로나 정보만 수집
                        print(covid19_data)
                        user_data[user_id]['area_covid19_decide'] = covid19_data[area_code[user_data[user_id]["area_code"]]]
                        user_data[user_id]['all_covid19_decide'] = covid19_data['합계']
                    except Exception as ex:
                        user = await self.bot.fetch_user(int(ADMIN_ID))
                        await user.send(f"지역 코로나 데이터 수집 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")
                    
                    try:
                        #failure의 값이 5 이상이면 정보 삭제
                        if "failure" in user_data[user_id].keys():
                            if user_data[user_id]["failure"] >= 5:
                                user_data[user_id]['possible'] = False
                                user = await self.bot.fetch_user(int(user_id))
                                await user.send(f'5회 이상 자가진단에 실패하여, 자동자가진단이 중지 상태로 변경되었습니다.')
                    except Exception as ex:
                        user = await self.bot.fetch_user(int(ADMIN_ID))
                        await user.send(f"failure 측정 중 에러가 발생 했습니다 {ex} | {user_id} | {user_data[user_id]['name']}")

                    with open(JSON_FILE_NAME, "w",encoding="utf-8-sig") as json_file:
                        json.dump(user_data,json_file,ensure_ascii = False, indent=4)

            print("===정보 수집 완료===")
            end = time.time()
            sec = (end - start)
            result = datetime.timedelta(seconds=sec)
            print(result)
            result_list = str(datetime.timedelta(seconds=sec)).split(".")
            print(result_list[0])
def setup(bot):
    bot.add_cog(task(bot))