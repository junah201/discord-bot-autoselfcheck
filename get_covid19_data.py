import requests
import xmltodict
import json
import asyncio
import datetime

covid19_api_key = "PEk93HmpBu4oPQ7khzVYY8z8f2JCUG9UIOHRrXKJB11j%2BfscZ4AoG%2F7z5pEr5c4BoQ7Ld46hGk2dzWEGS2PEIg%3D%3D"
covid19_api_key = "PEk93HmpBu4oPQ7khzVYY8z8f2JCUG9UIOHRrXKJB11j%2BfscZ4AoG%2F7z5pEr5c4BoQ7Ld46hGk2dzWEGS2PEIg%3D%3D"
seoul_covid19_api_key = "4e7a51565377686938376e73627150"

'''
async def get_covid19_decide():
    day = datetime.datetime.now().strftime('%Y%m%d')
    old_day = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d')
    url = f'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={covid19_api_key}&Type=json&pageNo=1&numOfRows=10&startCreateDt={old_day}&endCreateDt={day}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    print(url)
    response = requests.get(url,headers=headers)
    covid19_data = json.loads(json.dumps(xmltodict.parse(response.text), indent=4))
    if len(covid19_data['response']['body']['items']['item']) == 2:
        return int(covid19_data['response']['body']['items']['item'][0]['decideCnt']) - int(covid19_data['response']['body']['items']['item'][1]['decideCnt'])
    else:
        return None
'''

async def get_covid19_decide():
    day = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime('%Y%m%d')
    url = f"http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey={covid19_api_key}&pageNo=1&numOfRows=10&startCreateDt={day}&endCreateDt={day}"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    response = requests.get(url,headers=headers)
    print(url)
    covid19_data = json.loads(json.dumps(xmltodict.parse(response.text), indent=4))
    return_data = {}
    for each_data in covid19_data['response']['body']['items']['item']:
        return_data[each_data['gubun']] = each_data['incDec']
    with open("covid19_data.json", "w",encoding='UTF-8') as json_file:
        json.dump(return_data,json_file,ensure_ascii = False, indent=4)
    return return_data