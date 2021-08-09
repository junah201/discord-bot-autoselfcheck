import requests
import xmltodict
import json
import asyncio
import datetime

covid19_api_key = "PEk93HmpBu4oPQ7khzVYY8z8f2JCUG9UIOHRrXKJB11j%2BfscZ4AoG%2F7z5pEr5c4BoQ7Ld46hGk2dzWEGS2PEIg%3D%3D"

def get_covid19_decide():
    day = datetime.datetime.now().strftime('%Y%m%d')
    print(day)
    print(datetime.datetime.now()-datetime.timedelta(days=1))
    url = f'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey={covid19_api_key}&Type=json&pageNo=1&numOfRows=10&startCreateDt={datetime.datetime.now()-datetime.timedelta(days=1)}&endCreateDt={datetime.datetime.now().day}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    print(url)
    response = requests.get(url,headers=headers)
    json_type = json.dumps(xmltodict.parse(response.text))
    #print(json_type)

def main():
    get_covid19_decide()

main()

