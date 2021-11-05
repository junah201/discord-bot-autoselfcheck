import requests
import xmltodict
import json, os
import asyncio
import datetime
from dotenv import load_dotenv

load_dotenv()
covid19_api_key = os.getenv('COVID_API_KEY')

#코로나 확진자 수집 함수
async def get_covid19_decide():
    day = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d')
    url = f"http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey={covid19_api_key}&pageNo=1&numOfRows=10&startCreateDt={day}&endCreateDt={day}"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    response = requests.get(url,headers=headers)
    try:
        response = requests.get(url,headers=headers)
    except:
        response = requests.get(url,headers=headers,verify=False)
    print(url)
    covid19_data = json.loads(json.dumps(xmltodict.parse(response.text), indent=4))
    return_data = {}
    for each_data in covid19_data['response']['body']['items']['item']:
        return_data[each_data['gubun']] = each_data['incDec']
    with open("covid19_data.json", "w",encoding='UTF-8') as json_file:
        json.dump(return_data,json_file,ensure_ascii = False, indent=4)
    return return_data