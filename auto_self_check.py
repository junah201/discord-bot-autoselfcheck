Skip to content
Search or jump to…

Pull requests
Issues
Marketplace
Explore
 
@white-201 
white-201
/
discord-bot-autoselfcheck
1
10
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
discord-bot-autoselfcheck
/
auto_self_check.py
in
main
 

Spaces

4

No wrap
1
#-*- coding: UTF8-*-
2
​
3
import discord
4
from discord.ext import commands, tasks
5
import time, datetime
6
import hcskr
7
import random
8
import json
9
import os, sys
10
import socket
11
import asyncio
12
import school_data
13
​
14
host_name = socket.gethostbyaddr(socket.gethostname())[0]
15
​
16
bot = commands.Bot(command_prefix='?')
17
#KST = datetime.timezone(datetime.timedelta(hours=9))
18
​
19
start_minute=13
20
last_day = "2021-05-29"
21
#start_minute=datetime.datetime.now().minute
22
​
23
end_msg = "\n\n개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=8&scope=bot)"
24
#end_msg = "\n\n봇 : 자동자가진단#4767 | 개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359?permissions=0?scope=bot)"
25
​
26
last_notice = []
27
last_personal_notice = ""
28
​
29
log_add_success_channel = "847490299638186054"
30
log_add_failure_channel = "847731541915467797"
31
log_bot_start_channel = "847732651912593439"
32
log_auto_self_check_failure_channel = "847793169683972146"
33
log_auto_self_check_success_channel = "847775280650518568"
34
log_auto_self_check_after_send_failure_channel ="847738621972578315"
35
log_json_backup_channel = "847830055916404766"
36
log_server_join = "848948171408539678"
37
log_server_remove = "848950238059560990"
38
log_today = "852145484239732756"
39
​
40
area_list = ['서울시','부산시','대구시','인천시','광주시','대전시','울산시','세종시','경기도','강원도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주도','제주특별자치도']
41
back_area_list = ['서울', '서울시', '서울교육청', '서울시교육청', '서울특별시','부산', '부산광역시', '부산시', '부산교육청', '부산광역시교육청','대구', '대구광역시', '대구시', '대구교육청', '대구광역시교육청','인천', '인천광역시', '인천시', '인천교육청', '인천광역시교육청','광주', '광주광역시', '광주시', '광주교육청', '광주광역시교육청','대전', '대전광역시', '대전시', '대전교육청', '대전광역시교육청','울산', '울산광역시', '울산시', '울산교육청', '울산광역시교육청','세종', '세종특별시', '세종시', '세종교육청', '세종특별자치시', '세종특별자치시교육청','경기', '경기도', '경기교육청', '경기도교육청','강원', '강원도', '강원교육청', '강원도교육청','충북', '충청북도', '충북교육청', '충청북도교육청','충남', '충청남도', '충남교육청', '충청남도교육청','전북', '전라북도', '전북교육청', '전라북도교육청','전남', '전라남도', '전남교육청', '전라남도교육청','경북', '경상북도', '경북교육청', '경상북도교육청','경남', '경상남도', '경남교육청', '경상남도교육청','제주', '제주도', '제주특별자치시', '제주교육청', '제주도교육청', '제주특별자치시교육청', '제주특별자치도']
42
back_school_type_list = ['유치원', '유','유치','초등학교', '초','초등','중학교', '중','중등','고등학교', '고','고등','특수학교', '특','특수','특별']
43
school_type_list = ['유치원', '초등학교','중학교', '고등학교','특수학교']
44
​
45
@tasks.loop(seconds=60)
@white-201
Commit changes
Commit summary
Create auto_self_check.py
Optional extended description
Add an optional extended description…
 Commit directly to the main branch.
 Create a new branch for this commit and start a pull request. Learn more about pull requests.
 
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
