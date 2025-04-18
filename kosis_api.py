import requests
import pandas as pd
from io import StringIO

def get_kosis_data(stat_code, item_code, freq, start_date, end_date):
    url = "https://ecos.bok.or.kr/api/StatisticSearch/[YOUR_API_KEY]/json/kr/1/100000/"
    url += f"{stat_code}/{freq}/{start_date}/{end_date}/{item_code}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'StatisticSearch' in data and 'row' in data['StatisticSearch']:
        df = pd.DataFrame(data['StatisticSearch']['row'])
        df['TIME'] = pd.to_datetime(df['TIME'], format='%Y%m')
        df['DATA_VALUE'] = df['DATA_VALUE'].astype(float)
        return df
    else:
        raise ValueError("Failed to fetch data from KOSIS API")

if __name__ == "__main__":
    # 예시: 소비자물가지수 데이터 가져오기
    df = get_kosis_data("021Y126", "0", "M", "201001", "202312")
    print(df.head())