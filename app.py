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

# 한글-영문 도시명 매핑
city_name_map = {
    # 한국 특별시/광역시
    "서울": "Seoul",
    "부산": "Busan",
    "인천": "Incheon",
    "대구": "Daegu",
    "대전": "Daejeon",
    "광주": "Gwangju",
    "울산": "Ulsan",
    "세종": "Sejong",
    
    # 경기도
    "수원": "Suwon",
    "성남": "Seongnam",
    "고양": "Goyang",
    "용인": "Yongin",
    "부천": "Bucheon",
    "안산": "Ansan",
    "안양": "Anyang",
    "남양주": "Namyangju",
    "화성": "Hwaseong",
    "평택": "Pyeongtaek",
    "의정부": "Uijeongbu",
    "시흥": "Siheung",
    "파주": "Paju",
    "김포": "Gimpo",
    "광명": "Gwangmyeong",
    "광주시": "Gwangju-si",
    "군포": "Gunpo",
    "하남": "Hanam",
    "오산": "Osan",
    "양주": "Yangju",
    "이천": "Icheon",
    "구리": "Guri",
    "안성": "Anseong",
    "포천": "Pocheon",
    "의왕": "Uiwang",
    "여주": "Yeoju",
    "양평": "Yangpyeong",
    "동두천": "Dongducheon",
    "과천": "Gwacheon",
    "가평": "Gapyeong",
    "연천": "Yeoncheon",
    
    # 강원도
    "춘천": "Chuncheon",
    "원주": "Wonju",
    "강릉": "Gangneung",
    "동해": "Donghae",
    "태백": "Taebaek",
    "속초": "Sokcho",
    "삼척": "Samcheok",
    "홍천": "Hongcheon",
    "횡성": "Hoengseong",
    "영월": "Yeongwol",
    "평창": "Pyeongchang",
    "정선": "Jeongseon",
    "철원": "Cheorwon",
    "화천": "Hwacheon",
    "양구": "Yanggu",
    "인제": "Inje",
    "고성": "Goseong",
    "양양": "Yangyang",
    
    # 충청북도
    "청주": "Cheongju",
    "충주": "Chungju",
    "제천": "Jecheon",
    "보은": "Boeun",
    "옥천": "Okcheon",
    "영동": "Yeongdong",
    "증평": "Jeungpyeong",
    "진천": "Jincheon",
    "괴산": "Goesan",
    "음성": "Eumseong",
    "단양": "Danyang",
    
    # 충청남도
    "천안": "Cheonan",
    "공주": "Gongju",
    "보령": "Boryeong",
    "아산": "Asan",
    "서산": "Seosan",
    "논산": "Nonsan",
    "계룡": "Gyeryong",
    "당진": "Dangjin",
    "금산": "Geumsan",
    "부여": "Buyeo",
    "서천": "Seocheon",
    "청양": "Cheongyang",
    "홍성": "Hongseong",
    "예산": "Yesan",
    "태안": "Taean",
    
    # 전라북도
    "전주": "Jeonju",
    "군산": "Gunsan",
    "익산": "Iksan",
    "정읍": "Jeongeup",
    "남원": "Namwon",
    "김제": "Gimje",
    "완주": "Wanju",
    "진안": "Jinan",
    "무주": "Muju",
    "장수": "Jangsu",
    "임실": "Imsil",
    "순창": "Sunchang",
    "고창": "Gochang",
    "부안": "Buan",
    
    # 전라남도
    "목포": "Mokpo",
    "여수": "Yeosu",
    "순천": "Suncheon",
    "나주": "Naju",
    "광양": "Gwangyang",
    "담양": "Damyang",
    "곡성": "Gokseong",
    "구례": "Gurye",
    "고흥": "Goheung",
    "보성": "Boseong",
    "화순": "Hwasun",
    "장흥": "Jangheung",
    "강진": "Gangjin",
    "해남": "Haenam",
    "영암": "Yeongam",
    "무안": "Muan",
    "함평": "Hampyeong",
    "영광": "Yeonggwang",
    "장성": "Jangseong",
    "완도": "Wando",
    "진도": "Jindo",
    "신안": "Sinan",
    
    # 경상북도
    "포항": "Pohang",
    "경주": "Gyeongju",
    "김천": "Gimcheon",
    "안동": "Andong",
    "구미": "Gumi",
    "영주": "Yeongju",
    "영천": "Yeongcheon",
    "상주": "Sangju",
    "문경": "Mungyeong",
    "경산": "Gyeongsan",
    "군위": "Gunwi",
    "의성": "Uiseong",
    "청송": "Cheongsong",
    "영양": "Yeongyang",
    "영덕": "Yeongdeok",
    "청도": "Cheongdo",
    "고령": "Goryeong",
    "성주": "Seongju",
    "칠곡": "Chilgok",
    "예천": "Yecheon",
    "봉화": "Bonghwa",
    "울진": "Uljin",
    "울릉": "Ulleung",
    
    # 경상남도
    "창원": "Changwon",
    "진주": "Jinju",
    "통영": "Tongyeong",
    "사천": "Sacheon",
    "김해": "Gimhae",
    "밀양": "Miryang",
    "거제": "Geoje",
    "양산": "Yangsan",
    "의령": "Uiryeong",
    "함안": "Haman",
    "창녕": "Changnyeong",
    "고성군": "Goseong-gun",
    "남해": "Namhae",
    "하동": "Hadong",
    "산청": "Sancheong",
    "함양": "Hamyang",
    "거창": "Geochang",
    "합천": "Hapcheon",
    
    # 제주특별자치도
    "제주": "Jeju",
    "서귀포": "Seogwipo",
    
    # 세계 주요 도시
    "도쿄": "Tokyo",
    "오사카": "Osaka",
    "교토": "Kyoto",
    "베이징": "Beijing",
    "상하이": "Shanghai",
    "홍콩": "Hong Kong",
    "타이베이": "Taipei",
    "방콕": "Bangkok",
    "싱가포르": "Singapore",
    "뉴욕": "New York",
    "로스앤젤레스": "Los Angeles",
    "LA": "Los Angeles",
    "샌프란시스코": "San Francisco",
    "시카고": "Chicago",
    "런던": "London",
    "파리": "Paris",
    "로마": "Rome",
    "베를린": "Berlin",
    "마드리드": "Madrid",
    "바르셀로나": "Barcelona",
    "시드니": "Sydney",
    "멜버른": "Melbourne",
    "두바이": "Dubai",
    "모스크바": "Moscow"
}

