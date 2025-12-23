# main.py
from llm_utils import ask_llm

def main():
    print("=== 광고 콘텐츠 생성기 v1 ===")

    product = input("제품/서비스 이름을 입력하세요: ").strip()
    message = input("핵심 메시지를 한 줄로 입력하세요: ").strip()

    prompt = f"""
당신은 디지털 마케팅 카피라이터입니다.
다음 정보를 바탕으로 광고 문구를 작성하시오.

제품/서비스: {product}
핵심 메시지: {message}

출력 형식:
1) 헤드라인 1문장
2) 설명 문장 1문장
3) 행동 유도 문구(CTA) 1문장
"""

    ad_text = ask_llm(prompt, temperature=0.8)

    print("\n[생성된 광고 문구]")
    print(ad_text)

if __name__ == "__main__":
    main()
