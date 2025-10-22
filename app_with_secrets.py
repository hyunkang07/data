import streamlit as st
import requests
from datetime import datetime
import json

# 페이지 설정
st.set_page_config(
    page_title="날씨 정보 앱",
    page_icon="🌤️",
    layout="wide"
)

# API 키 (Streamlit Secrets 사용 - 배포 시 권장)
try:
    API_KEY = st.secrets["API_KEY"]
except:
    # Secrets가 없으면 기본값 사용 (개발 환경)
    API_KEY = "4420348db0f68ca32ed864b0702fd5a0"

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# 날씨 아이콘 매핑
weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️"
}

def get_weather_data(city_name):
    """OpenWeather API를 통해 날씨 데이터를 가져옵니다."""
    try:
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric",  # 섭씨 온도
            "lang": "kr"  # 한국어 설명
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

def display_weather(weather_data):
    """날씨 데이터를 화면에 표시합니다."""
    if weather_data:
        # 기본 정보 추출
        city = weather_data['name']
        country = weather_data['sys']['country']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description']
        weather_main = weather_data['weather'][0]['main']
        icon = weather_icons.get(weather_main, "🌍")
        
        # 날씨 정보 표시
        st.markdown(f"# {icon} {city}, {country}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🌡️ 현재 온도",
                value=f"{temp}°C",
                delta=f"체감 {feels_like}°C"
            )
        
        with col2:
            st.metric(
                label="💧 습도",
                value=f"{humidity}%"
            )
        
        with col3:
            st.metric(
                label="💨 풍속",
                value=f"{wind_speed} m/s"
            )
        
        # 추가 정보
        st.markdown("---")
        col4, col5 = st.columns(2)
        
        with col4:
            st.info(f"**날씨 상태:** {description.capitalize()}")
        
        with col5:
            st.info(f"**기압:** {pressure} hPa")
        
        # 상세 정보 (접을 수 있는 형태)
        with st.expander("📊 상세 정보 보기"):
            st.json(weather_data)

def main():
    """메인 애플리케이션"""
    
    # 타이틀
    st.title("🌤️ 실시간 날씨 정보")
    st.markdown("### OpenWeather API를 활용한 날씨 검색")
    
    # 사이드바
    with st.sidebar:
        st.header("🔍 검색 설정")
        st.markdown("---")
        
        # 도시 입력
        city_input = st.text_input(
            "도시 이름을 입력하세요",
            placeholder="예: Seoul, Tokyo, New York",
            help="영문 도시명을 입력하세요"
        )
        
        # 인기 도시 빠른 선택
        st.markdown("#### 🌍 인기 도시")
        quick_cities = ["Seoul", "Tokyo", "New York", "London", "Paris", "Sydney"]
        
        cols = st.columns(2)
        for idx, city in enumerate(quick_cities):
            with cols[idx % 2]:
                if st.button(city, use_container_width=True):
                    city_input = city
        
        st.markdown("---")
        st.markdown("**ℹ️ 정보**")
        st.markdown("""
        - 실시간 날씨 데이터
        - 전 세계 도시 검색 가능
        - 온도는 섭씨(°C) 기준
        """)
    
    # 메인 컨텐츠
    if city_input:
        with st.spinner(f"{city_input}의 날씨를 가져오는 중..."):
            weather_data = get_weather_data(city_input)
            
            if weather_data and weather_data.get('cod') != '404':
                display_weather(weather_data)
            else:
                st.error("❌ 도시를 찾을 수 없습니다. 도시 이름을 확인해주세요.")
    else:
        # 안내 메시지
        st.info("👈 왼쪽 사이드바에서 도시를 선택하거나 입력하세요!")
        
        # 예시 이미지나 설명
        st.markdown("""
        ### 사용 방법
        1. 왼쪽 사이드바에서 도시 이름을 입력하거나
        2. 인기 도시 버튼을 클릭하세요
        3. 실시간 날씨 정보가 표시됩니다!
        
        ### 제공되는 정보
        - 🌡️ 현재 온도 및 체감 온도
        - 💧 습도
        - 💨 풍속
        - 🌤️ 날씨 상태
        - 📊 기압 및 상세 정보
        """)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <small>Powered by OpenWeather API | Made with Streamlit ❤️</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

