import discord

end_msg = "\n\n개발자 : white201#0201 | [개발자 서버](https://discord.gg/bhJEbEgHED) | [초대링크](https://discord.com/oauth2/authorize?client_id=863013480709750805&permissions=2184571456&scope=bot)"

help_embed = discord.Embed(title="명령어", description="자동자가진단 봇에 대한 도움말 입니다. ?명령어 로 확인 가능합니다.\n평일날에만 자가진단이 작동하며, 공휴일 제외 기능을 추가할 예정입니다.",color=0x62c1cc)
help_embed.add_field(name="?정보등록", value="?정보등록 [이름] [생년월일] [지역] [학교이름] [학교타입] [비밀번호]```?정보등록 홍길동 721027 서울시 길동고 고등학교 1234``````?정보등록 홍길동 050201 충청남도 길동중 중학교 2580```※정보등록은 `개인DM`으로 하는 것을 보안상 추천 드립니다.", inline=False)
help_embed.add_field(name="?정보삭제", value="※디스코드 아이디를 기준으로 삭제합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
help_embed.add_field(name="?정보확인", value="※디스코드 아이디를 기준으로 확인합니다.\n※만약 디스코드 계정이 바뀌었을 경우 white201#0201 님께 문의 부탁드립니다.", inline=False)
help_embed.add_field(name="?진단참여", value="수동으로 자가진단을 실시합니다.", inline=False)
help_embed.add_field(name="?자가진단실시", value="중지되었던 자동자가진단을 다시 실시합니다.", inline=False)
help_embed.add_field(name="?자가진단중지", value="이제부터 자동자가진단이 작동되지않습니다.", inline=False)
help_embed.add_field(name="?급식", value="?급식\n?급식 <날짜> <태그>의 형식으로 타인의 급식도 볼 수 있습니다.", inline=False)
help_embed.add_field(name="기타명령어",value="`?학년반정보입력 [반] [번호]`\n`?급식`, `?내일급식`, `?어제급식`\n`?시간표`\n`?학사일정`", inline=False)
help_embed.add_field(name="기타",value="자동자가진단은 7시 00분에서 7시 16분 사이에 랜덤하게 작동하며,\n자동자가진단 DM 메시지를 통하여 그 다음날의 작동 시간을 알 수 있습니다.", inline=False)
help_embed.add_field(name="정보",value=end_msg)