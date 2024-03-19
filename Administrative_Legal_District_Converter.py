import pandas as pd
import requests
import os
import json

# Kakao Maps API 키
with open('kakao_api_key.json') as f:
    secrets = json.loads(f.read())
    
kakao_api_key = secrets['kakao_api_key']

# Kakao Maps API 호출 함수
def get_admin_dong(address,row_number):
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={address}'
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
        if 'documents' in result and result['documents']:
            region_3depth_h_name = result['documents'][0]['address']['region_3depth_h_name']    
            return region_3depth_h_name
        else:
            print(f"{row_number}번행 {address} : 주소 정보를 찾을 수 없습니다.")
            return None
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

def remove_specific_string(value, specific_string):
    return value.replace(specific_string, '')

# 엑셀 파일 읽기
print("엑셀 파일을 실행 파일과 동일한 경로에 놔주세요.")
excel_file_path = input("읽어야 할 엑셀 파일 이름를 입력하세요: ")
df = pd.read_excel(excel_file_path)
df_slice = df

# 출력 파일 이름
output_file_path = os.path.join(os.path.dirname(excel_file_path), "output_file.xlsx")

df['법정동'] = df['법정동'].apply(remove_specific_string, specific_string='외 1필지')

df['행정동'] = df.apply(lambda row: get_admin_dong(row['법정동'], row.name), axis=1)

# 결과를 엑셀 파일로 저장
df.to_excel(output_file_path, index=False)

print(f"작업이 완료되었습니다. 결과는 {output_file_path}에 저장되었습니다.")

# 실행이 완료되면 입력 대기
input("엔터 키를 누르면 종료됩니다.")