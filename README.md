# AI 기반 대시보드 및 보고서 생성기

사용자의 자연어 입력을 바탕으로 동적 차트를 생성하고, 커스터마이징 가능한 대시보드를 구성하며, AI가 데이터 인사이트를 분석하여 보고서까지 작성해주는 웹 애플리케이션입니다.

## ✨ 주요 기능

- **동적 차트 생성**: "월간 이용 내역 보여줘"와 같은 자연어 프롬프트로 라인, 바, 파이 차트 등 생성
- **Gemini API 연동**: Google Gemini를 활용한 지능적인 프롬프트 분석 및 보고서 내용 생성
- **커스터마이징 대시보드**: 드래그 앤 드롭으로 위젯(차트)의 위치와 크기를 자유롭게 배치하고 저장
- **AI 리포팅**: 생성된 대시보드의 각 차트를 이미지로 캡처하고, AI가 차트 데이터를 분석하여 생성한 설명과 함께 A4 형식의 보고서 페이지로 제공합니다.
- **데이터 그리드**: 대시보드에 생성된 모든 차트의 원본 데이터를 별도의 페이지에서 테이블 형태로 확인하고 분석할 수 있습니다.

## 🛠️ 기술 스택

- **Backend**: Python, Flask, Google Generative AI
- **Frontend**: Vue.js 3, Vuetify 3, ApexCharts, vue3-grid-layout
- **Database**: SQLite

## 📂 프로젝트 구조
  ```
  /
  ├── backend/
  │   ├── app.py          # Flask API 서버
  │   └── database.db     # SQLite 데이터베이스 파일
  │
  ├── frontend-v3/
  │   ├── src/
  │   │   ├── views/
  │   │   │   ├── Dashboard.vue
  │   │   │   ├── Report.vue
  │   │   │   └── DataGrid.vue
  │   │   ├── main.js
  │   │   └── App.vue
  │   └── ...
  │
  ├── docs/
  │   ├── API.md          # API 명세서
  │   └── DATABASE.md     # 데이터베이스 스키마 정보
  │
  └── database.py         # DB 테이블 생성 및 초기화 스크립트
  ```

## 🚀 설치 및 실행

**사전 준비**: Python 3.8+, Node.js 16+

**1. 환경 변수 설정**

Google Gemini API 키를 환경 변수로 설정합니다.
- macOS/Linux
  ```
  export GOOGLE_API_KEY="YOUR_API_KEY"
  ```
- Windows
  ```
  set GOOGLE_API_KEY="YOUR_API_KEY"
  ```

**2. 백엔드 설정**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # 또는 venv\Scripts\activate (Windows)
pip install Flask google-generativeai numpy
```

**3. 데이터베이스 초기화**
프로젝트 루트에서 실행합니다. 이 스크립트는 테스트용 샘플 데이터를 함께 생성합니다.
```bash
python database.py
```

**4. 프론트엔드 설정**
```bash
cd frontend-v3
npm install
```

**5. 애플리케이션 실행**
- **백엔드 서버 실행:**
  ```bash
  cd backend
  python app.py
  ```
- **프론트엔드 서버 실행:**
  ```bash
  cd frontend-v3
  npm run serve
  ```
브라우저에서 실행된 frontend-v3의 URL로 접속합니다.
기본 url은 `http://localhost:8080`이나 접속 경로는 실행한 `frontend-v3`의 내용에 따라 달라질 수 있습니다.

## 🧪 테스트 프롬프트 예시

데이터베이스 초기화 후, 대시보드에서 다음 프롬프트를 입력하여 주요 기능을 테스트할 수 있습니다.

- `월별 검출 유형을 라인 차트로 그려줘`
- `일별 검출 유형을 막대 차트로 그려줘`
- `개인정보 접근 사용자 유형을 원 차트로 만들어줘`

차트를 추가한 후, 상단의 **보고서 생성** 버튼을 클릭하여 AI가 분석한 보고서를 확인할 수 있습니다.
또한, **데이터 그리드** 탭을 클릭하여 각 차트의 원본 데이터를 테이블 형태로 확인해 보세요.


