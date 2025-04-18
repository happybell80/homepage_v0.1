import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
from io import BytesIO
import base64
from kosis_api import get_kosis_data

def catenary(x, a, b, c):
    return a * np.cosh((x - b) / a) + c

def analyze_and_plot(stat_code, item_code, freq, start_date, end_date, save_to_db_func):
    # 데이터 가져오기
    df = get_kosis_data(stat_code, item_code, freq, start_date, end_date)
    
    # 데이터 준비
    df = df.sort_values('TIME')
    x_data = np.arange(len(df))
    y_data = df['DATA_VALUE'].values

    # 초기 추정값 설정 (a, b, c)
    initial_guess = (1, len(df) / 2, np.mean(y_data))

    # 곡선 피팅
    popt, pcov = curve_fit(catenary, x_data, y_data, p0=initial_guess, maxfev=10000)

    # 피팅된 곡선 값 계산
    x_fit = np.linspace(0, len(df) - 1, 1000)
    y_fit = catenary(x_fit, *popt)

    # Seaborn 스타일 설정
    sns.set(style="whitegrid")

    # 결과 시각화
    plt.figure(figsize=(12, 8))
    plt.plot(df['TIME'], y_data, 'b-', label='Original Data', linewidth=2)
    plt.plot(df['TIME'].iloc[x_fit.astype(int)], y_fit, 'r--', label='Catenary Fit', linewidth=2)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Value', fontsize=14)
    plt.legend(fontsize=12)
    plt.title('Catenary Trend Line', fontsize=16)
    plt.grid(True)

    # 그래프를 이미지로 저장
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()

    # 차이 계산
    df['APROX'] = catenary(x_data, *popt)
    df['DIFF'] = df['DATA_VALUE'] - df['APROX']

    # 차이 그래프 생성
    plt.figure(figsize=(12, 8))
    plt.plot(df['TIME'], df['DIFF'], 'b-', label='Difference', linewidth=2)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Difference', fontsize=14)
    plt.legend(fontsize=12)
    plt.title('Difference Line', fontsize=16)
    plt.grid(True)

    # 차이 그래프를 이미지로 저장
    diff_img_buffer = BytesIO()
    plt.savefig(diff_img_buffer, format='png')
    diff_img_buffer.seek(0)
    diff_img_str = base64.b64encode(diff_img_buffer.getvalue()).decode()
    plt.close()

    # 이미지를 데이터베이스에 저장
    save_to_db_func('catenary_trend.png', img_str)
    save_to_db_func('difference_line.png', diff_img_str)

    return {
        'catenary_params': popt.tolist(),
        'covariance_matrix': pcov.tolist(),
        'catenary_trend_image': img_str,
        'difference_line_image': diff_img_str
    }

# 데이터베이스에 이미지를 저장하는 함수 (실제 구현은 데이터베이스에 따라 다를 수 있음)
def save_image_to_db(filename, img_str):
    # 여기에 데이터베이스에 이미지를 저장하는 코드를 구현하세요
    pass

# 사용 예시
if __name__ == "__main__":
    # 소비자물가지수 데이터 분석
    results = analyze_and_plot("021Y126", "0", "M", "201001", "202312", save_image_to_db)
    print("Analysis complete. Results:", results)