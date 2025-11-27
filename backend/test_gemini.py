import os
import google.generativeai as genai

def test_gemini_api():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("오류: GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("스크립트 실행 전 'export GOOGLE_API_KEY=YOUR_API_KEY' 또는 'set GOOGLE_API_KEY=YOUR_API_KEY'를 실행해주세요.")
        return

    try:
        genai.configure(api_key=api_key)
        print("Gemini API가 성공적으로 구성되었습니다.")

        # 사용 가능한 모델 목록 가져오기
        print("\n사용 가능한 Gemini 모델 목록:")
        found_gemini_pro = False
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"  - {m.name} (지원 메서드: {m.supported_generation_methods})")
                if m.name == "models/gemini-pro":
                    found_gemini_pro = True

        if found_gemini_pro:
            print("\n'models/gemini-pro' 모델이 목록에서 확인되었습니다.")
        else:
            print("\n경고: 'models/gemini-pro' 모델이 목록에서 발견되지 않았습니다. API 키 또는 지역 문제일 수 있습니다.")

        # gemini-pro 모델로 간단한 테스트 수행
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Hello, Gemini!")
            print("\n'models/gemini-pro' 모델로 테스트 메시지 생성 성공:")
            print(f"  응답: {response.text[:50]}...") # 처음 50자만 출력
        except Exception as e:
            print(f"\n오류: 'models/gemini-pro' 모델로 메시지 생성 실패: {e}")
            print("이 오류는 모델이 유효하지 않거나, API 키에 해당 모델에 대한 접근 권한이 없음을 의미할 수 있습니다.")

    except Exception as e:
        print(f"\n치명적인 오류: Gemini API 구성 또는 모델 목록 가져오기 실패: {e}")
        print("API 키가 유효하지 않거나, 네트워크 연결에 문제가 있을 수 있습니다.")

if __name__ == "__main__":
    test_gemini_api()

