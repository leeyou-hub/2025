import streamlit as st
import requests
import datetime

# ---------------------
# 설정
# ---------------------
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # 👉 여기에 본인 API 키 입력
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ---------------------
# 날씨 데이터 가져오기 함수
# ---------------------
def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "kr"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# ---------------------
# Streamlit UI
# ---------------------
st.title("🌦️ 날씨 대시보드")
st.markdown("도시를 입력하면 현재 날씨를 보여줍니다.")

city = st.text_input("도시 이름 입력 (예: Seoul, Tokyo, New York)", "Seoul")

if st.button("날씨 조회"):
    data = get_weather(city)
    if data:
        st.subheader(f"{city} 날씨 정보")
        st.write(f"**날씨:** {data['weather'][0]['description']}")
        st.write(f"**기온:** {data['main']['temp']} °C")
        st.write(f"**체감온도:** {data['main']['feels_like']} °C")
        st.write(f"**습도:** {data['main']['humidity']} %")
        st.write(f"**풍속:** {data['wind']['speed']} m/s")

        # 간단한 차트 (기온 vs 체감온도)
        temps = [data['main']['temp'], data['main']['feels_like']]
        labels = ["기온", "체감온도"]

        fig, ax = plt.subplots()
        ax.bar(labels, temps)
        ax.set_ylabel("°C")
        ax.set_title("기온 비교")
        st.pyplot(fig)
    else:
        st.error("날씨 데이터를 가져올 수 없습니다. 도시 이름을 확인하세요.")

