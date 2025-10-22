# 🌤️ 날씨 정보 웹 애플리케이션

OpenWeather API와 Streamlit을 사용한 실시간 날씨 정보 앱입니다.

## 📋 기능

- 🌍 전 세계 도시의 실시간 날씨 검색
- 🌡️ 현재 온도 및 체감 온도 표시
- 💧 습도, 풍속, 기압 등 상세 정보
- 🎨 직관적이고 아름다운 UI
- 🚀 빠른 검색을 위한 인기 도시 버튼

## 🛠️ 설치 방법

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱이 실행됩니다.

## 📦 필요한 패키지

- `streamlit`: 웹 애플리케이션 프레임워크
- `requests`: HTTP 요청을 위한 라이브러리

## 🔑 API 키

현재 OpenWeather API 키가 코드에 포함되어 있습니다.
프로덕션 환경에서는 환경 변수를 사용하는 것을 권장합니다.

## 🎯 사용 방법

1. 애플리케이션을 실행합니다
2. 왼쪽 사이드바에서 도시 이름을 입력하거나 인기 도시 버튼을 클릭합니다
3. 실시간 날씨 정보를 확인합니다!

## 🌟 주요 화면

- **메인 대시보드**: 온도, 습도, 풍속 등 주요 정보를 카드 형식으로 표시
- **상세 정보**: JSON 형식의 원본 데이터 확인 가능
- **반응형 디자인**: 다양한 화면 크기에 최적화

## 📝 참고사항

- 도시 이름은 영문으로 입력해야 합니다
- 온도는 섭씨(°C) 기준입니다
- 날씨 설명은 한국어로 표시됩니다

## 🔗 API 출처

[OpenWeather API](https://openweathermap.org/api)

---

## 🚀 Streamlit Cloud 배포 방법

### 1. GitHub 저장소 준비

1. GitHub에 새 저장소를 만듭니다
2. 프로젝트 파일들을 push 합니다:

```bash
git init
git add .
git commit -m "날씨 앱 초기 커밋"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Streamlit Cloud 배포

1. [share.streamlit.io](https://share.streamlit.io)에 접속합니다
2. GitHub 계정으로 로그인합니다
3. "New app" 버튼을 클릭합니다
4. 다음 정보를 입력합니다:
   - **Repository**: 생성한 GitHub 저장소 선택
   - **Branch**: main
   - **Main file path**: app.py
5. "Deploy!" 버튼을 클릭합니다

### 3. 배포 완료

몇 분 후 앱이 배포되고 공개 URL이 생성됩니다!

## 📦 배포에 필요한 파일

배포를 위해 다음 파일들이 준비되어 있습니다:

- ✅ `app.py` - 메인 애플리케이션
- ✅ `requirements.txt` - Python 패키지 의존성
- ✅ `.streamlit/config.toml` - Streamlit 설정 (테마, 서버 설정)
- ✅ `packages.txt` - 시스템 레벨 패키지 (필요시)
- ✅ `.gitignore` - Git 제외 파일
- ✅ `README.md` - 프로젝트 문서

## ⚙️ 환경 변수 설정 (선택사항)

보안을 위해 API 키를 환경 변수로 관리하려면:

1. Streamlit Cloud 대시보드에서 앱 설정으로 이동
2. "Secrets" 섹션에서 다음을 추가:

```toml
API_KEY = "4420348db0f68ca32ed864b0702fd5a0"
```

3. `app.py`에서 다음과 같이 수정:

```python
import streamlit as st

# API 키
API_KEY = st.secrets.get("API_KEY", "4420348db0f68ca32ed864b0702fd5a0")
```

## 🔄 업데이트 방법

앱을 수정한 후:

```bash
git add .
git commit -m "업데이트 설명"
git push
```

Streamlit Cloud가 자동으로 새 버전을 배포합니다!