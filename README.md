# 자동자가진단 디스코드 봇

## 설명
아침에 자동으로 자가진단을 해주는 봇 입니다. (NEW자동자가진단)

## 라이센스

본 봇은 모든 코드가 공개되어 있으며, 영리적 사용 및 코드의 수정이 가능하지만, 출처(개발자)를 명확하게 밝혀야 합니다.

코드를 사용하실 경우 `discord : white201#0201`로 통보와 `Github Star` 부탁드립니다.

또한 출력 Embed 하단 개발자 탭은 수정하시면 안됩니다.

## 세팅
### env 세팅
`.env` 파일을 생성해주세요.
그 후 `.env` 파일 내에 아래 형식으로 작성해주세요.
```
TOKEN = 디스코드 봇 토큰
JSON_FILE_NAME = 유저 데이터가 저장될 JSON 파일명 (확장자 포함)
PREFIX = 봇의 명령어 접두사
ADMIN_ID = 봇 관리자의 디스코드 ID
KOR_TOKEN = 한국 디스코드 리스트의 토큰
COVID_API_KEY = 공공데이터 포털 API KEY (시도 확진자 수 API가 활용 신청이 되어있는 KEY)
```

※한디리 토큰에 경우 [한디리](https://koreanbots.dev/bots/)를 이용하지 않으신다면, KOR_TOKEN이 들어가는 모든 코드를 지우셔도 됩니다.

### 파일 생성
`auto_self_check.py` 와 같은 경로에 위 env 세팅에서 `JSON_FILE_NAME`으로 지정한 파일 이름으로 파일을 생성해주세요.

## 기타
### 서포트
[초대링크](https://discord.com/api/oauth2/authorize?client_id=846650618701283359&permissions=2184703040&scope=bot) ,[공식 서포트 서버](https://discord.gg/bhJEbEgHED)
### 모듈
사용 모듈 : [hcskr](https://pypi.org/project/hcskr/), [discord.py](https://pypi.org/project/discord.py/), [asyncio](https://pypi.org/project/asyncio/), [requests](https://pypi.org/project/requests/), [xmltodict](https://pypi.org/project/xmltodict3/) 등