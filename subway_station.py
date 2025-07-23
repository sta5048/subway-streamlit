# 🚨 1. 한글 폰트 설정 먼저
from set_korean_font import setup_korean_font
setup_korean_font()

# 📦 2. 라이브러리 임포트
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 📂 3. CSV 경로
csv_path = "혼잡도_통계_요약 (1).csv"

# 📌 4. 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(csv_path, encoding="cp949")
    df["월"] = df["월"].astype(str).str.replace("월", "")
    df["월"] = df["월"].astype(int)
    df["역명"] = df["역명"].astype(str).str.strip()
    df["주말여부"] = df["요일"].apply(lambda x: "주말" if x in ["토요일", "일요일"] else "평일")
    return df

df = load_data()

# 🎛️ 5. UI 구성
selected_month = st.selectbox("📅 월 선택", sorted(df["월"].unique()))
filtered_stations = sorted(df[df["월"] == selected_month]["역명"].unique())
selected_station = st.selectbox("🚉 역 선택", filtered_stations)
selected_weektype = st.radio("📌 평일/주말 선택", ["평일", "주말"], horizontal=True, key="weekday_radio")
filtered_hours = sorted(
    df[
        (df["월"] == selected_month) &
        (df["역명"] == selected_station) &
        (df["주말여부"] == selected_weektype)
    ]["시간대"].unique()
)
selected_hour = st.selectbox("⏰ 시간대 선택", filtered_hours)

# 📊 6. 해당 데이터 추출
row = df[
    (df["월"] == selected_month) &
    (df["역명"] == selected_station) &
    (df["시간대"] == selected_hour) &
    (df["주말여부"] == selected_weektype)
]

if row.empty:
    st.warning("데이터가 존재하지 않습니다.")
else:
    mean = row["mean"].values[0]
    std = row["std"].values[0]
    ci_lower = mean - 1.96 * std
    ci_upper = mean + 1.96 * std

    # X 범위 고정 (0부터 시작)
    x_min = 0
    x_max = max(mean + 4 * std, 100)
    x = np.linspace(x_min, x_max, 1000)
    y = norm.pdf(x, loc=mean, scale=std)

    # 📈 7. 그래프 출력
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="red", label="정규분포 곡선")
    ax.axvline(mean, color="green", linestyle="-", label="📌 평균")
    ax.axvline(ci_lower, color="blue", linestyle="--", label="🔵 95% 신뢰구간")
    ax.axvline(ci_upper, color="blue", linestyle="--")
    ax.fill_between(x, y, where=(x >= ci_lower) & (x <= ci_upper), color='blue', alpha=0.3)
    ax.set_title(f"📊 {selected_month}월 {selected_station}역 {selected_hour} ({selected_weektype})")
    ax.set_xlabel("이용 승객 수")
    ax.set_ylabel("확률 밀도")
    ax.grid(False)
    ax.legend(loc="upper right")

    # 📤 출력
    st.pyplot(fig)
    col1, col2 = st.columns(2)
    col1.metric(label="📌 평균 이용 승객 수", value=f"{mean:.2f}")
    col2.metric(label="📌 표준편차", value=f"{std:.2f}")
