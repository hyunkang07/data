# 🚀 Streamlit Cloud 배포 가이드

## 빠른 시작

### 1단계: GitHub 저장소 생성 및 Push

```bash
# Git 초기화 (아직 안했다면)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial commit: 날씨 웹 애플리케이션"

# GitHub에서 저장소 생성 후
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

### 2단계: Streamlit Cloud에서 배포

1. **https://share.streamlit.io** 접속
2. **Sign in with GitHub** 클릭
3. **New app** 클릭
4. 배포 설정:
   ```
   Repository: your-username/your-repo-name
   Branch: main
   Main file path: app.py
   ```
5. **Deploy!** 클릭

### 3단계: 완료! 🎉

몇 분 후 앱이 배포되고 다음과 같은 URL을 받게 됩니다:
```
https://your-app-name.streamlit.app
```

---

## 필수 파일 체크리스트

배포를 위해 다음 파일들이 필요합니다:

- ✅ `app.py` - 메인 애플리케이션 코드
- ✅ `requirements.txt` - Python 패키지 의존성
- ✅ `.streamlit/config.toml` - Streamlit 설정 파일
- ✅ `README.md` - 프로젝트 설명
- ✅ `.gitignore` - Git 제외 파일 목록

선택사항:
- ⚪ `packages.txt` - 시스템 레벨 패키지 (필요시)
- ⚪ `secrets.toml` - 로컬 개발용 비밀 키 (Git에 포함하지 말 것!)

---

## 보안: API 키 관리

### 현재 상태
API 키가 코드에 하드코딩되어 있습니다. 공개 저장소라면 보안 개선이 필요합니다.

### 개선 방법

#### 1. Streamlit Secrets 사용 (권장)

**Streamlit Cloud 대시보드에서:**
1. 앱 설정 → "Secrets" 섹션
2. 다음 내용 추가:
```toml
API_KEY = "4420348db0f68ca32ed864b0702fd5a0"
```

**app.py 수정:**
```python
import streamlit as st

# API 키 (Secrets에서 가져오기, 없으면 기본값 사용)
try:
    API_KEY = st.secrets["API_KEY"]
except:
    API_KEY = "4420348db0f68ca32ed864b0702fd5a0"
```

#### 2. 로컬 개발용 secrets.toml 파일

`.streamlit/secrets.toml` 파일 생성 (로컬 개발용):
```toml
API_KEY = "4420348db0f68ca32ed864b0702fd5a0"
```

⚠️ **중요**: `.gitignore`에 `secrets.toml`이 포함되어 있는지 확인!

---

## 문제 해결

### 배포 실패 시

1. **로그 확인**: Streamlit Cloud 대시보드에서 배포 로그 확인
2. **requirements.txt 확인**: 패키지 버전 호환성 체크
3. **파일 경로 확인**: `app.py`가 저장소 루트에 있는지 확인

### 일반적인 오류

#### ModuleNotFoundError
```bash
# requirements.txt에 누락된 패키지 추가
streamlit>=1.28.0
requests>=2.27.0
```

#### 앱이 로드되지 않음
- 브라우저 캐시 삭제
- Streamlit Cloud에서 "Reboot app" 클릭

#### API 키 오류
- Secrets 설정 확인
- API 키가 유효한지 확인

---

## 배포 후 관리

### 앱 업데이트
```bash
# 코드 수정 후
git add .
git commit -m "업데이트 내용 설명"
git push
```
→ Streamlit Cloud가 자동으로 재배포합니다!

### 앱 중지/재시작
Streamlit Cloud 대시보드에서:
- **Reboot app**: 앱 재시작
- **Delete app**: 앱 삭제

### 모니터링
- **Usage**: 방문자 수, 리소스 사용량 확인
- **Logs**: 실시간 로그 모니터링

---

## 추가 리소스

- 📚 [Streamlit 문서](https://docs.streamlit.io/)
- 🚀 [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- 💬 [Streamlit 커뮤니티](https://discuss.streamlit.io/)
- 🌐 [OpenWeather API 문서](https://openweathermap.org/api)

---

## 다음 단계

배포 후 개선할 수 있는 사항:

1. **커스텀 도메인 연결** (유료 플랜)
2. **데이터베이스 연동** (날씨 기록 저장)
3. **더 많은 기능 추가**:
   - 5일 일기예보
   - 날씨 그래프 차트
   - 여러 도시 비교
   - 위치 기반 자동 검색

4. **UI/UX 개선**:
   - 다크 모드 토글
   - 애니메이션 효과
   - 다국어 지원

즐거운 배포 되세요! 🎉

