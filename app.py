import streamlit as st
import requests
from datetime import datetime
import json
from collections import defaultdict

# 페이지 설정
st.set_page_config(
    page_title="날씨 정보 앱",
    page_icon="🌤️",
    layout="wide"
)

# API 키
API_KEY = "4420348db0f68ca32ed864b0702fd5a0"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

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
    """OpenWeather API를 통해 현재 날씨 데이터를 가져옵니다."""
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

def get_forecast_data(city_name):
    """OpenWeather API를 통해 5일 일기예보 데이터를 가져옵니다."""
    try:
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric",
            "lang": "kr"
        }
        response = requests.get(FORECAST_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None

def process_forecast_data(forecast_data):
    """5일 예보 데이터를 날짜별로 집계합니다."""
    if not forecast_data or 'list' not in forecast_data:
        return None
    
    daily_data = defaultdict(lambda: {
        'temps': [],
        'humidity': [],
        'weather': [],
        'wind_speed': [],
        'date': None
    })
    
    for item in forecast_data['list']:
        # 날짜 추출 (YYYY-MM-DD 형식)
        dt = datetime.fromtimestamp(item['dt'])
        date_key = dt.strftime('%Y-%m-%d')
        day_name = dt.strftime('%A')  # 요일
        
        # 데이터 수집
        daily_data[date_key]['temps'].append(item['main']['temp'])
        daily_data[date_key]['humidity'].append(item['main']['humidity'])
        daily_data[date_key]['weather'].append(item['weather'][0])
        daily_data[date_key]['wind_speed'].append(item['wind']['speed'])
        daily_data[date_key]['date'] = dt
        daily_data[date_key]['day_name'] = day_name
    
    # 일별 평균 계산
    result = []
    for date_key in sorted(daily_data.keys())[:5]:  # 최대 5일
        data = daily_data[date_key]
        result.append({
            'date': data['date'],
            'day_name': data['day_name'],
            'temp_min': min(data['temps']),
            'temp_max': max(data['temps']),
            'temp_avg': sum(data['temps']) / len(data['temps']),
            'humidity': sum(data['humidity']) / len(data['humidity']),
            'wind_speed': sum(data['wind_speed']) / len(data['wind_speed']),
            'weather': max(set([w['main'] for w in data['weather']]), 
                          key=[w['main'] for w in data['weather']].count),
            'description': data['weather'][0]['description']
        })
    
    return result

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

def display_weekly_forecast(forecast_data):
    """주간 날씨 예보를 표시합니다."""
    daily_forecast = process_forecast_data(forecast_data)
    
    if not daily_forecast:
        st.error("주간 예보 데이터를 가져올 수 없습니다.")
        return
    
    st.markdown("---")
    st.markdown("## 📅 주간 날씨 예보 (5일)")
    
    # 날짜별로 카드 형식으로 표시
    cols = st.columns(5)
    
    for idx, day_data in enumerate(daily_forecast):
        with cols[idx]:
            # 날짜와 요일
            date_str = day_data['date'].strftime('%m/%d')
            day_name_kr = {
                'Monday': '월요일',
                'Tuesday': '화요일',
                'Wednesday': '수요일',
                'Thursday': '목요일',
                'Friday': '금요일',
                'Saturday': '토요일',
                'Sunday': '일요일'
            }
            day_kr = day_name_kr.get(day_data['day_name'], day_data['day_name'])
            
            # 날씨 아이콘
            icon = weather_icons.get(day_data['weather'], "🌍")
            
            # 카드 스타일로 표시
            st.markdown(f"""
            <div style='
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                height: 100%;
            '>
                <h4 style='margin: 0; color: #262730;'>{day_kr}</h4>
                <p style='margin: 5px 0; color: #666; font-size: 0.9em;'>{date_str}</p>
                <div style='font-size: 2.5em; margin: 10px 0;'>{icon}</div>
                <p style='margin: 5px 0;'><strong>{day_data['temp_max']:.1f}°C</strong></p>
                <p style='margin: 5px 0; color: #666; font-size: 0.9em;'>{day_data['temp_min']:.1f}°C</p>
                <p style='margin: 5px 0; font-size: 0.85em;'>{day_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # 상세 정보 테이블
    st.markdown("---")
    st.markdown("### 📊 상세 주간 예보")
    
    # HTML 테이블로 표시
    day_name_kr = {
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Wednesday': '수요일',
        'Thursday': '목요일',
        'Friday': '금요일',
        'Saturday': '토요일',
        'Sunday': '일요일'
    }
    
    # HTML 테이블 생성
    table_html = """
    <table style='width: 100%; border-collapse: collapse; margin: 20px 0;'>
        <thead>
            <tr style='background-color: #f0f2f6;'>
                <th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>날짜</th>
                <th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>요일</th>
                <th style='padding: 12px; text-align: left; border: 1px solid #ddd;'>날씨</th>
                <th style='padding: 12px; text-align: center; border: 1px solid #ddd;'>최고온도</th>
                <th style='padding: 12px; text-align: center; border: 1px solid #ddd;'>최저온도</th>
                <th style='padding: 12px; text-align: center; border: 1px solid #ddd;'>평균습도</th>
                <th style='padding: 12px; text-align: center; border: 1px solid #ddd;'>평균풍속</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for day_data in daily_forecast:
        day_kr = day_name_kr.get(day_data['day_name'], day_data['day_name'])
        icon = weather_icons.get(day_data['weather'], "🌍")
        
        table_html += f"""
            <tr style='border: 1px solid #ddd;'>
                <td style='padding: 10px; border: 1px solid #ddd;'>{day_data['date'].strftime('%Y-%m-%d')}</td>
                <td style='padding: 10px; border: 1px solid #ddd;'>{day_kr}</td>
                <td style='padding: 10px; border: 1px solid #ddd;'>{icon} {day_data['description']}</td>
                <td style='padding: 10px; text-align: center; border: 1px solid #ddd;'>{day_data['temp_max']:.1f}°C</td>
                <td style='padding: 10px; text-align: center; border: 1px solid #ddd;'>{day_data['temp_min']:.1f}°C</td>
                <td style='padding: 10px; text-align: center; border: 1px solid #ddd;'>{day_data['humidity']:.0f}%</td>
                <td style='padding: 10px; text-align: center; border: 1px solid #ddd;'>{day_data['wind_speed']:.1f} m/s</td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)

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
        - 5일 주간 날씨 예보
        - 전 세계 도시 검색 가능
        - 온도는 섭씨(°C) 기준
        """)
    
    # 메인 컨텐츠
    if city_input:
        with st.spinner(f"{city_input}의 날씨를 가져오는 중..."):
            weather_data = get_weather_data(city_input)
            
            if weather_data and weather_data.get('cod') != '404':
                # 현재 날씨 표시
                display_weather(weather_data)
                
                # 주간 날씨 예보 표시
                forecast_data = get_forecast_data(city_input)
                if forecast_data:
                    display_weekly_forecast(forecast_data)
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
        - 📅 5일 주간 날씨 예보
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

