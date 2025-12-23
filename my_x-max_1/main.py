# llm_ad_project/
#  ├── main.py              # 광고 생성기 실행 파일
#  ├── llm_utils.py         # LLM 호출 함수 모듈
#  └── prompt_templates.py  # 프롬프트 템플릿 모음


# main.py

# 우리가 직접 만든 파일들이므로 pip로 설치할 필요가 없습니다. 같은 폴더에 파일이 있는지 확인하세요.
from llm_utils import ask_llm  # 우리가 만든 AI 호출 유틸리티 함수를 가져옵니다. (로컬 파일: pip 설치 불필요)
from prompt_templates import AD_TEMPLATE  # 미리 정의해둔 프롬프트 템플릿을 가져옵니다. (로컬 파일: pip 설치 불필요)

def generate_ad_copies(product: str, message: str, n: int = 5) -> str:
    """서로 다른 스타일의 광고 문구 n개를 생성합니다."""
    
    # 2. 컨텍스트 관리 (프롬프트 구성)
    # ✍️ [기록]: AI에게 건넬 구체적인 작업 지시서(Prompt)를 작성합니다.
    prompt = f"""
당신은 디지털 마케팅 카피라이터입니다.
다음 정보를 바탕으로 서로 다른 스타일의 광고 문구를 {n}개 작성하시오.

제품/서비스: {product}
핵심 메시지: {message}

조건:
- 각 광고 문구는 2문장 이내
- 문체와 표현은 서로 다르게 변형
- 번호를 붙여서 출력

"""
    # 3. 추론 요청
    # 👆 [AI 호출]: 작성된 프롬프트를 가지고 LLM에게 질문을 던집니다. (temperature 0.9로 창의성 높임)
    return ask_llm(prompt, temperature=0.9)

def main():
    # 프로그램 시작 안내
    # 👍 [출력]: 프로그램 제목을 화면에 표시합니다.
    print("=== 광고 콘텐츠 생성기 v3 (5종) ===")

    # 1. 대화 시작 (입력 단계)
    # 👇 [입력 대기]: 사용자가 제품 이름을 입력할 때까지 기다립니다.
    product = input("제품/서비스 이름을 입력하세요: ").strip()
    # 👇 [입력 대기]: 사용자가 핵심 메시지를 입력할 때까지 기다립니다.
    message = input("핵심 메시지를 한 줄로 입력하세요: ").strip()

    # --- ① 단일 광고 문구 생성 ---
    
    # 2. 컨텍스트 관리
    # ✍️ [기록]: 템플릿에 입력값을 채워 넣어 완성된 프롬프트를 만듭니다.
    single_prompt = AD_TEMPLATE.format(product=product, message=message)
    
    # 3. 추론 요청
    # 👆 [AI 호출]: LLM에게 단일 광고 문구 생성을 요청합니다.
    # 🤜 [결과 저장]: 반환된 텍스트를 single_ad 변수에 담습니다.
    single_ad = ask_llm(single_prompt, temperature=0.8)

    # 8. 최종 응답
    # 👍 [출력]: 생성된 단일 광고 문구를 화면에 보여줍니다.
    print("\n[단일 광고 문구]")
    print(single_ad)

    # --- ② 5종 광고 문구 생성 (확장 기능) ---
    
    # 3. 추론 요청 (함수 내부에서 수행)
    # 👆 [AI 호출]: 위에서 정의한 함수를 호출하여 5가지 버전을 요청합니다.
    # 🤜 [결과 저장]: 결과 문자열을 multi_ads 변수에 담습니다.
    multi_ads = generate_ad_copies(product, message, n=5)
    
    # 8. 최종 응답
    # 👍 [출력]: 5가지로 변형된 광고 문구들을 화면에 보여줍니다.
    print("\n[서로 다른 스타일의 광고 문구 5종]")
    print(multi_ads)


if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 아래 함수를 동작시킵니다.
    main()  # 메인 함수 실행