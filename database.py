import sqlite3
import json

# --- 데이터베이스 설정 ---
DB_PATH = 'backend/database.db'

def create_database():
    """데이터베이스와 테이블을 생성하고 초기 데이터를 삽입합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("기존 테이블 삭제 중...")
    cursor.execute("DROP TABLE IF EXISTS POPULATOR")
    cursor.execute("DROP TABLE IF EXISTS DASHBOARDS")

    print("'POPULATOR' 테이블 생성 중...")
    cursor.execute("""
    CREATE TABLE POPULATOR (
        ID TEXT NOT NULL,
        NAME TEXT,
        CODE TEXT,
        DATA REAL,
        DT_ID TEXT,
        DT_DATA REAL,
        CREATE_DATE TEXT DEFAULT (datetime('now', 'localtime'))
    )
    """)

    print("'DASHBOARDS' 테이블 생성 중...")
    cursor.execute("""
    CREATE TABLE DASHBOARDS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME TEXT NOT NULL,
        LAYOUT TEXT
    )
    """)

    # --- 예시 데이터 삽입 ---

    # 1. 월별 검출 유형 (CODE: 월별 검출 유형) - 라인/바 차트용
    monthly_detection_data = [
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 150, '2023-01', None),
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 180, '2023-02', None),
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 220, '2023-03', None),
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 200, '2023-04', None),
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 210, '2023-05', None),
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 250, '2023-06', None),
        ('detection_monthly', '월별 검출 건수', '월별 검출 유형', 310, '2023-07', None),
    ]

    # 2. 일별 검출 유형 (CODE: 일별 검출 유형) - 라인/바 차트용
    daily_detection_data = [
        ('detection_daily', '일별 검출 건수', '일별 검출 유형', 20, '2023-07-01', None),
        ('detection_daily', '일별 검출 건수', '일별 검출 유형', 25, '2023-07-02', None),
        ('detection_daily', '일별 검출 건수', '일별 검출 유형', 15, '2023-07-03', None),
        ('detection_daily', '일별 검출 건수', '일별 검출 유형', 30, '2023-07-04', None),
        ('detection_daily', '일별 검출 건수', '일별 검출 유형', 22, '2023-07-05', None),
    ]

    # 3. 개인정보 접근 사용자 유형 (CODE: 개인정보 접근 사용자 유형) - 파이/도넛 차트용
    user_access_data = [
        ('user_access', 'Admin', '개인정보 접근 사용자 유형', None, 'user_admin', 15),
        ('user_access', 'Developer', '개인정보 접근 사용자 유형', None, 'user_dev', 45),
        ('user_access', 'Operator', '개인정보 접근 사용자 유형', None, 'user_op', 25),
        ('user_access', 'Manager', '개인정보 접근 사용자 유형', None, 'user_manager', 10),
    ]

    print("'POPULATOR' 테이블에 데이터 삽입 중...")
    cursor.executemany("INSERT INTO POPULATOR (ID, NAME, CODE, DATA, DT_ID, DT_DATA) VALUES (?, ?, ?, ?, ?, ?)", monthly_detection_data)
    cursor.executemany("INSERT INTO POPULATOR (ID, NAME, CODE, DATA, DT_ID, DT_DATA) VALUES (?, ?, ?, ?, ?, ?)", daily_detection_data)
    cursor.executemany("INSERT INTO POPULATOR (ID, NAME, CODE, DATA, DT_ID, DT_DATA) VALUES (?, ?, ?, ?, ?, ?)", user_access_data)

    # 초기 대시보드 레이아웃을 빈 배열로 설정
    initial_layout = []

    print("'DASHBOARDS' 테이블에 데이터 삽입 중...")
    cursor.execute("INSERT INTO DASHBOARDS (ID, NAME, LAYOUT) VALUES (?, ?, ?)",
                   (1, '기본 대시보드', json.dumps(initial_layout)))

    conn.commit()
    conn.close()

    print(f"\n데이터베이스 '{DB_PATH}' 생성 및 초기화 완료.")
    print("이제 다음 프롬프트를 사용하여 차트를 생성하고 테스트할 수 있습니다:")
    print("- 월별 검출 유형을 라인 차트로 그려줘")
    print("- 일별 검출 유형을 막대 차트로 그려줘")
    print("- 개인정보 접근 사용자 유형을 원 차트로 만들어줘")


if __name__ == '__main__':
    create_database()
