import os
import json
import sqlite3
from datetime import datetime
import numpy as np
from flask import Flask, request, jsonify
import google.generativeai as genai
import traceback # traceback 모듈 임포트

# --- Flask 앱 및 데이터베이스 설정 ---
app = Flask(__name__)
DB_PATH = 'database.db'

def get_db_connection():
    """데이터베이스 연결 객체를 반환합니다."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Gemini API 설정 ---
gemini_model = None
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("경고: GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다. Gemini API 관련 기능이 작동하지 않습니다.")
    else:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash-lite')
        print("Gemini API가 성공적으로 초기화되었습니다. 사용 모델: gemini-2.5-flash-lite")
except Exception as e:
    print(f"Gemini API 설정 중 오류 발생: {e}")
    gemini_model = None

# --- Gemini 프롬프트 템플릿 ---
# GEMINI_CHART_PROMPT_TEMPLATE를 두 부분으로 나누어 직접 조합
GEMINI_CHART_PROMPT_TEMPLATE_PART1 = """
You are an expert at generating database queries. Analyze the user's request and respond in the following JSON format.
The available table is 'POPULATOR', with columns: ID, NAME, CODE, DATA, DT_ID, DT_DATA.

Here are specific rules for common chart requests based on the 'CODE' column:
- If the user asks for "월별 검출 유형" or "일별 검출 유형":
    - The 'chart_type' MUST be 'line' or 'bar'.
    - The 'x_axis' MUST be 'DT_ID'.
    - The 'y_axis' MUST be 'DATA'.
    - You MUST include a filter: "filters": {"CODE": "월별 검출 유형"} (or "일별 검출 유형" accordingly).
- If the user asks for "개인정보 접근 사용자 유형":
    - The 'chart_type' MUST be 'pie' or 'donut'.
    - The 'x_axis' MUST be 'NAME' (representing the user names for grouping).
    - The 'y_axis' MUST be the string "COUNT" (representing the count for each user).
    - You MUST include a filter: "filters": {"CODE": "개인정보 접근 사용자 유형"}.

General rules for other chart requests:
- For 'line', 'bar' chart types:
    - The 'x_axis' and 'y_axis' values MUST be one of the available columns: ID, NAME, CODE, DATA, DT_ID, DT_DATA.
- For 'pie', 'donut' chart types:
    - The 'x_axis' MUST be a categorical column (e.g., NAME, CODE).
    - The 'y_axis' MUST always be the string "COUNT" (representing COUNT(*)).

The chart type must be one of 'line', 'bar', 'pie', 'donut'.
For 3D data (when DT_ID is relevant), the dimension is '3D', otherwise '2D'.
If 'dimension' is '3D', you MUST also include a 'group_by' key, which must be one of the available columns.
Ensure to include 'x_axis' and 'y_axis' keys in the JSON output.
If the user's request implies filtering (e.g., "월간 이용 내역", "ID가 monthly_usage인 데이터"), include a 'filters' key (e.g., "filters": {"ID": "monthly_usage"}). The keys within the 'filters' object (e.g., "ID") MUST be enclosed in double quotes. Otherwise, omit the 'filters' key.

User Request: "
"""

GEMINI_CHART_PROMPT_TEMPLATE_PART2 = """

JSON Output:
"""

GEMINI_REPORT_PROMPT_TEMPLATE = """
You are a professional data analyst. Write an analysis report in Markdown format based on the provided data.
You must explain the overall trend, average, peak/trough, and any notable anomalies.
If the user has additional requests, focus on them in your analysis.

- Chart Name: {chart_name}
- User's Additional Request: {user_prompt}
- Data (CSV format):
{data_csv}

