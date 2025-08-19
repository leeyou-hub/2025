import streamlit as st
import requests
import pandas as pd

# -------------------------------------------------
# 페이지 설정
# -------------------------------------------------
st.set_page_config(page_title="🌦️ 날씨 대시보드", page_icon="🌦️", layout="wide")

# -------------------------------------------------
# Open-Meteo (API 키 불필요)
# -------------------------------------------------
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# WMO 날씨 코드 → 간단 설명/이모지 매핑
WMO_MAP = {
    0: "맑음 ☀️", 1: "대체로 맑음 🌤️", 2: "부분적으로 흐림 ⛅", 3: "흐림 ☁️",
    45: "안개 🌫️", 48: "착빙 안개 🌫️",
    51: "이슬비(약) 🌧️", 53: "이슬비(중) 🌧️", 55: "이슬비(강) 🌧️",
    56: "어는 이슬비(약) 🌧️", 57: "어는 이슬비(강) 🌧️",
    61: "비(약) 🌦️", 63: "비(중) 🌧️", 65: "비(강) 🌧️",
    66: "어는 비(약) 🌧️", 67: "어는 비(강) 🌧️",
    71: "눈(약) ❄️", 73: "눈(중) ❄️", 75: "눈(강) ❄️", 77: "싸락눈 ❄️",
    80: "소나기(약) 🌧️", 81: "소나기(중) 🌧️", 82: "소나기(강) 🌧️",
    85: "소나기 눈(약) 🌨️", 86: "소나기 눈(강) 🌨️",
    95: "뇌우 ⛈️", 96: "뇌우(약한 우박) ⛈️", 99: "뇌우(강한 우박) ⛈️"
}

@st.cache_data(ttl=1800)
def geocode_city(name: str, count: int = 5):
    params = {"name": name, "count": count, "language": "ko", "format": "json"}
    r = requests.get(GEOCODE_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data.get("results", [])

@st.cache_data(ttl=600)
def fetch_forecast(lat: float, lon: float, days: int = 7, tz: str = "auto"):
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": tz,
        # 현재값
        "current": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "wind_speed_10m",
            "weather_code"
        ]),
        # 일별 (가장 호환성 좋은 변수만 선택)
        "daily": ",".join([
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum"
        ]),
        "forecast_days": days,
        "past_days": 0,
        "temperature_unit": "celsius",
        "wind_speed_unit": "ms",
        "precipitation_unit": "mm",
    }
    r = requests.get(FORECAST_URL, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("🌦️ 날씨 대시보드 (API 키 불필요)")
st.caption("Open-Meteo 기반: 도시명 → 좌표 변환 후 현재 날씨 + 일별 예보")

col_left, col_right = st.columns([2, 1])
with col_left:
    city = st.text_input("도시 이름 입력 (예: Seoul, Tokyo, New York)", "Seoul")
with col_right:
    days = st.slider("예보 일수", min_value=3, max_value=14, value=7)

if st.button("날씨 조회", type="primary"):
    try:
        # 1) 지오코딩
        candidates = geocode_city(city)
        if not candidates:
            st.error("도시를 찾을 수 없습니다. 다른 이름으로 시도해 주세요.")
            st.stop()

        options = {f"{c['name']}, {c.get('country_code','')} (lat {c['latitude']:.2f}, lon {c['longitude']:.2f})": c for c in candidates}
        selected_label = st.selectbox("검색된 위치 선택", list(options.keys()))
        selected = options[selected_label]
        lat, lon = selected["latitude"], selected["longitude"]

        # 2) 예보 조회
        data = fetch_forecast(lat, lon, days=days)

        # 현재 날씨 카드
        current = data.get("current", {})
        wcode = int(current.get("weather_code", 0))
        desc = WMO_MAP.get(wcode, f"코드 {wcode}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("현재 기온", f"{current.get('temperature_2m', '—')} °C")
        c2.metric("체감 온도", f"{current.get('apparent_temperature', '—')} °C")
        c3.metric("습도", f"{current.get('relative_humidity_2m', '—')} %")
        c4.metric("풍속", f"{current.get('wind_speed_10m', '—')} m/s")
        st.info(f"현재 상태: {desc}")

        # 3) 일별 요약 (강건성 개선)
        daily = data.get("daily")
        if not daily:
            st.warning("이 위치에 대한 일별 데이터가 제공되지 않았습니다. 모델 변경 또는 일수 조정을 시도해 보세요.")
        else:
            df_d = pd.DataFrame(daily)
            # 필수 컬럼 확인
            required = ["time", "temperature_2m_max", "temperature_2m_min"]
            missing = [c for c in required if c not in df_d.columns]
            if missing:
                st.warning(f"일별 요약에 필요한 컬럼이 없습니다: {', '.join(missing)}")
                st.dataframe(df_d)
            else:
                # 문자열로 처리하여 렌더링 문제 방지
                df_d["date"] = pd.to_datetime(df_d["time"]).dt.strftime("%Y-%m-%d")
                st.subheader("일별 요약")

                # 최고/최저 기온
                fig3, ax3 = plt.subplots()
                ax3.plot(df_d["date"], df_d["temperature_2m_max"], marker="o", label="최고")
                ax3.plot(df_d["date"], df_d["temperature_2m_min"], marker="o", label="최저")
                ax3.set_title("일별 최고/최저 기온")
                ax3.set_xlabel("날짜")
                ax3.set_ylabel("°C")
                ax3.legend()
                ax3.grid(True, linestyle=":", linewidth=0.5)
                st.pyplot(fig3, use_container_width=True)

                # 강수량 합계(있을 때만)
                if "precipitation_sum" in df_d.columns:
                    fig4, ax4 = plt.subplots()
                    ax4.bar(df_d["date"], df_d["precipitation_sum"])
                    ax4.set_title("일별 강수량 합계")
                    ax4.set_xlabel("날짜")
                    ax4.set_ylabel("mm")
                    st.pyplot(fig4, use_container_width=True)

                # 표로도 제공
                show_cols = [c for c in ["date", "temperature_2m_max", "temperature_2m_min", "precipitation_sum"] if c in df_d.columns]
                st.dataframe(df_d[show_cols].rename(columns={
                    "date": "날짜",
                    "temperature_2m_max": "최고(°C)",
                    "temperature_2m_min": "최저(°C)",
                    "precipitation_sum": "강수량(mm)"
                }))

        st.success("데이터 갱신 완료 ✅ (Open-Meteo)")

    except requests.HTTPError as http_err:
        try:
            detail = http_err.response.json()
        except Exception:
            detail = http_err.response.text if hasattr(http_err, 'response') and http_err.response is not None else str(http_err)
        st.error(f"HTTP 오류: {detail}")
    except requests.Timeout:
        st.error("요청이 시간 초과되었습니다. 네트워크 상태를 확인해 주세요.")
    except Exception as e:
        st.error(f"예상치 못한 오류: {e}")
