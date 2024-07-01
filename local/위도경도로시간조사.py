# 파이참으로 경도, 위도 불러오기
# 라이브러리 불러오기
import pandas as pd
import numpy as np
import os
import sys
import json

# 시간
import time
from tqdm import tqdm

# url 분석
import urllib.request
import requests
from urllib.parse import quote

df_address = pd.read_csv('교통점수경도위도.csv', encoding = 'utf-8-sig', index_col = 'Unnamed: 0')
df_address['위도'] = df_address['위도'].round(6)
df_address['경도'] = df_address['경도'].round(6)
print(df_address)

# 에러난 곳만 따로 한번 더 조사
start_index = 55
end_index = 136
df_address_error = df_address[start_index:end_index + 1]  # 인덱스는 0부터 시작하므로 end_index에 1을 더해줍니다.

start_index1 = 1
end_index1 = 1
df_address_error1 = df_address[start_index:end_index + 1]  # 인덱스는 0부터 시작하므로 end_index에 1을 더해줍니다.

# Time 데이터프레임 생성
df_time = pd.DataFrame(index=df_address['시청'], columns=df_address['시청'])
print(df_time)

# 카카오 소요시간 검색기
count = 0


sunchun_sichung_destination = '31.819051,127.8733'

origin = "126.852601,35.159545"
time_list = []
for temp3, temp4 in tqdm(zip(df_address['위도'],df_address['경도'])):
    try:
        destination = f"{temp4},{temp3}"

        REST_API_KEY = "your_api_key"


        url = "https://apis-navi.kakaomobility.com/v1/directions"
        params = {
          "origin": origin,
          "destination": destination,
          "waypoints": "",
          "priority": "TIME",
          "car_fuel": "GASOLINE",
          "car_hipass": "false",
          "alternatives": "false",
          "road_details": "false"
        }
        headers = {
          "Authorization": f"KakaoAK {REST_API_KEY}"  # Replace YOUR_REST_API_KEY_HERE with your actual API key
        }

        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        time = data['routes'][0]["summary"]["duration"]
        time_list.append(time)
    except:
        time_list.append(0)

# df_address 안의 위도가 temp1의 값을 갖는 시청값을 가져온다.
# 그 값을 활용하여 df_time 안에 있는 열 을 선택 한 후 그 열에 time_list를 넣는다.
df_time[list(df_address['시청'])[count]] = time_list
df_time.to_csv('교통점수시간만광주.csv', encoding='utf-8-sig')
count +=1
print(df_time)
df_time.to_csv('교통점수시간만_꽁주  최종.csv', encoding = 'utf-8-sig')