def convert_city_name(city_input):
    """한글 도시명을 영문으로 변환합니다."""
    if not city_input:
        return None
    
    # 입력값을 정리 (앞뒤 공백 제거)
    city_input = city_input.strip()
    
    # 한글-영문 매핑 딕셔너리에서 찾기
    if city_input in city_name_map:
        return city_name_map[city_input]
    
    # 매핑에 없으면 입력값 그대로 반환 (영문 도시명일 경우)
    return city_input

def get_weather_data(city_name):
    """OpenWeather API를 통해 현재 날씨 데이터를 가져옵니다."""
    try:
        # 한글 도시명을 영문으로 변환
        english_city = convert_city_name(city_name)
        
        params = {
            "q": english_city,
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
        # 한글 도시명을 영문으로 변환
        english_city = convert_city_name(city_name)
        
        params = {
            "q": english_city,
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
            placeholder="예: 서울, 부산, 인천 또는 Seoul, Tokyo",
            help="한글 또는 영문 도시명을 입력하세요"
        )
        
        # 한국 도시 선택 (드롭다운 + 빠른 버튼)
        st.markdown("#### 🇰🇷 한국 도시 선택")
        
        # 카테고리별 분류
        korea_cities_by_category = {
            "특별시/광역시": ["서울", "부산", "인천", "대구", "대전", "광주", "울산", "세종"],
            "경기도": ["수원", "성남", "고양", "용인", "부천", "안산", "안양", "남양주", 
                      "화성", "평택", "의정부", "시흥", "파주", "김포", "광명", "이천"],
            "강원도": ["춘천", "원주", "강릉", "동해", "태백", "속초", "삼척"],
            "충청북도": ["청주", "충주", "제천"],
            "충청남도": ["천안", "공주", "보령", "아산", "서산", "논산", "당진"],
            "전라북도": ["전주", "군산", "익산", "정읍", "남원", "김제"],
            "전라남도": ["목포", "여수", "순천", "나주", "광양"],
            "경상북도": ["포항", "경주", "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산"],
            "경상남도": ["창원", "진주", "통영", "사천", "김해", "밀양", "거제", "양산"],
            "제주도": ["제주", "서귀포"]
        }
        
        # 셀렉트박스로 카테고리 선택
        selected_category = st.selectbox(
            "지역 선택",
            list(korea_cities_by_category.keys()),
            key="category_select"
        )
        
        # 선택된 카테고리의 도시들을 버튼으로 표시
        category_cities = korea_cities_by_category[selected_category]
        
        # 4개씩 버튼 배치 (2줄)
        for i in range(0, len(category_cities), 4):
            cols = st.columns(4)
            for idx, city in enumerate(category_cities[i:i+4]):
                with cols[idx]:
                    if st.button(city, key=f"kr_{city}", use_container_width=True):
                        city_input = city
        
        # 세계 인기 도시 빠른 선택
        st.markdown("#### 🌍 세계 주요 도시")
        world_cities = ["도쿄", "뉴욕", "런던", "파리", "시드니", "두바이"]
        
        cols = st.columns(2)
        for idx, city in enumerate(world_cities):
            with cols[idx % 2]:
                if st.button(city, key=f"world_{city}", use_container_width=True):
                    city_input = city
        
        st.markdown("---")
        st.markdown("**ℹ️ 정보**")
        st.markdown("""
        - 🇰🇷 한글 도시명 지원
        - 🌏 영문 도시명도 가능
        - 📅 5일 주간 날씨 예보
        - 🌡️ 섭씨(°C) 기준
        """)
        
        st.markdown("**💡 팁**")
        st.markdown("""
        한글로 검색 가능:
        - 서울, 부산, 인천, 제주 등
        - 도쿄, 뉴욕, 파리 등
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
        1. 왼쪽 사이드바에서 **한글** 또는 **영문**으로 도시 이름을 입력하세요
        2. 또는 도시 버튼을 클릭하세요
        3. 실시간 날씨 정보와 주간 예보가 표시됩니다!
        
        ### 🇰🇷 한글 지원 도시 (예시)
        - **한국**: 서울, 부산, 인천, 대구, 대전, 광주, 울산, 제주 등
        - **일본**: 도쿄, 오사카, 교토
        - **중국**: 베이징, 상하이, 홍콩
        - **미국**: 뉴욕, LA, 샌프란시스코
        - **유럽**: 런던, 파리, 로마, 베를린
        - **기타**: 시드니, 두바이, 방콕, 싱가포르 등
        
        ### 제공되는 정보
        - 🌡️ 현재 온도 및 체감 온도
        - 💧 습도
        - 💨 풍속
        - 🌤️ 날씨 상태
        - 📅 5일 주간 날씨 예보
        - 📊 기압
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

