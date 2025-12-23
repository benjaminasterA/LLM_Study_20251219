# main.py
from llm_utils import ask_llm
from prompt_templates import AD_TEMPLATE

def generate_ad_copies(product: str, message: str, n: int = 5) -> str:
    """서로 다른 스타일의 광고 문구 n개를 생성합니다."""
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
    return ask_llm(prompt, temperature=0.9)

def main():
    print("=== 광고 콘텐츠 생성기 v3 (5종) ===")

    product = input("제품/서비스 이름을 입력하세요: ").strip()
    message = input("핵심 메시지를 한 줄로 입력하세요: ").strip()

    # ① 단일 광고 문구 생성
    single_prompt = AD_TEMPLATE.format(product=product, message=message)
    single_ad = ask_llm(single_prompt, temperature=0.8)

    print("\n[단일 광고 문구]")
    print(single_ad)

    # ② 5종 광고 문구 생성
    multi_ads = generate_ad_copies(product, message, n=5)
    print("\n[서로 다른 스타일의 광고 문구 5종]")
    print(multi_ads)

if __name__ == "__main__":
    main()