Analysis Report:
"""

# --- API Endpoints ---

@app.route('/api/chart', methods=['POST'])
def generate_chart():
    """사용자 프롬프트를 기반으로 차트 데이터를 생성합니다."""
    if not gemini_model:
        return jsonify({"error": "Gemini API가 초기화되지 않았거나 GOOGLE_API_KEY가 유효하지 않습니다."}), 500

    prompt = request.json.get('prompt', '')
    if not prompt:
        return jsonify({"error": "프롬프트가 필요합니다."}), 400

    try:
        # Dr. Python: 템플릿 내용 출력 추가 (이스케이프된 중괄호가 아닌 리터럴 중괄호로 변경)
        print(f"Dr. Python Debug: GEMINI_CHART_PROMPT_TEMPLATE_PART1 content: {GEMINI_CHART_PROMPT_TEMPLATE_PART1}")

        # 직접 문자열 조합
        full_prompt = f"{GEMINI_CHART_PROMPT_TEMPLATE_PART1}{prompt}{GEMINI_CHART_PROMPT_TEMPLATE_PART2}"

        print(f"Dr. Python Debug: 최종 full_prompt: {full_prompt}")

        response = gemini_model.generate_content(full_prompt)

        # Dr. Python: Gemini 응답 객체 및 텍스트 상세 디버깅
        print(f"Dr. Python Debug: Type of response object: {type(response)}")
        print(f"Dr. Python Debug: Dir of response object: {dir(response)}")
        print(f"Dr. Python Debug: Type of response.text: {type(response.text)}")
        print(f"Dr. Python Debug: Gemini 원시 응답 (response.text): {response.text}")

        # Add this print to see the raw text before stripping/replacing
        print(f"Dr. Python Debug: Content of response.text before strip/replace: {response.text}")

        json_text = response.text.strip().replace('```json', '').replace('```', '')

        print(f"Dr. Python Debug: 가공된 JSON 텍스트 (json_text): {json_text}")

        params = json.loads(json_text)

        print(f"Dr. Python Debug: Gemini로부터 받은 파싱된 params: {params}")

    except Exception as e:
        print(f"Dr. Python Debug: Exception caught in Gemini interaction block: {type(e).__name__}: {e}")
        traceback.print_exc() # 상세 트레이스백 출력
        return jsonify({"error": f"Gemini 분석 중 오류 발생: {e}"}), 500

    if 'x_axis' not in params or 'y_axis' not in params:
        return jsonify({"error": "Gemini 응답에 'x_axis' 또는 'y_axis' 정보가 누락되었습니다. 프롬프트를 더 명확하게 작성해주세요."}), 500

    conn = get_db_connection()

    chart_type = params['chart_type']
    x_axis_col = params['x_axis']
    y_axis_col = params['y_axis']

    sql_query = ""
    query_params = []

    if chart_type in ['pie', 'donut']:
        # For pie/donut charts, we need to group by x_axis and count occurrences
        # If y_axis is explicitly DT_DATA, we select DT_DATA directly
        if y_axis_col == 'DT_DATA': # This condition is now less likely to be met for "개인정보 접근 사용자 유형"
            select_clause = f"{x_axis_col}, {y_axis_col}"
        else: # Default to COUNT(*) for other pie/donut charts, including "개인정보 접근 사용자 유형"
            select_clause = f"{x_axis_col}, COUNT(*) as count_value"

        sql_query = f"SELECT {select_clause} FROM POPULATOR"

        if 'filters' in params and params['filters']:
            filter_key_raw = list(params['filters'].keys())[0]
            filter_value = list(params['filters'].values())[0]
            filter_key_cleaned = filter_key_raw.strip('"')
            sql_query += f" WHERE {filter_key_cleaned} = ?"
            query_params.append(filter_value)

        # Only group by if we are counting, not if we are using DT_DATA directly
        if y_axis_col != 'DT_DATA': # This condition is now more likely to be met for "개인정보 접근 사용자 유형"
            sql_query += f" GROUP BY {x_axis_col}"

    else: # line, bar charts
        select_columns = [x_axis_col, y_axis_col]
        if params.get('dimension') == '3D':
            if 'group_by' not in params:
                return jsonify({"error": "Gemini 응답에 'group_by' 정보가 누락되었습니다. 3D 차트 프롬프트를 더 명확하게 작성해주세요."}), 500
            select_columns.append(params['group_by'])

        select_clause = ", ".join(select_columns)
        sql_query = f"SELECT {select_clause} FROM POPULATOR"

        if 'filters' in params and params['filters']: # Check if 'filters' key exists and is not empty
            print(f"Dr. Python Debug: 'filters' key found in params: {params['filters']}")

            # Ensure filters is a dictionary
            if not isinstance(params['filters'], dict):
                print(f"Dr.Python Debug: 'filters' is not a dictionary: {type(params['filters'])}")
                return jsonify({"error": "Gemini 응답의 'filters' 형식이 올바르지 않습니다. 딕셔너리여야 합니다."}), 500

            if not params['filters']: # Check if filters dictionary is empty
                print("Dr. Python Debug: params['filters'] is empty, skipping WHERE clause.")
            else:
                filter_key_raw = list(params['filters'].keys())[0] # Get the raw key
                filter_value = list(params['filters'].values())[0]

                print(f"Dr. Python Debug: filter_key_raw: '{filter_key_raw}', filter_value: '{filter_value}'")

                # Dr. Python: filter_key에서 따옴표 제거
                filter_key_cleaned = filter_key_raw.strip('"')
                print(f"Dr. Python Debug: filter_key_cleaned: '{filter_key_cleaned}'")

                sql_query += f" WHERE {filter_key_cleaned} = ?" # Use the cleaned key in the SQL query
                query_params.append(filter_value)
        else:
            print("Dr. Python Debug: 'filters' key not found or is empty in params.")

    print(f"Dr. Python Debug: Final SQL Query: {sql_query}")
    print(f"Dr. Python Debug: Query Parameters: {query_params}")

    try:
        rows = conn.execute(sql_query, tuple(query_params)).fetchall()
    except Exception as e:
        print(f"Dr. Python Debug: Error during conn.execute: {type(e).__name__}: {e}")
        traceback.print_exc() # 상세 트레이스백 출력
        return jsonify({"error": f"데이터베이스 쿼리 실행 중 오류 발생: {e}"}), 500

    categories = []
    series = []
    table_data = { "headers": [], "items": [] }

    if rows:
        table_data["headers"] = list(rows[0].keys())
        table_data["items"] = [dict(row) for row in rows]

    if chart_type in ['pie', 'donut']:
        labels = [row[x_axis_col] for row in rows]
        # If y_axis is DT_DATA, use it directly. Otherwise, use 'count_value'.
        data_values = [row[y_axis_col] if y_axis_col == 'DT_DATA' else row['count_value'] for row in rows]

        series = data_values # For pie/donut, series is just an array of values
        chart_options = {
            "chart": {"type": chart_type},
            "labels": labels, # Labels for pie/donut slices
            "responsive": [{
                "breakpoint": 480,
                "options": {
                    "chart": {"width": 200},
                    "legend": {"position": 'bottom'}
                }
            }]
        }
    elif params.get('dimension') == '3D':
        categories = sorted(list(set([row[x_axis_col] for row in rows])))
        groups = sorted(list(set([row[params['group_by']] for row in rows])))

        for group in groups:
            data = []
            for category in categories:
                value = next((row[y_axis_col] for row in rows if row[x_axis_col] == category and row[params['group_by']] == group), 0)
                data.append(value)
            series.append({"name": group, "data": data})

        chart_options = {
            "chart": {"type": chart_type},
            "xaxis": {"categories": categories}
        }
    else: # 2D line, bar charts
        categories = [row[x_axis_col] for row in rows]
        series_data = [row[y_axis_col] for row in rows]
        series = [{"name": y_axis_col, "data": series_data}]

        chart_options = {
            "chart": {"type": chart_type},
            "xaxis": {"categories": categories}
        }

    conn.close()

    response_data = {
        "chartOptions": chart_options,
        "series": series,
        "tableData": table_data
    }
    return jsonify(response_data)


@app.route('/api/dashboards/<dashboard_id>', methods=['GET', 'POST'])
def handle_dashboard(dashboard_id):
    """대시보드 레이아웃을 조회하거나 저장합니다."""
    conn = get_db_connection()
    if request.method == 'POST':
        layout_data = request.json.get('layout')
        conn.execute("UPDATE DASHBOARDS SET layout = ? WHERE id = ?", (json.dumps(layout_data), dashboard_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    else:  # GET
        dashboard = conn.execute("SELECT layout FROM DASHBOARDS WHERE id = ?", (dashboard_id,)).fetchone()
        conn.close()
        if dashboard and dashboard['layout']:
            return jsonify({"layout": json.loads(dashboard['layout'])})
        return jsonify({"layout": []})


@app.route('/api/report', methods=['POST'])
def create_report():
    """대시보드 데이터를 기반으로 분석 보고서를 생성합니다."""
    if not gemini_model:
        return jsonify({"error": "Gemini API가 초기화되지 않았거나 GOOGLE_API_KEY가 유효하지 않습니다."}), 500

    chart_prompt = request.json.get('prompt', '')
    if not chart_prompt:
        return jsonify({"error": "프롬프트가 필요합니다."}), 400

    try:
        # 1. Get chart parameters from Gemini
        full_chart_prompt = f"{GEMINI_CHART_PROMPT_TEMPLATE_PART1}{chart_prompt}{GEMINI_CHART_PROMPT_TEMPLATE_PART2}"
        chart_response = gemini_model.generate_content(full_chart_prompt)
        json_text = chart_response.text.strip().replace('```json', '').replace('```', '')
        params = json.loads(json_text)

        if 'x_axis' not in params or 'y_axis' not in params:
            raise Exception("Gemini response missing 'x_axis' or 'y_axis'.")

        # 2. Get data from database based on params
        conn = get_db_connection()
        chart_type = params['chart_type']
        x_axis_col = params['x_axis']
        y_axis_col = params['y_axis']

        sql_query = ""
        query_params = []

        if chart_type in ['pie', 'donut']:
            select_clause = f"{x_axis_col}, COUNT(*) as count_value"
            sql_query = f"SELECT {select_clause} FROM POPULATOR"
            if 'filters' in params and params['filters']:
                filter_key_raw = list(params['filters'].keys())[0]
                filter_value = list(params['filters'].values())[0]
                filter_key_cleaned = filter_key_raw.strip('"')
                sql_query += f" WHERE {filter_key_cleaned} = ?"
                query_params.append(filter_value)
            sql_query += f" GROUP BY {x_axis_col}"
        else: # line, bar charts
            select_columns = [x_axis_col, y_axis_col]
            if params.get('dimension') == '3D':
                if 'group_by' not in params:
                    raise Exception("Gemini response missing 'group_by' for 3D chart.")
                select_columns.append(params['group_by'])
            select_clause = ", ".join(select_columns)
            sql_query = f"SELECT {select_clause} FROM POPULATOR"
            if 'filters' in params and params['filters']:
                filter_key_raw = list(params['filters'].keys())[0]
                filter_value = list(params['filters'].values())[0]
                filter_key_cleaned = filter_key_raw.strip('"')
                sql_query += f" WHERE {filter_key_cleaned} = ?"
                query_params.append(filter_value)

        rows_for_chart = conn.execute(sql_query, tuple(query_params)).fetchall()
        conn.close()

        if not rows_for_chart:
            return jsonify({"analysis": "분석할 데이터를 찾을 수 없습니다."})

        # 3. Format data and get analysis from Gemini
        header = rows_for_chart[0].keys()
        data_csv = ",".join(map(str, header)) + "\n"
        for row in rows_for_chart:
            data_csv += ",".join(map(str, row)) + "\n"

        full_report_prompt = GEMINI_REPORT_PROMPT_TEMPLATE.format(
            chart_name=chart_prompt,
            user_prompt="전반적인 분석을 해줘.", # Can be customized later
            data_csv=data_csv
        )
        report_response = gemini_model.generate_content(full_report_prompt)
        analysis_text = report_response.text

        return jsonify({"analysis": analysis_text})

    except Exception as e:
        print(f"Dr. Python Debug: Error generating report for chart '{chart_prompt}': {e}")
        traceback.print_exc()
        return jsonify({"error": f"보고서 생성 중 오류 발생: {e}"}), 500


if __name__ == '__main__':
    # 개발 환경에서만 debug=True 사용
    app.run(debug=True, port=5000)
