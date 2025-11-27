# API 명세서

**Base URL:** `/api`

---

### 1. 차트 데이터 생성

- **Endpoint:** `POST /chart`
- **Description:** 사용자의 자연어 프롬프트를 받아 Gemini API를 통해 분석 후, 차트를 그리는 데 필요한 데이터를 반환합니다.
- **Request Body:**
  ```json
  {
    "prompt": "지난달 개인정보 이용 내역을 바 차트로 보여줘"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "chartOptions": {
      "chart": { "type": "bar" },
      "xaxis": { "categories": ["2023-03-01", "2023-03-02", "..."] }
    },
    "series": [
      { "name": "이용 내역", "data": [150, 180, "..."] }
    ]
  }
  ```
- **Error Response (500 Internal Server Error):**
  ```json
  {
    "error": "Gemini API 호출 또는 JSON 파싱 실패: <error_message>"
  }
  ```

---

### 2. 대시보드 레이아웃

#### 2.1. 레이아웃 조회
- **Endpoint:** `GET /dashboards/{id}`
- **Description:** 특정 대시보드의 레이아웃 정보를 조회합니다.
- **Success Response (200 OK):**
  ```json
  {
    "layout": [
      { "x": 0, "y": 0, "w": 6, "h": 8, "i": "0", "chartId": "monthly_usage" },
      { "x": 6, "y": 0, "w": 6, "h": 8, "i": "1", "chartId": "daily_pi_type" }
    ]
  }
  ```

#### 2.2. 레이아웃 저장
- **Endpoint:** `POST /dashboards/{id}`
- **Description:** 특정 대시보드의 위젯 레이아웃을 저장합니다.
- **Request Body:**
  ```json
  {
    "layout": [
      { "x": 0, "y": 0, "w": 6, "h": 8, "i": "0", "chartId": "monthly_usage" }
    ]
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "status": "success"
  }
  ```

---

### 3. 보고서 생성

- **Endpoint:** `POST /report`
- **Description:** 특정 대시보드의 데이터와 사용자 프롬프트를 기반으로 Gemini API를 통해 분석 보고서를 생성합니다.
- **Request Body:**
  ```json
  {
    "dashboard_id": 1,
    "prompt": "A 사용자의 7월 데이터에 특이사항이 있는지 집중적으로 분석해줘"
  }
  ```
- **Success Response (200 OK):**
  ```json
  {
    "report": "# 대시보드 분석 보고서\n\n### 월간 이용 내역 분석\n\n- **특이사항**: A 사용자는 7월에 평소보다 30% 더 많은 개인정보를 조회했습니다..."
  }
  ```
- **Error Response (404 Not Found):**
  ```json
  {
    "error": "Dashboard not found"
  }
  ```
