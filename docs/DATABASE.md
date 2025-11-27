# 데이터베이스 스키마

이 문서는 프로젝트에서 사용하는 SQLite 데이터베이스의 테이블 구조를 설명합니다.

---

### ERD (Entity-Relationship Diagram)

```
+------------------+          +-------------------+
|    POPULATOR     |          |    DASHBOARDS     |
+------------------+          +-------------------+
| PK | ID: TEXT     |          | PK | ID: INTEGER    |
|    | NAME: TEXT   |          |    | NAME: TEXT     |
|    | CODE: TEXT   |          |    | LAYOUT: TEXT   |
|    | DATA: TEXT   |          +-------------------+
|    | DT_ID: TEXT  |
|    | DT_DATA: REAL|
|    | CREATE_DATE: TEXT |
+------------------+
```

- **관계:** `DASHBOARDS.LAYOUT` 필드는 `POPULATOR.ID`를 논리적으로 참조하는 `chartId`를 포함한 JSON 배열 문자열을 저장합니다. 물리적인 Foreign Key 제약은 설정되지 않았습니다.

---

### 테이블 상세

#### 1. `POPULATOR`

차트의 원본이 되는 시계열 또는 분류 데이터를 저장하는 테이블입니다.

- **`ID`** (TEXT, Primary Key): 데이터셋을 고유하게 식별하는 ID (예: `monthly_usage`, `daily_pi_type`).
- **`NAME`** (TEXT): 데이터셋의 이름 (예: `월간 이용 내역`).
- **`CODE`** (TEXT): 데이터셋을 분류하기 위한 코드 (예: `A01`).
- **`DATA`** (TEXT): 2D, 3D 차트의 X축 또는 그룹화 기준이 되는 데이터 (예: `2023-01`, `2023-04-01`).
- **`DT_ID`** (TEXT): 3D 차트에서 시리즈(범례)를 구분하는 ID (예: `이름`, `연락처`). 2D 데이터의 경우 `NULL`.
- **`DT_DATA`** (REAL): 차트의 Y축 값이 되는 수치 데이터 (예: `150`, `50`).
- **`CREATE_DATE`** (TEXT): 레코드 생성 일시.

#### 2. `DASHBOARDS`

사용자가 구성한 대시보드의 정보를 저장하는 테이블입니다.

- **`ID`** (INTEGER, Primary Key): 대시보드의 고유 ID.
- **`NAME`** (TEXT): 대시보드의 이름 (예: `기본 대시보드`).
- **`LAYOUT`** (TEXT): 대시보드 위젯들의 레이아웃 정보를 담는 JSON 배열 문자열.
  - **JSON 구조 예시:**
    ```json
    [
      {
        "x": 0,
        "y": 0,
        "w": 6,
        "h": 8,
        "i": "0",
        "chartId": "monthly_usage"
      }
    ]
    ```
    - `x`, `y`: 그리드 내 위젯의 시작 위치
    - `w`, `h`: 위젯의 너비와 높이
    - `i`: 위젯의 고유 ID (vue-grid-layout에서 사용)
    - `chartId`: 이 위젯이 보여줄 `POPULATOR` 테이블의 ID

